"""Wykrywanie dodatków: porównanie obrazu badanego z wzorcem (obliczenia na karcie, torch/CUDA).

Metody (hipotezy wyniku bazowego):
  roznica — H1: różnica po wyrównaniu (skala wzdłuż przejazdu + przesunięcie + wzmocnienie)
            badanego do jednego wzorca czystego; próg z czystych par.
  nauka   — H2: model nauczony na kilku czystych obrazach grupy: średnia i rozrzut każdego
            piksela (po wyrównaniu), wynik = odchylenie w jednostkach rozrzutu; próg z
            walidacji krzyżowej (zostaw-jeden) na czystych.
Wynik: JSON z ramkami [x, y, w, h, punktacja] w pikselach oryginału i czasem na obraz.

  python -m rtg.wykryj --dane dane/maly --metoda roznica nauka --wyjscie wyniki
"""
import argparse
import json
import os
import time
from collections import defaultdict

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
DEV = None


def wczytaj(sciezka, roboczy):
    """BMP -> tłumienie A = -ln(I) w rozdzielczości roboczej (szerokość ≈ roboczy)."""
    im = Image.open(sciezka).convert("L")
    W, H = im.size
    x = torch.from_numpy(np.asarray(im, dtype=np.uint8).copy()).to(DEV).float()
    x = ((x - 8) / 240).clamp(0.01, 1.0)
    A = -torch.log(x)[None, None]
    f = max(1, round(W / roboczy))
    if f > 1:
        A = F.avg_pool2d(A, f)
    return A[0, 0], f, (W, H)


def warp(A, sx, dx, dy):
    """out(x,y) = A(cx + sx*(x-cx) + dx, y + dy) (bilinearnie)."""
    h, w = A.shape
    xs = torch.arange(w, device=DEV, dtype=torch.float32)
    ys = torch.arange(h, device=DEV, dtype=torch.float32)
    cx = (w - 1) / 2
    gx = cx + sx * (xs - cx) + dx
    gy = ys + dy
    gx = gx / (w - 1) * 2 - 1
    gy = gy / (h - 1) * 2 - 1
    grid = torch.stack(torch.meshgrid(gy, gx, indexing="ij")[::-1], -1)[None]
    return F.grid_sample(A[None, None], grid, align_corners=True, padding_mode="border")[0, 0]


def okno(h, w):
    return torch.outer(torch.hann_window(h, device=DEV), torch.hann_window(w, device=DEV))


def faza(R, M, win):
    """Korelacja fazowa: przesunięcie (dy, dx) i siła szczytu."""
    a = (R - R.mean()) * win
    b = (M - M.mean()) * win
    Fa, Fb = torch.fft.rfft2(a), torch.fft.rfft2(b)
    C = Fa * Fb.conj()
    c = torch.fft.irfft2(C / (C.abs() + 1e-6), s=a.shape)
    k = int(torch.argmax(c))
    h, w = a.shape
    py, px = k // w, k % w
    dy = py if py <= h // 2 else py - h
    dx = px if px <= w // 2 else px - w
    return float(dy), float(dx), float(c.flatten()[k])


def wyrownaj(R, A):
    """Szuka sx, dx, dy, aby warp(A) ≈ R. Zwraca wyrównany A (znormalizowany do wzmocnienia R)."""
    win = okno(*R.shape)
    best = None
    for sx in torch.linspace(0.97, 1.03, 25).tolist():
        M = warp(A, sx, 0.0, 0.0)
        dy, dx, pk = faza(R, M, win)
        if best is None or pk > best[0]:
            best = (pk, sx, dx, dy)
    _, sx, dx, dy = best
    # znak przesunięcia sprawdzamy wprost (mniejszy błąd wygrywa), potem dokładamy ±0.5 px
    kand = []
    for s in (1, -1):
        for ex in (-0.5, 0, 0.5):
            for ey in (-0.5, 0, 0.5):
                M = warp(A, sx, s * dx + ex, s * dy + ey)
                kand.append((float(((M - R) ** 2).mean()), M))
    M = min(kand, key=lambda t: t[0])[1]
    g = float((M * R).sum() / (M * M).sum().clamp_min(1e-6))
    return M * g


def rozmyj(x, sigma=1.5):
    r = int(3 * sigma)
    t = torch.arange(-r, r + 1, device=DEV, dtype=torch.float32)
    k = torch.exp(-t ** 2 / (2 * sigma ** 2))
    k = k / k.sum()
    x = F.conv2d(x[None, None], k.view(1, 1, 1, -1), padding=(0, r))
    x = F.conv2d(x, k.view(1, 1, -1, 1), padding=(r, 0))
    return x[0, 0]


def otwarcie(x, k):
    """Otwarcie morfologiczne (min potem max k×k) — zostają tylko plamy ≥ k×k."""
    p = k // 2
    m = -F.max_pool2d(-x[None, None], k, 1, p)
    return F.max_pool2d(m, k, 1, p)[0, 0]


def skladowe(maska):
    """Etykietowanie spójnych składowych na karcie (propagacja maksimum)."""
    h, w = maska.shape
    lab = torch.arange(1, h * w + 1, device=DEV, dtype=torch.float32).view(h, w) * maska
    for i in range(4000):
        nowy = F.max_pool2d(lab[None, None], 3, 1, 1)[0, 0] * maska
        if i % 10 == 0 and torch.equal(nowy, lab):
            break
        lab = nowy
    return lab


