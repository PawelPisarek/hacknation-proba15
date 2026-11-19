"""Generator sztucznego zbioru obrazów RTG naczep (.bmp) z prawdą o „dodatkach”.

Model obrazu: transmisja RTG  I = exp(-T), gdzie T to suma tłumienia elementów
(konstrukcja naczepy, towar, dodatki) w rzucie bocznym. Konstrukcja zależy od typu
(model naczepy), towar od załadunku; kolejne prześwietlenia różnią się przesunięciem, skalą
wzdłuż przejazdu (prędkość), wzmocnieniem, szumem, pasami detektora, przesunięciem palet.

Warianty (--wariant):
  ta_sama    — grupa = jedna naczepa z jednym towarem; nauka = czyste tej samej naczepy z tym towarem.
  pusta      — (P19) nauka = pusta naczepa; badane w 2/3 załadowane zgłoszonym towarem.
  biblioteka — (P19, KA1, KA5) biblioteka pustych wzorców typów plandeka/chłodnia/kontener;
               obrazy „nauka_towaru” (czyste załadowane, 5 rodzajów towaru) do nauki towaru;
               badane: typy z biblioteki i typ spoza biblioteki (skrzyniowa) — wzorzec dobiera system.
Role: biblioteka / nauka / nauka_towaru (do nauki), czysty (każda ramka = FP), dodatki (ramki prawdy).
Towary (P20/P23): drobnica, plyny, sypkie, maszyny, meble, pusta.
--trudny: niższy kontrast dodatków i ~2x zakłócenia (przesunięcie, skala, szum, palety) — KA8.

  python -m rtg.generator --wyjscie dane/bib --wariant biblioteka --skala 0.25
  python -m rtg.generator --wyjscie dane/duzy --grupy 1 --skala 1 --bity 24   # ~50 MB/obraz
"""
import argparse
import json
import math
import os
import time
import zlib

import numpy as np
from PIL import Image

PELNY_W, PELNY_H = 7300, 2300  # 7300 x 2300 x 24 bity ≈ 50 MB
TYPY = ("plandeka", "chlodnia", "kontener")
TYP_SPOZA = "skrzyniowa"
TOWARY = ("drobnica", "plyny", "sypkie", "maszyny", "meble")
RODZAJE_DODATKOW = ("podwojna_podloga", "sciana_przednia", "rama", "dach", "w_towarze", "jak_towar")
WYMAGA_TOWARU = ("w_towarze", "jak_towar")


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


def projekt_typu(typ, ziarno=0):
    """Konstrukcja modelu naczepy — stała dla typu (biblioteka wzorców = puste naczepy typu)."""
    rng = np.random.default_rng([zlib.crc32(typ.encode()), ziarno])
    p = {"typ": typ}
    p["podloga_v"] = rng.uniform(0.70, 0.73)
    p["podloga_t"] = rng.uniform(0.025, 0.035)
    p["rama_v"] = (p["podloga_v"] + p["podloga_t"], p["podloga_v"] + p["podloga_t"] + rng.uniform(0.05, 0.07))
    p["zebra_co"] = rng.uniform(0.025, 0.04)
    p["poprzeczki_co"] = rng.uniform(0.03, 0.05)
    n_osi = 2 if typ == TYP_SPOZA else 3
    os0 = rng.uniform(0.68, 0.78)
    p["osie"] = [os0 + i * rng.uniform(0.075, 0.085) for i in range(n_osi)]
    p["podpora_u"] = rng.uniform(0.16, 0.26)
    p["sciana"] = {"plandeka": 0.05, "chlodnia": 0.35, "kontener": 0.18, TYP_SPOZA: 0.25}[typ]
    p["agregat"] = typ == "chlodnia"
    p["slupki"] = typ == "kontener"
    return p


