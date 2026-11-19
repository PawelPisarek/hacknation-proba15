"""Generator sztucznego zbioru obrazów RTG naczep (.bmp) z prawdą o „dodatkach”.

Model obrazu: transmisja RTG  I = exp(-T), gdzie T to suma tłumienia elementów
(konstrukcja naczepy, towar, dodatki) w rzucie bocznym. Każda grupa = jedna fizyczna
naczepa z jednym ułożeniem towaru; obrazy w grupie różnią się jak kolejne prześwietlenia:
przesunięcie, skala wzdłuż osi przejazdu (prędkość), wzmocnienie, szum, pasy detektora,
drobne przesunięcia palet. Role obrazów:
  nauka   — czyste obrazy do nauki / wzorzec (pierwszy = wzorzec do porównania par),
  czysty  — czyste obrazy testowe (każda ramka = false positive),
  dodatki — obrazy testowe z ukrytymi przedmiotami (ramki prawdy w etykiety.json).

Użycie:
  python -m rtg.generator --wyjscie dane/maly --grupy 12 --skala 0.25
  python -m rtg.generator --wyjscie dane/duzy --grupy 1 --skala 1 --bity 24   # ~50 MB/obraz
"""
import argparse
import json
import math
import os
import time

import numpy as np
from PIL import Image

PELNY_W, PELNY_H = 7300, 2300  # 7300 x 2300 x 24 bity ≈ 50 MB
TYPY = ("plandeka", "chlodnia", "kontener")
RODZAJE_DODATKOW = ("podwojna_podloga", "sciana_przednia", "rama", "dach", "w_towarze")


class Plotno:
    """Mapa tłumienia T i przekształcenie współrzędnych naczepy (u, v ∈ [0,1]) na piksele."""

    def __init__(self, w, h, geo):
        self.T = np.zeros((h, w), np.float32)
        self.w, self.h = w, h
        self.g = geo  # x0, y0, L, Hh, sx, dx, dy

    def px(self, u, v):
        g = self.g
        cx = g["x0"] + g["L"] / 2
        x = cx + (g["x0"] + u * g["L"] - cx) * g["sx"] + g["dx"]
        y = g["y0"] + v * g["Hh"] + g["dy"]
        return x, y

    def prost_px(self, x0, y0, x1, y1, val):
        """Prostokąt z pokryciem ułamkowym na brzegach (podpikselowe przesunięcia)."""
        if x1 <= x0 or y1 <= y0:
            return
        ix0, iy0 = max(int(math.floor(x0)), 0), max(int(math.floor(y0)), 0)
        ix1, iy1 = min(int(math.ceil(x1)), self.w), min(int(math.ceil(y1)), self.h)
        if ix1 <= ix0 or iy1 <= iy0:
            return
        xs = np.arange(ix0, ix1, dtype=np.float32)
        ys = np.arange(iy0, iy1, dtype=np.float32)
        cx = np.clip(np.minimum(x1, xs + 1) - np.maximum(x0, xs), 0, 1)
        cy = np.clip(np.minimum(y1, ys + 1) - np.maximum(y0, ys), 0, 1)
        self.T[iy0:iy1, ix0:ix1] += val * np.outer(cy, cx)

    def prost(self, u0, v0, u1, v1, val):
        x0, y0 = self.px(u0, v0)
        x1, y1 = self.px(u1, v1)
        self.prost_px(x0, y0, x1, y1, val)
        return x0, y0, x1, y1

    def kolo(self, u, v, r_v, val, r_wew=0.0, val_wew=0.0):
        """Koło (r w jednostkach wysokości naczepy) — opona z piastą."""
        x, y = self.px(u, v)
        r = r_v * self.g["Hh"]
        ix0, iy0 = max(int(x - r - 2), 0), max(int(y - r - 2), 0)
        ix1, iy1 = min(int(x + r + 2), self.w), min(int(y + r + 2), self.h)
        if ix1 <= ix0 or iy1 <= iy0:
            return
        yy, xx = np.mgrid[iy0:iy1, ix0:ix1].astype(np.float32)
        d = np.sqrt((xx + 0.5 - x) ** 2 + (yy + 0.5 - y) ** 2)
        m = np.clip(r - d + 0.5, 0, 1) * val
        if r_wew > 0:
            m += np.clip(r_wew * self.g["Hh"] - d + 0.5, 0, 1) * val_wew
        self.T[iy0:iy1, ix0:ix1] += m


