"""Silnik MVP: biblioteka wzorców + analiza jednego obrazu (karta, torch/CUDA).

Używany przez usługę (rtg.usluga) i tryb partiami (rtg.wykryj bez etykiet).
Metoda: H2 „nauka” (średnia/rozrzut pustych naczep typu) — w sondach mniej FN niż H1.
Wzorzec dobiera system: typ z biblioteki o najlepszym NCC pasa podłoga–rama–koła (P19);
„wzorzec niepewny”, gdy NCC poniżej progu z biblioteki (P11, P25).
Wybór towaru (P29) gasi tylko komórki we WNĘTRZU przestrzeni ładunkowej — bez dachu, podłogi
i ściany przedniej (wniosek 2 z sond, Z5); „pusta” i „nie wiem” nic nie gaszą (P34).
Wynik: wszystkie miejsca (najpewniejsze pierwsze) z listą towarów, które je gaszą — ekran sam
liczy „wygaszone: N” i „+N dalszych miejsc” (P21, P28, P35).
"""
import io
import json
import os
import time
from collections import defaultdict

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from rtg import wykryj as W

Image.MAX_IMAGE_PIXELS = None
TOWARY = ("drobnica", "plyny", "sypkie", "maszyny", "meble")
# strefy w układzie naczepy wzorca: u = wzdłuż (0 przód), v = w pionie (0 dach) — generator projekt_typu/dodaj
WNETRZE_U = (0.035, 0.975)   # bez ściany przedniej (u < 0.03) i tylnych drzwi
WNETRZE_V = (0.14, 0.655)    # bez dachu (v < 0.13) i podłogi (v ≥ 0.66)
PODLOGA_V = (0.655, 0.775)


def _uv(geo, x, y):
    cx = geo["x0"] + geo["L"] / 2
    u = ((x - geo["dx"] - cx) / geo["sx"] + cx - geo["x0"]) / geo["L"]
    v = (y - geo["dy"] - geo["y0"]) / geo["Hh"]
    return u, v


def gdzie(geo, x, y, w, h):
    """Opis miejsca po środku ramki (układ wzorca) i czy to podłoga (P26)."""
    u, v = _uv(geo, x + w / 2, y + h / 2)
    czesc = "przód" if u < 0.33 else ("środek" if u < 0.66 else "tył")
    if v < 0.135:
        return f"dach, {czesc}", False
    if u < 0.035:
        return "ściana przednia", False
    if PODLOGA_V[0] <= v < PODLOGA_V[1]:
        return f"podłoga, {czesc}", True
    if PODLOGA_V[1] <= v < 0.88:
        return f"rama, {czesc}", False
    if v >= 0.88:
        return f"podwozie, {czesc}", False
    return f"przestrzeń ładunkowa, {czesc}", False


def pewnosc(r):
    """Stosunek punktacji do progu (≥ 1) → skala 0–100% na ekran: 1,0 → 30%, 1,4 → 50%, 3,5 → 80%."""
    return round(max(0.0, min(0.99, 1 - 0.7 / max(r, 1e-6))), 3)


