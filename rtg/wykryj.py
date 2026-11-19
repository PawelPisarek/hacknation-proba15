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


PAS = None  # (od, do) — ułamek wysokości obrazu używany do wyrównania; None = cały obraz


def wyrownaj(R, A, pas=-1, zwroc_ncc=False):
    """Szuka sx, dx, dy, aby warp(A) ≈ R. Zwraca wyrównany A (znormalizowany do wzmocnienia R).

    pas: pas wierszy (ułamki wysokości) do dopasowania — w wariancie z pustym wzorcem bierzemy
    podłogę, ramę i koła (bez towaru), bo towar zmienia obraz ponad podłogą.
    """
    pas = PAS if pas == -1 else pas
    h = R.shape[0]
    y0, y1 = (0, h) if pas is None else (int(pas[0] * h), int(pas[1] * h))
    Rp = R[y0:y1]
    win = okno(*Rp.shape)
    best = None
    for sx in torch.linspace(0.97, 1.03, 25).tolist():
        M = warp(A, sx, 0.0, 0.0)[y0:y1]
        dy, dx, pk = faza(Rp, M, win)
        if best is None or pk > best[0]:
            best = (pk, sx, dx, dy)
    _, sx, dx, dy = best
    # znak przesunięcia sprawdzamy wprost (mniejszy błąd wygrywa), potem dokładamy ±0.5 px
    kand = []
    for s in (1, -1):
        for ex in (-0.5, 0, 0.5):
            for ey in (-0.5, 0, 0.5):
                M = warp(A, sx, s * dx + ex, s * dy + ey)
                kand.append((float(((M[y0:y1] - Rp) ** 2).mean()), M))
    M = min(kand, key=lambda t: t[0])[1]
    Mp = M[y0:y1]
    g = float((Mp * Rp).sum() / (Mp * Mp).sum().clamp_min(1e-6))
    if not zwroc_ncc:
        return M * g
    a, b = Mp - Mp.mean(), Rp - Rp.mean()
    ncc = float((a * b).sum() / (a.norm() * b.norm()).clamp_min(1e-6))
    return M * g, ncc


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
    return sorted(out, key=lambda r: -r[4])


class Roznica:
    """H1: jeden wzorzec, różnica dodatnia (więcej materiału) po wyrównaniu."""

    def __init__(self, A_nauka, k, zapas):
        self.R = A_nauka[0]
        self.k = k
        sc = [self.punktacja(A) for A in A_nauka[1:]]
        self.prog = zapas * max(float(otwarcie(s, k).max()) for s in sc)

    def surowa(self, Aal):
        return Aal - self.R

    def ocen(self, Aal):
        return rozmyj(Aal - self.R)

    def punktacja(self, A):
        return self.ocen(wyrownaj(self.R, A))


class Nauka:
    """H2: średnia i rozrzut czystych obrazów (po wyrównaniu do pierwszego); z-score."""

    def __init__(self, A_nauka, k, zapas):
        self.k = k
        R = A_nauka[0]
        self.al = [R] + [wyrownaj(R, A) for A in A_nauka[1:]]
        self.R = R
        maks = []  # próg: zostaw-jeden
        for i in range(len(self.al)):
            reszta = [a for j, a in enumerate(self.al) if j != i]
            M, S = self.model(reszta)
            maks.append(float(otwarcie(self.z(self.al[i], M, S), k).max()))
        self.M, self.S = self.model(self.al)
        self.prog = zapas * max(maks)
        del self.al

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

    def surowa(self, Aal):
        return Aal - self.M

    def ocen(self, Aal):
        return self.z(Aal, self.M, self.S)

    def punktacja(self, A):
        return self.ocen(wyrownaj(self.R, A))


METODY = {"roznica": Roznica, "nauka": Nauka}
KOMORKA = 16          # komórka cech towaru (px roboczych)
STREFA_TOWARU = (0.09, 0.70)  # wiersze (ułamek wysokości) między dachem a podłogą — tam może być towar
PAS_DOBORU = (0.69, 0.97)     # podłoga, rama, koła — bez towaru


def cechy_komorek(D):
    """Średnia i odchylenie różnicy w komórkach KOMORKA×KOMORKA."""
    e = F.avg_pool2d(D[None, None], KOMORKA, KOMORKA, ceil_mode=True)[0, 0]
    e2 = F.avg_pool2d((D * D)[None, None], KOMORKA, KOMORKA, ceil_mode=True)[0, 0]
    return e, (e2 - e * e).clamp_min(0).sqrt()


def maska_strefy(shape_kom, h):
    hk = shape_kom[0]
    rows = (torch.arange(hk, device=DEV, dtype=torch.float32) + 0.5) * KOMORKA / h
    return ((rows > STREFA_TOWARU[0]) & (rows < STREFA_TOWARU[1]))[:, None].expand(shape_kom)


