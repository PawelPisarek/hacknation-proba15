"""O35: ocena FP/FN z plików JSON trybu partiami (silnik MVP) — „nie wiem” i towar zgłoszony (z pola gasi, P40).
  python skrypty/ocena_partii.py <katalog JSON partii> <katalog danych z etykiety.json> <wyjście>
Ramka = [x, y, w, h, punktacja/próg], jak oczekuje rtg.ocena."""
import glob
import json
import os
import sys

P, D, W = sys.argv[1:]
os.makedirs(W, exist_ok=True)
tow = {o["plik"]: o.get("towar_zgloszony", "pusta") for o in json.load(open(f"{D}/etykiety.json"))["obrazy"]}
for nazwa, filtr in (("nie_wiem", lambda q, p: True), ("zgloszony", lambda q, p: tow.get(p) not in q["gasi"])):
    z = {"towar": nazwa, "metoda": "MVP", "obrazy": {}}
    for f in glob.glob(f"{P}/*.json"):
        w = json.load(open(f))
        if "plik" not in w:
            continue
        z["obrazy"][w["plik"]] = {"ramki": [[q["x"], q["y"], q["w"], q["h"], q["punktacja"]] for q in w["miejsca"] if filtr(q, w["plik"])],
                                  "wzorzec": w["wzorzec"], "wzorzec_typ": w["typ"], "niepewny": w["niepewny"],
                                  "czas_s": w["czas_s"], "pamiec_karty_MB": w.get("pamiec_karty_MB")}
    json.dump(z, open(f"{W}/{nazwa}.json", "w"))
print("zapisano", W)
