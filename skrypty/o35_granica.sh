#!/bin/sh
# O35 po rozstrzygnięciu Szefa (granica wnętrza nie gaszona) — jeden przebieg na karcie, siatka marginesów:
#   H1: sama zgodność ramki z wnętrzem (margines 0) już obniża liczbę zgaszonych dodatków z 24/68;
#   H2: margines 0,03/0,05 → ≤ 5 zgaszonych dodatków, 0 w podłodze i dachu; FP rośnie o ≤ 15%;
#   H3: szerszy margines (0,05/0,08; 0,05/0,12) → 0 zgaszonych kosztem FP.
set -e
D=${D:-$HOME/dane/rtg/bib}; W=wyniki/o35; rm -rf $W; mkdir -p $W/we
ln -s $D/obrazy/* $W/we/
python -m rtg.wykryj --dane $W/we --biblioteka $D --wyjscie $W/partie > $W/partie.log
tail -1 $W/partie.log
python skrypty/ocena_partii.py $W/partie $D $W/ocena 0,0 0.03,0.05 0.05,0.08 0.05,0.12 > /dev/null
echo "== nie_wiem"; python -m rtg.ocena --dane $D --wyniki $W/ocena/nie_wiem.json
for f in $W/ocena/zgloszony_*.json; do echo "== $(basename $f .json)"; python -m rtg.ocena --dane $D --wyniki $f --bazowe $W/ocena/nie_wiem.json; done
python - $W/partie <<'EOF'
import glob, json, sys
m = [q for f in glob.glob(sys.argv[1] + "/*.json") if not f.endswith("wyniki.json") for q in json.load(open(f))["miejsca"]]
print("miejsca", len(m), "z gasi_wnetrze", sum(bool(q["gasi_wnetrze"]) for q in m), "gaszone przy domyślnym marginesie", sum(bool(q["gasi"]) for q in m), "granica", sum(q["granica"] for q in m))
EOF