class Silnik:
    def __init__(self, katalog, roboczy=1800, k=5, zapas=1.1):
        if not torch.cuda.is_available():
            raise SystemExit("BRAK KARTY: torch.cuda.is_available() == False — nie liczę na procesorze")
        W.DEV = torch.device("cuda")
        W.PAS = W.PAS_DOBORU
        self.kat = katalog
        self.roboczy, self.k = roboczy, k
        meta = json.load(open(os.path.join(katalog, "etykiety.json")))
        self.meta = meta
        t0 = time.time()
        bib = defaultdict(list)
        for o in meta["obrazy"]:
            if o["rola"] == "biblioteka":
                bib[o["typ"]].append(o)
        self.modele, self.geo, self.plik_wzorca = {}, {}, {}
        sk = {}
        for typ, obr in sorted(bib.items()):
            A = [self._wczytaj_plik(o["plik"]) for o in obr]
            m = W.Nauka(A, k, zapas)
            self.modele[typ] = m
            self.geo[typ] = obr[0]["geometria"]
            self.plik_wzorca[typ] = obr[0]["plik"]
            sk[typ] = A
        self.ksztalt = next(iter(self.modele.values())).R.shape
        swoje, obce = [], []
        for typ, m in self.modele.items():
            for A in sk[typ][1:]:
                swoje.append(W.wyrownaj(m.R, A, zwroc_ncc=True)[1])
            for typ2, m2 in self.modele.items():
                if typ2 != typ:
                    obce.append(W.wyrownaj(m2.R, sk[typ][0], zwroc_ncc=True)[1])
        self.prog_ncc = (min(swoje) + max(obce)) / 2 if min(swoje) > max(obce) else 0.98 * min(swoje)
        del sk
        self.obw = {}
        for o in meta["obrazy"]:
            if o["rola"] != "nauka_towaru":
                continue
            A = self._wczytaj_plik(o["plik"])
            m = self.modele[o["typ"]]
            e, s = W.cechy_komorek(m.surowa(W.wyrownaj(m.R, A)))
            st = self._wnetrze(o["typ"], e.shape)
            E, S = float(e[st].max()), float(s[st].max())
            p = self.obw.get(o["towar_zgloszony"], (0.0, 0.0))
            self.obw[o["towar_zgloszony"]] = (max(p[0], E), max(p[1], S))
        torch.cuda.synchronize()
        self.budowa_s = round(time.time() - t0, 2)

    # --- wczytanie: każdy obraz sprowadzony do rozmiaru wzorców biblioteki ---
    def _tlumienie(self, im):
        im = im.convert("L")
        x = torch.from_numpy(np.asarray(im, dtype=np.uint8).copy()).to(W.DEV).float()
        x = ((x - 8) / 240).clamp(0.01, 1.0)
        A = -torch.log(x)[None, None]
        f = max(1, round(im.size[0] / self.roboczy))
        if f > 1:
            A = F.avg_pool2d(A, f)
        return A

    def _wczytaj_plik(self, plik):
        return self._tlumienie(Image.open(os.path.join(self.kat, "obrazy", plik)))[0, 0]

    def _wnetrze(self, typ, shape_kom):
        g = self.geo[typ]
        hk, wk = shape_kom
        ys = (torch.arange(hk, device=W.DEV, dtype=torch.float32) + 0.5) * W.KOMORKA
        xs = (torch.arange(wk, device=W.DEV, dtype=torch.float32) + 0.5) * W.KOMORKA
        cx = g["x0"] + g["L"] / 2
        u = ((xs - g["dx"] - cx) / g["sx"] + cx - g["x0"]) / g["L"]
        v = (ys - g["dy"] - g["y0"]) / g["Hh"]
        mv = (v >= WNETRZE_V[0]) & (v < WNETRZE_V[1])
        mu = (u >= WNETRZE_U[0]) & (u < WNETRZE_U[1])
        return mv[:, None] & mu[None, :]

    def analizuj(self, im):
        """im: PIL.Image (bmp/png/jpg dowolnego rozmiaru). Zwraca dict + podgląd PNG (bajty)."""
        t0 = time.time()
        Wo, Ho = im.size
        A = self._tlumienie(im)
        h, w = self.ksztalt
        if A.shape[-2:] != (h, w):
            A = F.interpolate(A, size=(h, w), mode="bilinear", align_corners=False)
        A = A[0, 0]
        best = None
        for typ, m in self.modele.items():
            Aal, ncc = W.wyrownaj(m.R, A, zwroc_ncc=True)
            if best is None or ncc > best[0]:
                best = (ncc, typ, Aal)
        ncc, typ, Aal = best
        m = self.modele[typ]
        score = m.ocen(Aal)
        r = W.ramki(score, m.prog, self.k, 1, (w, h))
        # które towary gaszą które miejsca: ≥ 50% komórek ramki zgodnych z obwiednią towaru we wnętrzu
        e, s = W.cechy_komorek(m.surowa(Aal))
        wn = self._wnetrze(typ, e.shape)
        zg = {t: ((e <= 1.05 * E) & (s <= 1.05 * S) & wn) for t, (E, S) in self.obw.items()}
        sx, sy = Wo / w, Ho / h
        miejsca = []
        for i, (x, y, bw, bh, rr) in enumerate(r):
            k0x, k0y = x // W.KOMORKA, y // W.KOMORKA
            k1x, k1y = (x + bw - 1) // W.KOMORKA + 1, (y + bh - 1) // W.KOMORKA + 1
            gasi = [t for t, z in zg.items() if float(z[k0y:k1y, k0x:k1x].float().mean()) >= 0.5]
            opis, podloga = gdzie(self.geo[typ], x, y, bw, bh)
            miejsca.append({"x": round(x * sx), "y": round(y * sy), "w": round(bw * sx), "h": round(bh * sy),
                            "ocena": pewnosc(rr), "punktacja": rr, "gdzie": opis, "podloga": podloga, "gasi": gasi})
        miejsca.sort(key=lambda q: -q["ocena"])
        for i, q in enumerate(miejsca):
            q["id"] = i + 1
        torch.cuda.synchronize()
        czas = round(time.time() - t0, 3)
        # podgląd badanego: obraz w skali szarości + czerwień tam, gdzie różnica powyżej połowy progu
        g = Image.fromarray(np.asarray(im.convert("L").resize((w, h), Image.BILINEAR)))
        heat = (score / m.prog).clamp(0, 2).sub(0.5).clamp_min(0).div(1.5).cpu().numpy()
        base = np.asarray(g, dtype=np.float32)
        rgb = np.stack([np.minimum(255, base + 160 * heat), base * (1 - 0.5 * heat), base * (1 - 0.5 * heat)], -1)
        buf = io.BytesIO()
        Image.fromarray(rgb.astype(np.uint8)).save(buf, "PNG", optimize=False)
        return {"wzorzec": f"W-{typ}", "typ": typ, "niepewny": bool(ncc < self.prog_ncc), "ncc": round(ncc, 4),
                "prog_ncc": round(self.prog_ncc, 4), "rozmiar": [Wo, Ho], "miejsca": miejsca, "czas_s": czas,
                "towary_gaszace": sorted(self.obw), "pamiec_karty_MB": round(torch.cuda.max_memory_allocated() / 1e6)}, buf.getvalue()

    def podglad_wzorca(self, typ):
        h, w = self.ksztalt
        im = Image.open(os.path.join(self.kat, "obrazy", self.plik_wzorca[typ])).convert("L").resize((w, h))
        buf = io.BytesIO()
        im.save(buf, "PNG")
        return buf.getvalue()


