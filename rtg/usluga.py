"""Usługa analizy na karcie OMENa (HTTP, port 8770) — wynik dla aplikacji na ksefbot.pl.

  python -m rtg.usluga --biblioteka ~/dane/rtg/bib --port 8770 --bezczynnosc 120

GET  /zdrowie               stan, karta, czas budowy biblioteki
GET  /auta                  dwa auta pokazu (A z dodatkiem, B czyste) — wybrane z prawdziwych wyników (P18)
POST /analiza?auto=A|B      analiza auta pokazu
POST /analiza?nazwa=plik    analiza wczytanego pliku (.bmp/.png/.jpg w treści żądania) (P27, P31)
GET  /podglad/<id>.png      badany obraz z podświetloną różnicą
GET  /wzorzec/<typ>.png     użyty wzorzec (pusta naczepa z biblioteki)
Usługa kończy się sama po --bezczynnosc minutach bez żądań (nie trzyma karty, gdy nikt nie pyta).
"""
import argparse
import io
import json
import os
import threading
import time
import uuid
from collections import OrderedDict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import torch
from PIL import Image

from rtg.silnik import Silnik

LOCK = threading.Lock()
PODGLADY = OrderedDict()
STAN = {"ostatnie": time.time()}
MAX_MB = 120


def iou_pola(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0, min(ay + ah, by + bh) - max(ay, by))
    return ix * iy / max(1, min(aw * ah, bw * bh))


def wybierz_auta(s, plik_cache):
    """Auto A: z dodatkiem w podłodze, ≥ 6 miejsc (pokaz „+N”), dodatek w podłodze trafiony.
    Auto B: czyste z biblioteki, 0 miejsc przy „nie wiem” (P17). Wybór zapisany, żeby restart był szybki."""
    if os.path.exists(plik_cache):
        return json.load(open(plik_cache))
    A = B = None
    for o in s.meta["obrazy"]:
        if not o.get("w_bibliotece") or o["rola"] not in ("czysty", "dodatki"):
            continue
        if o["rola"] == "czysty" and B:
            continue
        if o["rola"] == "dodatki" and (A or not any(d["rodzaj"] == "podwojna_podloga" for d in o["dodatki"])):
            continue
        im = Image.open(os.path.join(s.kat, "obrazy", o["plik"]))
        w, _ = s.analizuj(im)
        m = w["miejsca"]
        if o["rola"] == "czysty" and not m and not w["niepewny"]:
            B = o
        if o["rola"] == "dodatki" and len(m) >= 6:
            pod = [d["ramka"] for d in o["dodatki"] if d["rodzaj"] == "podwojna_podloga"]
            if any(q["podloga"] and any(iou_pola([q["x"], q["y"], q["w"], q["h"]], p) >= 0.3 for p in pod) for q in m):
                A = o
        if A and B:
            break
    wyb = {}
    for k, o, nazwa in (("A", A, "Auto A — z dodatkiem"), ("B", B, "Auto B — czyste")):
        if o:
            wyb[k] = {"plik": o["plik"], "nazwa": nazwa, "typ": o["typ"], "towar_zgloszony": o["towar_zgloszony"],
                      "nr": f"SYN {abs(hash(o['plik'])) % 90000 + 10000}", "prawda": o["dodatki"]}
    json.dump(wyb, open(plik_cache, "w"), ensure_ascii=False, indent=1)
    return wyb


