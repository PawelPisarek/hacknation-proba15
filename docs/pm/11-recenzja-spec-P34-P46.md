# Recenzja speca R1 — P34–P46 (docs/spec.md, 2a07877)

Względem: odpowiedzi Artura P34–P46 w `docs/decyzje.md`. P34–P38 są w 7.2/7.3/7.4/7.5 i KA9/KA12/KA16 — bez braków. Braki (od najważniejszego):

1. **[produkt] P40 tylko w KA13/KA17 i 7.8, nie w 7.2/7.4/7.5.** 7.2 (l. 42) dalej pisze „każdy rodzaj towaru oprócz pusta naczepa wygasza swoje typowe miejsca” — bez „tylko wnętrze ładunku, nie dach, podłoga, ściana przednia”. Wprost sprzeczne z KA13/KA17 czytane osobno. Ponadto 7.2 l. 42 (rodzaje towaru wygaszają, „nie wiem” na liście rodzajów) a KA13/7.3 („nie wiem” nic nie wygasza, N=0) — wpisać „nie wiem” obok „pusta naczepa” w 7.2.
2. **[produkt] P42 (komunikat „Brakuje decyzji: N, w tym M w dalszych miejscach” + „rozwiń”) tylko w KA17 i 7.8.** 7.3 i E4/E2 w 7.5 mówią tylko „dostępny dopiero po decyzjach”; KA14 „niedostępny” bez komunikatu. Brak, gdzie widać komunikat (E2 przy przycisku raportu) i w 7.5.
3. **[produkt] P44 B (zmiana towaru zachowuje decyzje) tylko w KA17 i 7.8; „miejsca, które zostają” niezdefiniowane.** Wybór towaru zmienia wzorzec (P19 A) i listę zaznaczeń; spec nie mówi, po czym miejsce „zostaje” (ta sama pozycja/ramka? ten sam wskaźnik?) ani nie wpisuje reguły do 7.4. Do tego 7.8 „raport liczy się od nowa” — nie ma tego w 7.3.
4. **[produkt] P45 A: 7.1 (nagłówek „demo ≤ 2 min… dwa auta, P18”) i KA4 przeczą KA17/7.8** („w 2 min tylko auto A; auto B i własne zdjęcie jako krótkie ujęcia poza 2 min”). 7.1 nadal wlicza dwa auta do 2 min; poprawić 7.1 i KA4 na auto A.
5. **[technika] P41 i P43 nie wchodzą do kryteriów w pełni.** P43 (przycisk „do kontroli” niebieski, czerwień tylko dla wysokiej pewności, wyraźniejszy tekst odrzuconych) jest w 7.2, ale w żadnym KA; KA17 (tytuł P40–P45) go nie ma, a KA16 opisuje tylko stare kolory. P41 „ta sama zasada w raporcie” — 7.3 nie mówi, jaki nagłówek/liczba w raporcie auta A (7 pozycji).

<!-- skill: przesluchanie-hackathon -->

## R2 (docs/spec.md, 81c158f, względem P34–P46 i wpisu Szefa 14:08 o 44 B)

Sprawdzone punkty R1: 1 (P40 w 7.2, 7.4, 7.5; „nie wiem” obok „pusta naczepa” w 7.2), 2 (P42 w 7.2, 7.3, 7.5, KA17), 3 (P44 B z regułą „to samo miejsce” — kontur pokrywa się — w 7.2, 7.3, 7.4, KA17, zgodna z wpisem Szefa 14:08), 4 (P45 A w 7.1, KA4, KA17, 7.5 E1), 5 (P41 w 7.3, 7.5 E4, KA12; P43 w KA18). Sprzeczności między 7.1–7.5, KA4/KA13/KA16/KA17/KA18 i 7.8 nie znalazłem.

brak braków zmieniających zakres lub kryteria

Uwaga techniczna (nie brak): „kontur pokrywa się” (P44 B) i „wyraźniejszy kontrast” (KA18) nie mają progu — próg ustala Programista w MVP, bez zmiany tego, co widzi użytkownik.