def partie(katalog, biblioteka, wyjscie):
    """Tryb partiami (§8): każdy .bmp/.png/.jpg z katalogu → JSON z ramkami i pewnością + PNG z zaznaczeniem.
    Towar „nie wiem” — nic nie wygaszane; na liście ≤ 5 + licznik „dalsze”."""
    from PIL import ImageDraw
    s = Silnik(biblioteka)
    os.makedirs(wyjscie, exist_ok=True)
    zbior = {}
    for plik in sorted(os.listdir(katalog)):
        if not plik.lower().endswith((".bmp", ".png", ".jpg", ".jpeg")):
            continue
        im = Image.open(os.path.join(katalog, plik))
        w, png = s.analizuj(im)
        m = w["miejsca"]
        w.update({"plik": plik, "towar": "nie_wiem", "lista": m[:5], "dalsze": max(0, len(m) - 5)})
        pod = Image.open(io.BytesIO(png)).convert("RGB")
        d = ImageDraw.Draw(pod)
        fx, fy = pod.width / w["rozmiar"][0], pod.height / w["rozmiar"][1]
        for q in m[:5]:
            d.rectangle([q["x"] * fx - 3, q["y"] * fy - 3, (q["x"] + q["w"]) * fx + 3, (q["y"] + q["h"]) * fy + 3], outline=(255, 140, 0), width=3)
            d.text((q["x"] * fx, max(0, q["y"] * fy - 14)), str(q["id"]), fill=(255, 140, 0))
        baza = os.path.splitext(plik)[0]
        pod.save(os.path.join(wyjscie, baza + "_zaznaczenia.png"))
        json.dump(w, open(os.path.join(wyjscie, baza + ".json"), "w"), ensure_ascii=False, indent=1)
        zbior[plik] = {"ramki": [[q["x"], q["y"], q["w"], q["h"], q["punktacja"]] for q in m], "wzorzec": w["wzorzec"], "wzorzec_typ": w["typ"],
                       "niepewny": w["niepewny"], "czas_s": w["czas_s"]}
        print(plik, w["wzorzec"], "niepewny" if w["niepewny"] else "", len(m), "miejsc", w["czas_s"], "s", flush=True)
    json.dump({"towar": "nie_wiem", "obrazy": zbior}, open(os.path.join(wyjscie, "wyniki.json"), "w"), ensure_ascii=False, indent=1)
    print("partie:", len(zbior), "obrazów ->", wyjscie)
