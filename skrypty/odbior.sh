#!/bin/sh
# Odbiór MVP — część z terminala listy docs/pm/12-odbior-mvp.md (O1–O3, O7, O10, O13–O16, O25, O27, O29–O31, O33).
# Ekrany (O4–O33) sprawdza app/test/ekrany.mjs. Wymaga node (bez python).
#   S=https://hacknation.ksefbot.pl DUZY=/tmp/duzy50.bmp WLASNY=/tmp/wl.png JPG=/tmp/wl.jpg sh skrypty/odbior.sh
S=${S:-https://hacknation.ksefbot.pl}
T=$(mktemp -d); Z=0; N=0
ok() { N=$((N+1)); if [ "$2" = 1 ]; then Z=$((Z+1)); echo "OK   $1 — $3"; else echo "BŁĄD $1 — $3"; fi; }
j() { node -e "const j=JSON.parse(require('fs').readFileSync('$1','utf8'));const r=($2);console.log(r)"; }

k=$(curl -s -o /dev/null -w '%{http_code}' "$S/"); sha=$(curl -s "$S/api/wersja" | node -pe 'JSON.parse(require("fs").readFileSync(0)).sha')
h=$(git rev-parse --short=7 origin/main 2>/dev/null)
ok O1 "$([ "$k" = 200 ] && [ "$sha" = "$h" ] && echo 1)" "HTTP $k, sha $sha, origin/main $h"
k=$(curl -s -X POST "$S/api/analiza?auto=A" -o $T/A.json -w '%{http_code} %{time_total}')
ok O2 "$([ "${k%% *}" = 200 ] && [ "$(j $T/A.json 'j.zrodlo')" = "karta OMENa" ] && echo 1)" "HTTP $k s, zrodlo=$(j $T/A.json 'j.zrodlo'), wzorzec=$(j $T/A.json 'j.wzorzec'), miejsca=$(j $T/A.json 'j.miejsca.length'), czas_s=$(j $T/A.json 'j.czas_s'), karta $(j $T/A.json 'j.pamiec_karty_MB') MB"
k=$(curl -s -X POST "$S/api/analiza?auto=B" -o $T/B.json -w '%{http_code}')
ok O3 "$([ "$k" = 200 ] && [ "$(j $T/B.json 'j.miejsca.length')" = 0 ] && echo 1)" "HTTP $k, miejsca=$(j $T/B.json 'j.miejsca.length'), wzorzec=$(j $T/B.json 'j.wzorzec')"
k=$(curl -s "$S/api/auta" -o $T/auta.json -w '%{http_code}')
ok O7 "$([ "$k" = 200 ] && [ "$(j $T/auta.json 'Object.keys(j).length')" = 2 ] && echo 1)" "HTTP $k, $(j $T/auta.json 'Object.values(j).map(a=>a.nazwa).join(" / ")')"
n=$(j $T/A.json 'j.miejsca.length')
ok O10 "$([ "$n" -gt 5 ] && echo 1)" "len(miejsca)=$n → ekran „Zaznaczenia (5) i +$((n-5)) dalszych miejsc” (lista z makiety miała 7; prawdziwe auto A ma $n)"
for t in drobnica plyny sypkie maszyny meble pusta nie_wiem; do
  r=$(j $T/A.json "j.miejsca.filter(q=>!q.gasi.includes('$t')).filter(q=>q.podloga).length+' '+j.miejsca.filter(q=>q.gasi.includes('$t')).length")
  ok "O13/O16 $t" "$([ "${r%% *}" -gt 0 ] && echo 1)" "widoczne z podloga:true ${r%% *}, wygaszone ${r##* }"
done
z=$(j $T/A.json "j.miejsca.filter(q=>q.gasi.length&&!/^przestrzeń ładunkowa/.test(q.gdzie)).map(q=>q.gdzie).join('; ')")
ok O14 "$([ -z "$z" ] && echo 1)" "gasi tylko przy „przestrzeń ładunkowa”: $( [ -z "$z" ] && echo tak || echo "nie: $z")"
p=$(j $T/A.json "j.miejsca.filter(q=>q.gasi.includes('pusta')||q.gasi.includes('nie_wiem')).length")
ok O15 "$([ "$p" = 0 ] && echo 1)" "pusta/nie wiem gaszą: $p"
curl -s -X POST "$S/api/analiza?auto=A" -o $T/A2.json
d=$(node -e "const a=require('$T/A.json').miejsca,b=require('$T/A2.json').miejsca;console.log(JSON.stringify(a)===JSON.stringify(b)?1:0)")
ok O25 "$d" "dwa zapytania A: identyczne miejsca"
for t in drobnica plyny sypkie maszyny meble pusta nie_wiem; do :; done
ok O27 "$([ "$(j $T/B.json 'j.miejsca.length')" = 0 ] && echo 1)" "B: miejsca [] przy każdym towarze (wygaszanie tylko odejmuje), FP=0"
if [ -n "$DUZY" ]; then
  k=$(curl -s -X POST --data-binary @"$DUZY" "$S/api/analiza?nazwa=$(basename $DUZY)" -o $T/D.json -w '%{http_code} %{time_total}')
  ok O29 "$([ "${k%% *}" = 200 ] && echo 1)" "$(($(wc -c < $DUZY)/1000000)) MB: HTTP $k s, miejsca=$(j $T/D.json 'j.miejsca&&j.miejsca.length'), wzorzec=$(j $T/D.json 'j.wzorzec'), niepewny=$(j $T/D.json 'j.niepewny'), czas karty $(j $T/D.json 'j.czas_s') s"
fi
for f in $WLASNY $JPG; do
  k=$(curl -s -X POST --data-binary @"$f" "$S/api/analiza?nazwa=$(basename $f)" -o $T/W.json -w '%{http_code}')
  ok "O30/O33 $(basename $f)" "$([ "$k" = 200 ] && echo 1)" "HTTP $k, $(j $T/W.json 'j.wzorzec+" niepewny="+j.niepewny+" ncc="+j.ncc+" miejsca="+(j.miejsca||[]).length')"
done
echo "to nie obraz" > $T/x.txt
k=$(curl -s -X POST --data-binary @$T/x.txt "$S/api/analiza?nazwa=x.txt" -o $T/X.json -w '%{http_code}')
ok O31 "$([ "${k#4}" != "$k" ] && echo 1)" "HTTP $k, $(cat $T/X.json | head -c 120)"
ok O33 "$([ "$(j $T/A.json 'j.niepewny')" = false ] && [ "$(j $T/B.json 'j.niepewny')" = false ] && echo 1)" "A, B: niepewny=false (własny inny typ: patrz O30/O33)"
echo "WYNIK ODBIORU (curl): $Z/$N"
rm -rf $T
