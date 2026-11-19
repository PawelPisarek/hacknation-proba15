"""O35: ocena FP/FN z plików JSON trybu partiami (silnik MVP) — „nie wiem” i towar zgłoszony (P40 + granica wnętrza).
  python skrypty/ocena_partii.py <katalog JSON partii> <katalog danych z etykiety.json> <wyjście> [mu,mv ...]
Ramka = [x, y, w, h, punktacja/próg], jak oczekuje rtg.ocena. Dla każdego marginesu mu,mv (część długości/wysokości
naczepy) zapisuje zgloszony_<mu>_<mv>.json: miejsce gaszone, gdy towar w gasi_wnetrze i ramka w środku zwężonego wnętrza."""
import glob
import json
import os
import sys

from rtg.silnik import w_srodku

P, D, W = sys.argv[1:4]
marginesy = [tuple(map(float, m.split(","))) for m in sys.argv[4:]] or [(0.0, 0.0), (0.03, 0.05)]
os.makedirs(W, exist_ok=True)
tow = {o["plik"]: o.get("towar_zgloszony", "pusta") for o in json.load(open(f"{D}/etykiety.json"))["obrazy"]}
obrazy = [json.load(open(f)) for f in glob.glob(f"{P}/*.json")]
obrazy = [w for w in obrazy if "plik" in w]
warianty = {"nie_wiem": lambda q, p: True}
for mu, mv in marginesy:
    warianty[f"zgloszony_{mu}_{mv}"] = (lambda mu, mv: lambda q, p: not (tow.get(p) in q["gasi_wnetrze"] and w_srodku(q["uv"], mu, mv)))(mu, mv)
for nazwa, zostaje in warianty.items():
    z = {"towar": nazwa, "metoda": "MVP", "obrazy": {}}
    for w in obrazy:
        z["obrazy"][w["plik"]] = {"ramki": [[q["x"], q["y"], q["w"], q["h"], q["punktacja"]] for q in w["miejsca"] if zostaje(q, w["plik"])],
                                  "wzorzec": w["wzorzec"], "wzorzec_typ": w["typ"], "niepewny": w["niepewny"],
                                  "czas_s": w["czas_s"], "pamiec_karty_MB": w.get("pamiec_karty_MB")}
    json.dump(z, open(f"{W}/{nazwa}.json", "w"))
    print(nazwa)