def projekt_grupy(rng, typ):
    """Stałe cechy fizycznej naczepy i jej towaru (wspólne dla wszystkich obrazów grupy)."""
    p = {"typ": typ}
    p["podloga_v"] = rng.uniform(0.70, 0.73)          # górna krawędź podłogi
    p["podloga_t"] = rng.uniform(0.025, 0.035)        # grubość podłogi (v)
    p["rama_v"] = (p["podloga_v"] + p["podloga_t"], p["podloga_v"] + p["podloga_t"] + rng.uniform(0.05, 0.07))
    p["zebra_co"] = rng.uniform(0.025, 0.04)
    p["poprzeczki_co"] = rng.uniform(0.03, 0.05)
    n_osi = 3
    os0 = rng.uniform(0.70, 0.76)
    p["osie"] = [os0 + i * rng.uniform(0.075, 0.085) for i in range(n_osi)]
    p["podpora_u"] = rng.uniform(0.18, 0.24)
    p["sciana"] = {"plandeka": 0.05, "chlodnia": 0.35, "kontener": 0.18}[typ]
    p["agregat"] = typ == "chlodnia"
    # towar: palety w rzędzie, 1–2 warstwy
    towar = []
    u = 0.03
    rodzaj_towaru = rng.choice(["kartony", "butelki", "worki"])
    while u < 0.93:
        szer = rng.uniform(0.045, 0.06)
        if rng.random() < 0.15:  # luka między paletami
            u += szer
            continue
        warstwy = []
        v_d = p["podloga_v"]
        for _ in range(rng.integers(1, 3)):
            wys = rng.uniform(0.18, 0.28)
            if v_d - wys < 0.15:
                break
            nx, ny = int(rng.integers(3, 7)), int(rng.integers(3, 7))
            warstwy.append({"v0": v_d - wys, "v1": v_d - 0.012, "nx": nx, "ny": ny,
                            "gest": float(rng.uniform(0.12, 0.35)), "tlo": float(rng.uniform(0.05, 0.15))})
            v_d -= wys
        towar.append({"u0": u, "u1": u + szer, "warstwy": warstwy})
        u += szer + rng.uniform(0.003, 0.01)
    p["towar"] = towar
    p["rodzaj_towaru"] = str(rodzaj_towaru)
    return p


def rysuj_naczepe(pl, p, rng_obrazu, jitter_palet):
    """Konstrukcja + towar. Zwraca listę prostokątów palet w pikselach (do dodatków w towarze)."""
    sc = p["sciana"]
    pl.prost(0.0, 0.10, 1.0, 0.105, 0.10)                       # dach
    pl.prost(0.0, 0.10, 1.0, p["podloga_v"], sc)                # ściany boczne (rzut)
    pl.prost(0.0, 0.10, 0.012, p["podloga_v"], 0.9)             # ściana przednia
    pl.prost(0.988, 0.10, 1.0, p["podloga_v"], 0.7)             # drzwi tylne
    pl.prost(0.0, p["podloga_v"], 1.0, p["podloga_v"] + p["podloga_t"], 0.8)  # podłoga
    u = 0.02
    while u < 0.98:                                             # żebra ścian / łuki plandeki
        pl.prost(u, 0.10, u + 0.003, p["podloga_v"], 0.12 if p["typ"] != "plandeka" else 0.08)
        u += p["zebra_co"]
    if p["typ"] == "kontener":                                  # słupki narożne
        for u0 in (0.012, 0.25, 0.5, 0.75, 0.976):
            pl.prost(u0, 0.10, u0 + 0.008, p["podloga_v"], 0.5)
    if p["agregat"]:                                            # agregat chłodniczy z przodu
        pl.prost(-0.035, 0.14, 0.0, 0.42, 1.1)
        pl.prost(-0.03, 0.18, -0.006, 0.38, 0.6)
    r0, r1 = p["rama_v"]
    pl.prost(0.0, r0, 1.0, r0 + 0.012, 1.0)                     # podłużnica ramy
    pl.prost(0.0, r1 - 0.012, 1.0, r1, 1.0)
    u = 0.03
    while u < 0.97:                                             # poprzeczki
        pl.prost(u, r0, u + 0.006, r1, 0.7)
        u += p["poprzeczki_co"]
    pl.prost(0.03, r0 - 0.005, 0.06, r1 + 0.01, 1.4)            # płyta sworznia
    pl.prost(p["podpora_u"], r1, p["podpora_u"] + 0.008, 0.92, 0.9)  # podpory
    for os_u in p["osie"]:
        pl.prost(os_u - 0.02, r1, os_u + 0.02, r1 + 0.02, 1.2)  # resor
        pl.kolo(os_u, 0.875, 0.09, 0.9, r_wew=0.04, val_wew=1.5)
    # towar
    palety = []
    for i, pal in enumerate(p["towar"]):
        du = jitter_palet[i]
        u0, u1 = pal["u0"] + du, pal["u1"] + du
        pl.prost(u0, p["podloga_v"] - 0.012, u1, p["podloga_v"], 0.45)  # paleta drewniana
        for w in pal["warstwy"]:
            ramka = pl.prost(u0, w["v0"], u1, w["v1"], w["tlo"])
            szu = (u1 - u0) / w["nx"]
            szv = (w["v1"] - w["v0"]) / w["ny"]
            for a in range(w["nx"]):
                for b in range(w["ny"]):
                    cu, cv = u0 + a * szu, w["v0"] + b * szv
                    if p["rodzaj_towaru"] == "butelki":
                        pl.prost(cu + 0.25 * szu, cv + 0.1 * szv, cu + 0.75 * szu, cv + 0.95 * szv, w["gest"])
                    elif p["rodzaj_towaru"] == "worki":
                        pl.prost(cu + 0.05 * szu, cv + 0.2 * szv, cu + 0.95 * szu, cv + 0.9 * szv, w["gest"])
                    else:
                        pl.prost(cu + 0.04 * szu, cv + 0.04 * szv, cu + 0.96 * szu, cv + 0.96 * szv, w["gest"] * 0.6)
            palety.append(ramka)
    return palety


