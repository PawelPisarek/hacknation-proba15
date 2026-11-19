#!/bin/sh
# Test dymny usługi na karcie: start, /zdrowie, analiza aut A i B, własny plik (PNG), koniec.
set -e
P=${P:-8771}
python -m rtg.usluga --biblioteka "$HOME/dane/rtg/bib" --port $P --bezczynnosc 1 > /tmp/usluga_test.log 2>&1 &
PID=$!
for i in $(seq 1 120); do curl -s -m 2 localhost:$P/zdrowie > /dev/null 2>&1 && break; sleep 2; kill -0 $PID 2>/dev/null || { cat /tmp/usluga_test.log; exit 1; }; done
cat /tmp/usluga_test.log
curl -s localhost:$P/zdrowie; echo
curl -s localhost:$P/auta; echo
for A in A B; do curl -s -X POST "localhost:$P/analiza?auto=$A" | python -c "import json,sys; d=json.load(sys.stdin); print('$A', d['wzorzec'], 'niepewny', d['niepewny'], 'czas', d['czas_s'], 'karta', d['pamiec_karty_MB'], 'MB', 'miejsc', len(d['miejsca'])); [print(' ', m['id'], m['gdzie'], m['ocena'], m['podloga'], m['gasi'], [m['x'],m['y'],m['w'],m['h']]) for m in d['miejsca']]"; done
F=$(ls $HOME/dane/rtg/bib/obrazy/g005_*dodatki.bmp | head -1)
python -c "from PIL import Image; Image.open('$F').save('/tmp/wl.png')"
curl -s -X POST --data-binary @/tmp/wl.png "localhost:$P/analiza?nazwa=wl.png" | python -c "import json,sys; d=json.load(sys.stdin); print('wlasne', d['nazwa'], d['wzorzec'], 'niepewny', d['niepewny'], 'ncc', d['ncc'], d['prog_ncc'], 'miejsc', len(d['miejsca']), 'czas', d['czas_s'])"
kill $PID