class Obsluga(BaseHTTPRequestHandler):
    s = None
    auta = {}

    def log_message(self, fmt, *args):
        print(time.strftime("%H:%M:%S"), self.address_string(), fmt % args, flush=True)

    def _odp(self, kod, tresc, typ="application/json; charset=utf-8"):
        if isinstance(tresc, (dict, list)):
            tresc = json.dumps(tresc, ensure_ascii=False).encode()
        self.send_response(kod)
        self.send_header("Content-Type", typ)
        self.send_header("Content-Length", str(len(tresc)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(tresc)

    def do_GET(self):
        STAN["ostatnie"] = time.time()
        p = urlparse(self.path).path
        if p == "/zdrowie":
            return self._odp(200, {"ok": True, "karta": torch.cuda.get_device_name(0), "budowa_s": self.s.budowa_s,
                                   "typy": sorted(self.s.modele), "towary_gaszace": sorted(self.s.obw),
                                   "auta": sorted(self.auta)})
        if p == "/auta":
            return self._odp(200, {k: {kk: v[kk] for kk in ("nazwa", "typ", "nr", "towar_zgloszony")}
                                   for k, v in self.auta.items()})
        if p.startswith("/podglad/") and p.endswith(".png"):
            b = PODGLADY.get(p[9:-4])
            return self._odp(200, b, "image/png") if b else self._odp(404, {"blad": "brak podglądu"})
        if p.startswith("/wzorzec/") and p.endswith(".png"):
            typ = p[9:-4]
            if typ in self.s.modele:
                return self._odp(200, self.s.podglad_wzorca(typ), "image/png")
        return self._odp(404, {"blad": "nie ma"})

    def do_POST(self):
        STAN["ostatnie"] = time.time()
        u = urlparse(self.path)
        if u.path != "/analiza":
            return self._odp(404, {"blad": "nie ma"})
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_MB * 1e6:
            return self._odp(413, {"blad": f"plik większy niż {MAX_MB} MB"})
        body = self.rfile.read(n) if n else b""
        try:
            if q.get("auto") in self.auta:
                a = self.auta[q["auto"]]
                im = Image.open(os.path.join(self.s.kat, "obrazy", a["plik"]))
                nazwa = a["plik"]
            else:
                if not body:
                    return self._odp(400, {"blad": "brak pliku"})
                im = Image.open(io.BytesIO(body))
                im.load()
                nazwa = q.get("nazwa", "plik")
        except Exception as e:  # noqa: BLE001
            return self._odp(400, {"blad": f"nie umiem odczytać obrazu: {e}"})
        with LOCK:
            torch.cuda.reset_peak_memory_stats()
            wynik, png = self.s.analizuj(im)
        pid = uuid.uuid4().hex[:12]
        PODGLADY[pid] = png
        while len(PODGLADY) > 30:
            PODGLADY.popitem(last=False)
        wynik.update({"id": pid, "nazwa": nazwa, "auto": q.get("auto"), "podglad": f"/podglad/{pid}.png",
                      "wzorzec_png": f"/wzorzec/{wynik['typ']}.png"})
        self._odp(200, wynik)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--biblioteka", default=os.path.expanduser("~/dane/rtg/bib"))
    ap.add_argument("--port", type=int, default=8770)
    ap.add_argument("--bezczynnosc", type=float, default=120, help="minut bez żądań, po których usługa kończy")
    a = ap.parse_args()
    t0 = time.time()
    s = Silnik(a.biblioteka)
    print("karta:", torch.cuda.get_device_name(0), "biblioteka", s.budowa_s, "s", "typy", sorted(s.modele),
          "towary", sorted(s.obw), "prog_ncc", round(s.prog_ncc, 4), flush=True)
    Obsluga.s = s
    Obsluga.auta = wybierz_auta(s, os.path.join(a.biblioteka, "auta_pokazu.json"))
    print("auta pokazu:", {k: v["plik"] for k, v in Obsluga.auta.items()}, "start", round(time.time() - t0, 1), "s", flush=True)
    srv = ThreadingHTTPServer(("0.0.0.0", a.port), Obsluga)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"usługa nasłuchuje na :{a.port}", flush=True)
    while time.time() - STAN["ostatnie"] < a.bezczynnosc * 60:
        time.sleep(5)
    print("koniec: bezczynność", a.bezczynnosc, "min", flush=True)
    srv.shutdown()


if __name__ == "__main__":
    main()