def paczki(pl, x0, y0, x1, y1, val, rng):
    """Dodatek jako ułożone paczki (np. papierosy): siatka małych prostokątów + tło."""
    pl.prost_px(x0, y0, x1, y1, val * 0.4)
    nx = max(1, int((x1 - x0) / max(3.0, (y1 - y0) / 2)))
    ny = max(1, int(round((y1 - y0) / max(3.0, (x1 - x0) / max(nx, 1)))))
    ny = min(ny, 6)
    sx, sy = (x1 - x0) / nx, (y1 - y0) / ny
    for a in range(nx):
        for b in range(ny):
            pl.prost_px(x0 + a * sx + 0.1 * sx, y0 + b * sy + 0.1 * sy,
                        x0 + (a + 0.9) * sx, y0 + (b + 0.9) * sy, val * 0.6)


def dodaj(pl, p, rodzaj, rng, palety, kontrast):
    """Rysuje jeden dodatek i zwraca jego ramkę prawdy [x, y, w, h] w pikselach."""
    val = kontrast * rng.uniform(0.8, 1.2)
    if rodzaj == "podwojna_podloga":
        u0 = rng.uniform(0.08, 0.7)
        u1 = u0 + rng.uniform(0.06, 0.2)
        x0, y0 = pl.px(u0, p["podloga_v"] - p["podloga_t"] * 0.7)
        x1, y1 = pl.px(u1, p["podloga_v"])
    elif rodzaj == "sciana_przednia":
        v0 = rng.uniform(0.15, 0.4)
        x0, y0 = pl.px(0.013, v0)
        x1, y1 = pl.px(0.013 + rng.uniform(0.008, 0.015), v0 + rng.uniform(0.12, 0.25))
    elif rodzaj == "rama":
        r0, r1 = p["rama_v"]
        u0 = rng.uniform(0.25, 0.65)
        x0, y0 = pl.px(u0, r0 + 0.013)
        x1, y1 = pl.px(u0 + rng.uniform(0.04, 0.12), r1 - 0.013)
    elif rodzaj == "dach":
        u0 = rng.uniform(0.1, 0.8)
        x0, y0 = pl.px(u0, 0.106)
        x1, y1 = pl.px(u0 + rng.uniform(0.05, 0.12), 0.125)
    else:  # w_towarze
        if not palety:
            return dodaj(pl, p, "podwojna_podloga", rng, palety, kontrast)
        bx0, by0, bx1, by1 = palety[int(rng.integers(len(palety)))]
        fw, fh = rng.uniform(0.3, 0.6), rng.uniform(0.3, 0.6)
        ox = rng.uniform(0, 1 - fw) * (bx1 - bx0)
        oy = rng.uniform(0, 1 - fh) * (by1 - by0)
        x0, y0 = bx0 + ox, by0 + oy
        x1, y1 = x0 + fw * (bx1 - bx0), y0 + fh * (by1 - by0)
    paczki(pl, x0, y0, x1, y1, val, rng)
    return [int(math.floor(x0)), int(math.floor(y0)), int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))]