def tryb_biblioteki(a, meta, kat, nazwa, towar_tryb):
    """Wzorzec dobiera system z biblioteki pustych naczep (P19); wybór towaru wygasza zgodny ładunek."""
    global PAS
    PAS = PAS_DOBORU
    bib = defaultdict(list)
    for o in meta["obrazy"]:
        if o["rola"] == "biblioteka":
            bib[o["typ"]].append(o)
    modele, t0 = {}, time.time()
    for typ, obr in sorted(bib.items()):
        A = [wczytaj(os.path.join(kat, o["plik"]), a.roboczy)[0] for o in obr]
        m = METODY[nazwa](A, a.k, a.zapas)
        m._bib = A
        modele[typ] = m
    # próg „wzorzec niepewny”: NCC pasa konstrukcji — swój typ vs obce typy (z biblioteki)
    swoje, obce = [], []
    for typ, m in modele.items():
        for A in m._bib[1:]:
            swoje.append(wyrownaj(m.R, A, zwroc_ncc=True)[1])
        for typ2, m2 in modele.items():
            if typ2 != typ:
                obce.append(wyrownaj(m2.R, m._bib[0], zwroc_ncc=True)[1])
    prog_ncc = (min(swoje) + max(obce)) / 2 if min(swoje) > max(obce) else 0.98 * min(swoje)
    # nauka towaru: obwiednia cech komórek (średnia, odchylenie różnicy) dla każdego rodzaju
    obw = {}
    for o in meta["obrazy"]:
        if o["rola"] != "nauka_towaru":
            continue
        A, f, _ = wczytaj(os.path.join(kat, o["plik"]), a.roboczy)
        m = modele[o["typ"]]
        e, s = cechy_komorek(m.surowa(wyrownaj(m.R, A)))
        st = maska_strefy(e.shape, A.shape[0])
        E, S = float(e[st].max()), float(s[st].max())
        p = obw.get(o["towar_zgloszony"], (0.0, 0.0))
        obw[o["towar_zgloszony"]] = (max(p[0], E), max(p[1], S))
    for m in modele.values():
        del m._bib
    torch.cuda.synchronize()
    wynik = {"metoda": nazwa, "towar": towar_tryb, "tryb": "biblioteka", "dane": a.dane, "parametry": vars(a),
             "prog_ncc": prog_ncc, "ncc_swoje_min": min(swoje), "ncc_obce_max": max(obce),
             "obwiednie_towaru": obw, "budowa_modelu_s": round(time.time() - t0, 3),
             "modele": {t: {"prog": m.prog} for t, m in modele.items()}, "obrazy": {}}
    for o in meta["obrazy"]:
        if o["rola"] not in ("czysty", "dodatki"):
            continue
        t0 = time.time()
        A, f, rozm = wczytaj(os.path.join(kat, o["plik"]), a.roboczy)
        best = None
        for typ, m in modele.items():  # dobór wzorca: najlepsze dopasowanie pasa konstrukcji
            Aal, ncc = wyrownaj(m.R, A, zwroc_ncc=True)
            if best is None or ncc > best[0]:
                best = (ncc, typ, Aal)
        ncc, typ, Aal = best
        m = modele[typ]
        score = m.ocen(Aal)
        towar = o.get("towar_zgloszony", "pusta") if towar_tryb == "zgloszony" else "nie_wiem"
        wygaszone = 0
        if towar in obw:  # wybór towaru: komórki w strefie towaru zgodne z obwiednią → bez ramek
            E, S = obw[towar]
            e, s = cechy_komorek(m.surowa(Aal))
            zg = (e <= 1.05 * E) & (s <= 1.05 * S) & maska_strefy(e.shape, A.shape[0])
            wygaszone = int(zg.sum())
            zgp = zg.float().repeat_interleave(KOMORKA, 0).repeat_interleave(KOMORKA, 1)[:score.shape[0], :score.shape[1]]
            score = score * (1 - zgp)
        r = ramki(score, m.prog, a.k, f, rozm)
        torch.cuda.synchronize()
        wynik["obrazy"][o["plik"]] = {"ramki": r, "czas_s": round(time.time() - t0, 3), "wzorzec_typ": typ,
                                      "wzorzec": f"W-{typ}", "niepewny": ncc < prog_ncc, "ncc": round(ncc, 4),
                                      "towar_wybrany": towar, "komorki_wygaszone": wygaszone}
    return wynik


def tryb_grup(a, meta, kat, nazwa):
    """Wzorzec = obrazy „nauka” tej samej grupy (warianty ta_sama / pusta)."""
    grupy = defaultdict(list)
    for o in meta["obrazy"]:
        grupy[o["grupa"]].append(o)
    wynik = {"metoda": nazwa, "towar": "nie_wiem", "tryb": "grupa", "dane": a.dane, "parametry": vars(a),
             "obrazy": {}, "modele": {}}
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
    return wynik


def main():
    global DEV
    ap = argparse.ArgumentParser()
    ap.add_argument("--dane", required=True)
    ap.add_argument("--metoda", nargs="+", default=["roznica", "nauka"], choices=list(METODY))
    ap.add_argument("--towar", nargs="+", default=["nie_wiem"], choices=["nie_wiem", "zgloszony"],
                    help="biblioteka: nie_wiem = nic nie wygaszamy; zgloszony = operator wybrał towar z etykiety")
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
    os.makedirs(a.wyjscie, exist_ok=True)
    bibl = meta.get("wariant") == "biblioteka"
    for nazwa in a.metoda:
        for towar in (a.towar if bibl else ["nie_wiem"]):
            torch.cuda.reset_peak_memory_stats()
            wynik = tryb_biblioteki(a, meta, kat, nazwa, towar) if bibl else tryb_grup(a, meta, kat, nazwa)
            wynik["pamiec_karty_max_MB"] = round(torch.cuda.max_memory_allocated() / 1e6)
            wynik["czas_obejmuje"] = "wczytanie pełnego .bmp, zmniejszenie do szerokości roboczej, dobór wzorca, punktacja, ramki"
            sc = os.path.join(a.wyjscie, f"{nazwa}_{towar}.json" if bibl else f"{nazwa}.json")
            json.dump(wynik, open(sc, "w"), indent=1)
            print("zapisano", sc, "pamięć karty max", wynik["pamiec_karty_max_MB"], "MB")


if __name__ == "__main__":
    main()