def ramki(score, prog, k, f, rozmiar):
    o = otwarcie(score, k)
    maska = (o > prog).float()
    if maska.sum() == 0:
        return []
    lab = skladowe(F.max_pool2d(maska[None, None], k, 1, k // 2)[0, 0])
    idx = lab > 0
    ys, xs = torch.nonzero(idx, as_tuple=True)
    l = lab[idx]
    u, inv = torch.unique(l, return_inverse=True)
    n = len(u)
    big = 1 << 30
    x0 = torch.full((n,), big, device=DEV, dtype=torch.long).scatter_reduce(0, inv, xs, "amin")
    x1 = torch.zeros(n, device=DEV, dtype=torch.long).scatter_reduce(0, inv, xs, "amax")
    y0 = torch.full((n,), big, device=DEV, dtype=torch.long).scatter_reduce(0, inv, ys, "amin")
    y1 = torch.zeros(n, device=DEV, dtype=torch.long).scatter_reduce(0, inv, ys, "amax")
    sc = torch.zeros(n, device=DEV).scatter_reduce(0, inv, o[idx], "amax")
    W, H = rozmiar
    out = []
    for a, b, c, d, s in zip(x0.tolist(), y0.tolist(), x1.tolist(), y1.tolist(), sc.tolist()):
        X0, Y0 = a * f, b * f
        out.append([X0, Y0, min(W, (c + 1) * f) - X0, min(H, (d + 1) * f) - Y0, round(s / prog, 3)])
    return out


class Roznica:
    """H1: jeden wzorzec, różnica dodatnia (więcej materiału) po wyrównaniu."""

    def __init__(self, A_nauka, k, zapas):
        self.R = A_nauka[0]
        self.k = k
        sc = [self.punktacja(A) for A in A_nauka[1:]]
        self.prog = zapas * max(float(otwarcie(s, k).max()) for s in sc)

    def punktacja(self, A):
        return rozmyj(wyrownaj(self.R, A) - self.R)


class Nauka:
    """H2: średnia i rozrzut czystych obrazów (po wyrównaniu do pierwszego); z-score."""

    def __init__(self, A_nauka, k, zapas):
        self.k = k
        R = A_nauka[0]
        self.al = [R] + [wyrownaj(R, A) for A in A_nauka[1:]]
        self.R = R
        # próg: zostaw-jeden
        maks = []
        for i in range(len(self.al)):
            reszta = [a for j, a in enumerate(self.al) if j != i]
            M, S = self.model(reszta)
            maks.append(float(otwarcie(self.z(self.al[i], M, S), k).max()))
        self.M, self.S = self.model(self.al)
        self.prog = zapas * max(maks)

    @staticmethod
    def model(al):
        X = torch.stack(al)
        M = X.mean(0)
        S = X.std(0) if len(al) > 1 else torch.zeros_like(M)
        S = F.max_pool2d(S[None, None], 5, 1, 2)[0, 0]  # tolerancja drobnych przesunięć przy krawędziach
        s0 = float(S.median())
        return M, torch.sqrt(S ** 2 + s0 ** 2 + 1e-8)

    def z(self, Aal, M, S):
        return rozmyj((Aal - M) / S)

    def punktacja(self, A):
        return self.z(wyrownaj(self.R, A), self.M, self.S)


METODY = {"roznica": Roznica, "nauka": Nauka}


def main():
    global DEV
    ap = argparse.ArgumentParser()
    ap.add_argument("--dane", required=True)
    ap.add_argument("--metoda", nargs="+", default=["roznica", "nauka"], choices=list(METODY))
    ap.add_argument("--wyjscie", default="wyniki")
    ap.add_argument("--roboczy", type=int, default=1800, help="szerokość robocza w pikselach")
    ap.add_argument("--k", type=int, default=5, help="min. rozmiar plamy (px roboczych)")
    ap.add_argument("--zapas", type=float, default=1.1, help="mnożnik progu z czystych")
    a = ap.parse_args()
    if not torch.cuda.is_available():
        raise SystemExit("BRAK KARTY: torch.cuda.is_available() == False — nie liczę na procesorze")
    DEV = torch.device("cuda")
    print("karta:", torch.cuda.get_device_name(0), "torch", torch.__version__)
    meta = json.load(open(os.path.join(a.dane, "etykiety.json")))
    kat = os.path.join(a.dane, "obrazy")
    grupy = defaultdict(list)
    for o in meta["obrazy"]:
        grupy[o["grupa"]].append(o)
    os.makedirs(a.wyjscie, exist_ok=True)
    for nazwa in a.metoda:
        wynik = {"metoda": nazwa, "dane": a.dane, "parametry": vars(a), "obrazy": {}, "modele": {}}
        torch.cuda.synchronize()
        for g, obr in sorted(grupy.items()):
            t0 = time.time()
            nauka = [wczytaj(os.path.join(kat, o["plik"]), a.roboczy) for o in obr if o["rola"] == "nauka"]
            model = METODY[nazwa]([x[0] for x in nauka], a.k, a.zapas)
            torch.cuda.synchronize()
            wynik["modele"][g] = {"prog": model.prog, "czas_s": round(time.time() - t0, 3)}
            for o in obr:
                if o["rola"] == "nauka":
                    continue
                t0 = time.time()
                A, f, rozm = wczytaj(os.path.join(kat, o["plik"]), a.roboczy)
                r = ramki(model.punktacja(A), model.prog, a.k, f, rozm)
                torch.cuda.synchronize()
                wynik["obrazy"][o["plik"]] = {"ramki": r, "czas_s": round(time.time() - t0, 3)}
        sc = os.path.join(a.wyjscie, f"{nazwa}.json")
        json.dump(wynik, open(sc, "w"), indent=1)
        print("zapisano", sc, "pamięć karty max", round(torch.cuda.max_memory_allocated() / 1e6), "MB")


if __name__ == "__main__":
    main()
