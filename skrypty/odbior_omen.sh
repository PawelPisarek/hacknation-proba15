#!/bin/sh
# Odbiór MVP O34–O35 na karcie OMENa: tryb partiami (rtg.wykryj --dane) na zbiorze sond + ocena FP/FN silnikiem MVP
# (wygaszanie tylko wnętrza ładunku, P40) — „nie wiem” i towar zgłoszony (z pola gasi).
set -e
D=${D:-$HOME/dane/rtg/bib}; W=wyniki/odbior; rm -rf $W; mkdir -p $W/we
ln -s $D/obrazy/* $W/we/
python -m rtg.wykryj --dane $W/we --biblioteka $D --wyjscie $W/partie > $W/partie.log
tail -1 $W/partie.log
python - "$W" "$D" <<'EOF'
import glob, json, os, statistics, sys
W, D = sys.argv[1:]
meta = json.load(open(f"{D}/etykiety.json")); tow = {o["plik"]: o.get("towar_zgloszony", "pusta") for o in meta["obrazy"]}
zg = {"towar": "zgloszony", "metoda": "MVP", "obrazy": {}}
cz, pm = [], []
for f in glob.glob(f"{W}/partie/*.json"):
    if f.endswith("wyniki.json"): continue
    w = json.load(open(f)); p = w["plik"]
    zg["obrazy"][p] = {"ramki": [[q["x"], q["y"], q["w"], q["h"], q["ocena"]] for q in w["miejsca"] if tow.get(p) not in q["gasi"]],
                      "wzorzec": w["wzorzec"], "niepewny": w["niepewny"], "czas_s": w["czas_s"]}
    cz.append(w["czas_s"]); pm.append(w.get("pamiec_karty_MB", 0))
    assert len(w["lista"]) <= 5 and w["dalsze"] == max(0, len(w["miejsca"]) - 5)
json.dump(zg, open(f"{W}/zgloszony.json", "w"))
print(f"O34: {len(cz)} obrazów, JSON + _zaznaczenia.png na każdy, lista ≤ 5 + dalsze: tak; czas na obraz śr. {statistics.mean(cz):.2f} s, max {max(cz):.2f} s; karta max {max(pm)} MB")
EOF
ls $W/partie/*_zaznaczenia.png | wc -l
echo "== O35 nie wiem"; python -m rtg.ocena --dane $D --wyniki $W/partie/wyniki.json
echo "== O35 towar zgłoszony"; python -m rtg.ocena --dane $D --wyniki $W/zgloszony.json --bazowe $W/partie/wyniki.json
# 50 MB pełny rozmiar
python - <<'EOF'
import glob, time, torch
from PIL import Image
from rtg.silnik import Silnik
import os
s = Silnik(os.path.expanduser("~/dane/rtg/bib"))
for p in sorted(p for p in glob.glob(os.path.expanduser("~/dane/rtg/duzy/obrazy/*.bmp")) if "nauka" not in p):
    torch.cuda.reset_peak_memory_stats(); w, _ = s.analizuj(Image.open(p))
    print("O34 50 MB:", os.path.basename(p), w["rozmiar"], len(w["miejsca"]), "miejsc", w["czas_s"], "s", w["pamiec_karty_MB"], "MB")
EOF