def element(rodzaj, rng, u0, v0, u1, v1):
    """Prostokąty (u0, v0, u1, v1, tłumienie) jednej jednostki towaru danego rodzaju w ramce."""
    w, h = u1 - u0, v1 - v0
    r = []
    if rodzaj == "drobnica":  # kartony z drobnymi przedmiotami
        r.append((u0, v0, u1, v1, rng.uniform(0.06, 0.09)))
        nx, ny = int(rng.integers(3, 7)), int(rng.integers(3, 7))
        g = rng.uniform(0.09, 0.13)
        for a in range(nx):
            for b in range(ny):
                cu, cv = u0 + a * w / nx, v0 + b * h / ny
                r.append((cu + 0.04 * w / nx, cv + 0.04 * h / ny, cu + 0.96 * w / nx, cv + 0.96 * h / ny, g))
    elif rodzaj == "plyny":  # beczki: wypełnienie + ścianki + obręcze
        n = int(rng.integers(2, 4))
        f = rng.uniform(0.22, 0.28)
        for a in range(n):
            b0, b1 = u0 + a * w / n + 0.03 * w / n, u0 + (a + 1) * w / n - 0.03 * w / n
            r.append((b0, v0, b1, v1, f))
            r.append((b0, v0, b0 + 0.08 * (b1 - b0), v1, 0.2))
            r.append((b1 - 0.08 * (b1 - b0), v0, b1, v1, 0.2))
            for t in (0.0, 0.48, 0.94):
                r.append((b0, v0 + t * h, b1, v0 + (t + 0.06) * h, 0.15))
    elif rodzaj == "sypkie":  # worki typu big-bag
        f = rng.uniform(0.20, 0.26)
        r.append((u0, v0 + 0.12 * h, u1, v1, f))
        r.append((u0 + 0.15 * w, v0, u1 - 0.15 * w, v0 + 0.12 * h, 0.7 * f))
    elif rodzaj == "maszyny":  # korpus + gęste podzespoły
        r.append((u0, v0 + 0.1 * h, u1, v1, rng.uniform(0.12, 0.2)))
        for _ in range(int(rng.integers(3, 7))):
            fw, fh = rng.uniform(0.15, 0.4), rng.uniform(0.15, 0.4)
            a0, b0 = u0 + rng.uniform(0, 1 - fw) * w, v0 + 0.1 * h + rng.uniform(0, 0.9 - fh) * h
            r.append((a0, b0, a0 + fw * w, b0 + fh * h, rng.uniform(0.35, 0.7)))
    elif rodzaj == "meble":  # duże lekkie bryły z płytami
        r.append((u0, v0, u1, v1, rng.uniform(0.05, 0.08)))
        r.append((u0, v0, u0 + 0.04 * w, v1, 0.18))
        r.append((u1 - 0.04 * w, v0, u1, v1, 0.18))
        for _ in range(int(rng.integers(2, 5))):
            t = rng.uniform(0.1, 0.9)
            r.append((u0, v0 + t * h, u1, v0 + t * h + 0.03 * h, 0.18))
    return [tuple(float(x) for x in e) for e in r]


ROZMIAR = {  # szerokość, (wysokość min, max), warstw max, luka
    "drobnica": ((0.045, 0.06), (0.18, 0.28), 2, (0.003, 0.01)),
    "plyny": ((0.05, 0.06), (0.22, 0.26), 2, (0.003, 0.01)),
    "sypkie": ((0.07, 0.09), (0.30, 0.40), 1, (0.004, 0.012)),
    "maszyny": ((0.08, 0.15), (0.20, 0.40), 1, (0.03, 0.08)),
    "meble": ((0.06, 0.10), (0.30, 0.50), 1, (0.003, 0.01)),
}


def zaladunek(rng, rodzaj, p):
    """Ułożenie towaru: lista palet {u0, u1, prost: [...], skrzynie: [...]} we wsp. naczepy."""
    if rodzaj == "pusta":
        return []
    (sw0, sw1), (h0, h1), wmax, (l0, l1) = ROZMIAR[rodzaj]
    palety, u = [], 0.03
    while u < 0.93:
        szer = rng.uniform(sw0, sw1)
        if u + szer > 0.975:
            break
        if rng.random() < 0.15:
            u += szer
            continue
        prost, skrzynie, v_d = [], [], p["podloga_v"] - 0.012
        for _ in range(int(rng.integers(1, wmax + 1))):
            wys = rng.uniform(h0, h1)
            if v_d - wys < 0.15:
                break
            prost += element(rodzaj, rng, u, v_d - wys, u + szer, v_d)
            skrzynie.append((u, v_d - wys, u + szer, v_d))
            v_d -= wys
        palety.append({"u0": u, "u1": u + szer, "prost": prost, "skrzynie": skrzynie})
        u += szer + rng.uniform(l0, l1)
    return palety


