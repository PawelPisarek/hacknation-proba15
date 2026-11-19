#!/bin/sh
# Na karcie: zapis prawdziwych wyników aut pokazu do app/public/zapis/ (tryb awaryjny, pre-mortem),
# test podłogi auta A po każdym z 6 towarów + „nie wiem” (P26/P40) i tryb partiami na 4 obrazach.
set -e
export P=8772
Z=app/public/zapis; mkdir -p $Z
python -m rtg.usluga --biblioteka "$HOME/dane/rtg/bib" --port $P --bezczynnosc 1 > /tmp/usl_zapis.log 2>&1 &
PID=$!
for i in $(seq 1 120); do curl -s -m 2 localhost:$P/zdrowie >/dev/null 2>&1 && break; sleep 2; done
cat /tmp/usl_zapis.log
curl -s localhost:$P/auta > $Z/auta.json
for A in A B; do
  curl -s -X POST "localhost:$P/analiza?auto=$A" > $Z/$A.json
  python skrypty/zapis_auta.py $A $Z
done
kill $PID 2>/dev/null || true
rm -rf /tmp/partie_we && mkdir -p /tmp/partie_we && cp $(ls $HOME/dane/rtg/bib/obrazy/g00[0-1]_*.bmp | head -4) /tmp/partie_we/
python -m rtg.wykryj --dane /tmp/partie_we --wyjscie wyniki/partie
ls wyniki/partie