def obraz(w, h, p, rng, dodatki_rodzaje, kontrast):
    s = w / PELNY_W
    geo = {"x0": 0.08 * w, "y0": 0.0, "L": 0.84 * w, "Hh": 0.97 * h,
           "sx": rng.uniform(0.985, 1.015), "dx": rng.normal(0, 0.004 * w), "dy": rng.normal(0, 0.003 * h)}
    pl = Plotno(w, h, geo)
    jit = rng.normal(0, 0.0015, size=len(p["towar"]))
    palety = rysuj_naczepe(pl, p, rng, jit)
    ramki = []
    for r in dodatki_rodzaje:
        ramki.append({"rodzaj": r, "ramka": dodaj(pl, p, r, rng, palety, kontrast)})
    gain = rng.uniform(0.97, 1.03)
    I = np.exp(-pl.T * gain)
    # szum fotonowy (zależny od sygnału), pasy detektora (wiersze), pasy przejazdu (kolumny)
    I = I + rng.normal(0, 1, I.shape).astype(np.float32) * (0.004 + 0.012 * np.sqrt(I))
    I = I * (1 + rng.normal(0, 0.004, (h, 1)).astype(np.float32)) * (1 + rng.normal(0, 0.002, (1, w)).astype(np.float32))
    pix = np.clip(8 + 240 * I, 0, 255).astype(np.uint8)
    return pix, ramki, {k: float(v) for k, v in geo.items()}, float(s)


def zapisz_bmp(pix, sciezka, bity):
    im = Image.fromarray(pix, "L")
    if bity == 24:
        im = im.convert("RGB")
    im.save(sciezka, format="BMP")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wyjscie", required=True)
    ap.add_argument("--grupy", type=int, default=12)
    ap.add_argument("--nauka", type=int, default=4, help="czystych obrazów do nauki na grupę")
    ap.add_argument("--czyste", type=int, default=2, help="czystych obrazów testowych na grupę")
    ap.add_argument("--z-dodatkami", type=int, default=3, help="obrazów z dodatkami na grupę")
    ap.add_argument("--skala", type=float, default=0.25, help="1.0 = 7300x2300 (≈50 MB przy 24 bitach)")
    ap.add_argument("--bity", type=int, choices=(8, 24), default=8)
    ap.add_argument("--kontrast", type=float, default=0.35, help="tłumienie dodatku (mniej = trudniej)")
    ap.add_argument("--ziarno", type=int, default=15)
    a = ap.parse_args()

    w, h = int(round(PELNY_W * a.skala)), int(round(PELNY_H * a.skala))
    kat = os.path.join(a.wyjscie, "obrazy")
    os.makedirs(kat, exist_ok=True)
    rng_g = np.random.default_rng(a.ziarno)
    wpisy = []
    t0 = time.time()
    for g in range(a.grupy):
        typ = TYPY[g % len(TYPY)]
        seed_g = int(rng_g.integers(1 << 31))
        p = projekt_grupy(np.random.default_rng(seed_g), typ)
        role = ["nauka"] * a.nauka + ["czysty"] * a.czyste + ["dodatki"] * a.z_dodatkami
        wzorzec = None
        for i, rola in enumerate(role):
            rng = np.random.default_rng([seed_g, i])
            rodzaje = []
            if rola == "dodatki":
                n = int(rng.integers(1, 3))
                rodzaje = [str(x) for x in rng.choice(RODZAJE_DODATKOW, size=n, replace=False)]
            pix, ramki, geo, _ = obraz(w, h, p, rng, rodzaje, a.kontrast)
            nazwa = f"g{g:03d}_{typ}_{i:02d}_{rola}.bmp"
            zapisz_bmp(pix, os.path.join(kat, nazwa), a.bity)
            if wzorzec is None:
                wzorzec = nazwa
            wpisy.append({"plik": nazwa, "grupa": f"g{g:03d}", "typ": typ, "rola": rola,
                          "wzorzec": wzorzec, "dodatki": ramki, "geometria": geo})
    meta = {"szer": w, "wys": h, "bity": a.bity, "skala": a.skala, "kontrast": a.kontrast,
            "ziarno": a.ziarno, "obrazy": wpisy}
    with open(os.path.join(a.wyjscie, "etykiety.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    mb = os.path.getsize(os.path.join(kat, wpisy[0]["plik"])) / 1e6
    print(f"wygenerowano {len(wpisy)} obrazów {w}x{h} {a.bity} bit ({mb:.1f} MB/obraz) w {time.time()-t0:.1f} s -> {a.wyjscie}")


if __name__ == "__main__":
    main()

# <!-- skill: dummy-dataset -->