def rysuj_naczepe(pl, p, palety_towaru, jitter_palet):
    """Konstrukcja + towar. Zwraca prostokąty skrzyń w pikselach i we wsp. naczepy."""
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
    if p["slupki"]:
        for u0 in (0.012, 0.25, 0.5, 0.75, 0.976):
            pl.prost(u0, 0.10, u0 + 0.008, p["podloga_v"], 0.5)
    if p["agregat"]:
        pl.prost(-0.035, 0.14, 0.0, 0.42, 1.1)
        pl.prost(-0.03, 0.18, -0.006, 0.38, 0.6)
    r0, r1 = p["rama_v"]
    pl.prost(0.0, r0, 1.0, r0 + 0.012, 1.0)
    pl.prost(0.0, r1 - 0.012, 1.0, r1, 1.0)
    u = 0.03
    while u < 0.97:
        pl.prost(u, r0, u + 0.006, r1, 0.7)
        u += p["poprzeczki_co"]
    pl.prost(0.03, r0 - 0.005, 0.06, r1 + 0.01, 1.4)            # płyta sworznia
    pl.prost(p["podpora_u"], r1, p["podpora_u"] + 0.008, 0.92, 0.9)
    for os_u in p["osie"]:
        pl.prost(os_u - 0.02, r1, os_u + 0.02, r1 + 0.02, 1.2)
        pl.kolo(os_u, 0.875, 0.09, 0.9, r_wew=0.04, val_wew=1.5)
    skrzynie_px, skrzynie_uv = [], []
    for i, pal in enumerate(palety_towaru):
        du = jitter_palet[i]
        pl.prost(pal["u0"] + du, p["podloga_v"] - 0.012, pal["u1"] + du, p["podloga_v"], 0.45)
        for (a, b, c, d, val) in pal["prost"]:
            pl.prost(a + du, b, c + du, d, val)
        for (a, b, c, d) in pal["skrzynie"]:
            skrzynie_px.append(pl.px(a + du, b) + pl.px(c + du, d))
            skrzynie_uv.append((a + du, b, c + du, d))
    return skrzynie_px, skrzynie_uv


def paczki(pl, x0, y0, x1, y1, val):
    """Dodatek jako ułożone paczki (np. papierosy): siatka małych prostokątów + tło."""
    pl.prost_px(x0, y0, x1, y1, val * 0.4)
    bok = max(3.0, min(x1 - x0, y1 - y0) / 2)
    nx, ny = max(1, int((x1 - x0) / bok)), max(1, min(6, int((y1 - y0) / bok)))
    sx, sy = (x1 - x0) / nx, (y1 - y0) / ny
    for a in range(nx):
        for b in range(ny):
            pl.prost_px(x0 + (a + 0.1) * sx, y0 + (b + 0.1) * sy, x0 + (a + 0.9) * sx, y0 + (b + 0.9) * sy, val * 0.6)


def dodaj(pl, p, rodzaj, rng, skrzynie, kontrast, towar):
    """Rysuje jeden dodatek; zwraca ramkę prawdy [x, y, w, h] w pikselach."""
    val = kontrast * rng.uniform(0.8, 1.2)
    if rodzaj in WYMAGA_TOWARU and not skrzynie[0]:
        rodzaj = "podwojna_podloga"
    if rodzaj == "podwojna_podloga":
        u0 = rng.uniform(0.08, 0.7)
        x0, y0 = pl.px(u0, p["podloga_v"] - p["podloga_t"] * 0.7)
        x1, y1 = pl.px(u0 + rng.uniform(0.06, 0.2), p["podloga_v"])
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
    elif rodzaj == "jak_towar":
        # dodatkowa jednostka towaru tego samego rodzaju na szczycie stosu (atak 3 z 05)
        a, b, c, d = skrzynie[1][int(rng.integers(len(skrzynie[1])))]
        top = min(bb for (aa, bb, cc, dd) in skrzynie[1] if aa < c and cc > a)
        hh = min(rng.uniform(0.08, 0.14), top - 0.11)
        if hh < 0.03:
            return dodaj(pl, p, "w_towarze", rng, skrzynie, kontrast, towar)
        for (e0, e1, e2, e3, v) in element(towar, rng, a, top - hh, c, top):
            pl.prost(e0, e1, e2, e3, v)
        x0, y0 = pl.px(a, top - hh)
        x1, y1 = pl.px(c, top)
        return rodzaj, [int(math.floor(x0)), int(math.floor(y0)), int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))]
    else:  # w_towarze
        bx0, by0, bx1, by1 = skrzynie[0][int(rng.integers(len(skrzynie[0])))]
        fw, fh = rng.uniform(0.3, 0.6), rng.uniform(0.3, 0.6)
        x0 = bx0 + rng.uniform(0, 1 - fw) * (bx1 - bx0)
        y0 = by0 + rng.uniform(0, 1 - fh) * (by1 - by0)
        x1, y1 = x0 + fw * (bx1 - bx0), y0 + fh * (by1 - by0)
    paczki(pl, x0, y0, x1, y1, val)
    return rodzaj, [int(math.floor(x0)), int(math.floor(y0)), int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))]


def obraz(w, h, p, palety, towar, rng, dodatki_rodzaje, kontrast, zakl=1.0):
    geo = {"x0": 0.08 * w, "y0": 0.0, "L": 0.84 * w, "Hh": 0.97 * h,
           "sx": 1 + rng.uniform(-0.015, 0.015) * zakl, "dx": rng.normal(0, 0.004 * w * zakl),
           "dy": rng.normal(0, 0.003 * h * zakl)}
    pl = Plotno(w, h, geo)
    jit = rng.normal(0, 0.0015 * zakl, size=len(palety))
    skrzynie = rysuj_naczepe(pl, p, palety, jit)
    ramki = []
    for r in dodatki_rodzaje:
        rr, ramka = dodaj(pl, p, r, rng, skrzynie, kontrast, towar)
        ramki.append({"rodzaj": rr, "ramka": ramka})
    gain = rng.uniform(0.97, 1.03)
    I = np.exp(-pl.T * gain)
    I = I + rng.normal(0, 1, I.shape).astype(np.float32) * (0.004 + 0.012 * np.sqrt(I)) * zakl
    I = I * (1 + rng.normal(0, 0.004 * zakl, (h, 1)).astype(np.float32)) * (1 + rng.normal(0, 0.002 * zakl, (1, w)).astype(np.float32))
    pix = np.clip(8 + 240 * I, 0, 255).astype(np.uint8)
    return pix, ramki, {k: float(v) for k, v in geo.items()}


def zapisz_bmp(pix, sciezka, bity):
    im = Image.fromarray(pix, "L")
    if bity == 24:
        im = im.convert("RGB")
    im.save(sciezka, format="BMP")


def losuj_dodatki(rng, z_towarem):
    n = int(rng.integers(1, 3))
    mozliwe = [r for r in RODZAJE_DODATKOW if z_towarem or r not in WYMAGA_TOWARU]
    return [str(x) for x in rng.choice(mozliwe, size=n, replace=False)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wyjscie", required=True)
    ap.add_argument("--wariant", choices=("ta_sama", "pusta", "biblioteka"), default="ta_sama")
    ap.add_argument("--grupy", type=int, default=12)
    ap.add_argument("--nauka", type=int, default=4, help="ta_sama/pusta: czystych do nauki na grupę")
    ap.add_argument("--biblioteka", type=int, default=4, help="biblioteka: pustych wzorców na typ")
    ap.add_argument("--nauka-towaru", type=int, default=3, help="biblioteka: czystych załadowanych na rodzaj towaru")
    ap.add_argument("--czyste", type=int, default=2, help="czystych obrazów testowych na grupę")
    ap.add_argument("--z-dodatkami", type=int, default=3, help="obrazów z dodatkami na grupę")
    ap.add_argument("--skala", type=float, default=0.25, help="1.0 = 7300x2300 (≈50 MB przy 24 bitach)")
    ap.add_argument("--bity", type=int, choices=(8, 24), default=8)
    ap.add_argument("--kontrast", type=float, default=0.35, help="tłumienie dodatku (mniej = trudniej)")
    ap.add_argument("--trudny", action="store_true", help="kontrast x0.65, zakłócenia x2 (KA8)")
    ap.add_argument("--ziarno", type=int, default=15)
    a = ap.parse_args()
    zakl = 2.0 if a.trudny else 1.0
    kontrast = a.kontrast * (0.65 if a.trudny else 1.0)

    w, h = int(round(PELNY_W * a.skala)), int(round(PELNY_H * a.skala))
    kat = os.path.join(a.wyjscie, "obrazy")
    os.makedirs(kat, exist_ok=True)
    rng_g = np.random.default_rng(a.ziarno)
    wpisy = []
    t0 = time.time()

    def zrob(nazwa, p, palety, towar, rng, rodzaje, **pola):
        pix, ramki, geo = obraz(w, h, p, palety, towar, rng, rodzaje, kontrast, zakl)
        zapisz_bmp(pix, os.path.join(kat, nazwa), a.bity)
        wpisy.append({"plik": nazwa, "typ": p["typ"], "dodatki": ramki, "geometria": geo,
                      "towar_zgloszony": towar, **pola})

    if a.wariant == "biblioteka":
        for typ in TYPY:  # biblioteka pustych wzorców
            p = projekt_typu(typ)
            for i in range(a.biblioteka):
                zrob(f"W-{typ}_{i:02d}.bmp", p, [], "pusta", np.random.default_rng([a.ziarno, 1, TYPY.index(typ), i]), [],
                     grupa=f"W-{typ}", rola="biblioteka", w_bibliotece=True)
        for k, towar in enumerate(TOWARY):  # nauka towaru: czyste załadowane
            for i in range(a.nauka_towaru):
                rng = np.random.default_rng([a.ziarno, 2, k, i])
                typ = TYPY[int(rng.integers(len(TYPY)))]
                p = projekt_typu(typ)
                zrob(f"T-{towar}_{i:02d}_{typ}.bmp", p, zaladunek(rng, towar, p), towar, rng, [],
                     grupa=f"T-{towar}", rola="nauka_towaru", w_bibliotece=True)
        for g in range(a.grupy):  # badane: ten sam załadunek bez i z dodatkami
            typ = TYP_SPOZA if g % 6 == 5 else TYPY[g % 3]
            p = projekt_typu(typ)
            seed_g = int(rng_g.integers(1 << 31))
            rng0 = np.random.default_rng(seed_g)
            towar = "pusta" if rng0.random() < 1 / 3 else str(rng0.choice(TOWARY))
            palety = zaladunek(rng0, towar, p)
            role = ["czysty"] * a.czyste + ["dodatki"] * a.z_dodatkami
            for i, rola in enumerate(role):
                rng = np.random.default_rng([seed_g, i])
                rodzaje = losuj_dodatki(rng, towar != "pusta") if rola == "dodatki" else []
                zrob(f"g{g:03d}_{typ}_{towar}_{i:02d}_{rola}.bmp", p, palety, towar, rng, rodzaje,
                     grupa=f"g{g:03d}", rola=rola, w_bibliotece=typ in TYPY)
    else:
        for g in range(a.grupy):
            typ = TYPY[g % len(TYPY)]
            seed_g = int(rng_g.integers(1 << 31))
            p = projekt_typu(typ, ziarno=seed_g)  # każda grupa — inny egzemplarz
            rng0 = np.random.default_rng(seed_g)
            towar = str(rng0.choice(TOWARY))
            palety = zaladunek(rng0, towar, p)
            role = ["nauka"] * a.nauka + ["czysty"] * a.czyste + ["dodatki"] * a.z_dodatkami
            wzorzec = f"g{g:03d}_{typ}_00_nauka.bmp"
            for i, rola in enumerate(role):
                rng = np.random.default_rng([seed_g, i])
                z_towarem = True
                if a.wariant == "pusta":
                    z_towarem = rola != "nauka" and (i - a.nauka) % 3 != 0
                rodzaje = losuj_dodatki(rng, z_towarem) if rola == "dodatki" else []
                zrob(f"g{g:03d}_{typ}_{i:02d}_{rola}.bmp", p, palety if z_towarem else [],
                     towar if z_towarem else "pusta", rng, rodzaje,
                     grupa=f"g{g:03d}", rola=rola, wzorzec=wzorzec, w_bibliotece=True)
    meta = {"szer": w, "wys": h, "bity": a.bity, "skala": a.skala, "kontrast": kontrast, "trudny": a.trudny,
            "ziarno": a.ziarno, "wariant": a.wariant, "biblioteka_typy": list(TYPY),
            "towary": list(TOWARY) + ["pusta"], "obrazy": wpisy}
    with open(os.path.join(a.wyjscie, "etykiety.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    mb = os.path.getsize(os.path.join(kat, wpisy[0]["plik"])) / 1e6
    print(f"wygenerowano {len(wpisy)} obrazów {w}x{h} {a.bity} bit ({mb:.1f} MB/obraz) w {time.time()-t0:.1f} s -> {a.wyjscie}")


if __name__ == "__main__":
    main()

# <!-- skill: dummy-dataset -->
