# 05 — Priorytety założeń i atak na spec

Źródło: `docs/spec.md` (Z1–Z8 z §7.6 i ryzyka §7.7), `docs/pm/02-discover.md`, `docs/decyzje.md` (P1–P26), `docs/zadanie.md`. Spec zmieni się jeszcze tylko o dopisek P26.
Liczb pomiarowych jeszcze nie mamy (wynik bazowy Programisty niewypchnięty w chwili pisania) — oceny poniżej to szacunki Analityka w skali 1–5, **bez źródła pomiarowego**, a progi „rozstrzygające” to **propozycje** do potwierdzenia przez Programistę/Pawła.

## Część 1 — Priorytety założeń (prioritize-assumptions)

Wpływ = co się stanie, gdy założenie fałszywe (1–5). Niepewność = 1 − pewność (1–5, im mniej wiemy, tym więcej). Koszt sprawdzenia: n = niski (jeden przebieg na OMENie), ś = średni. Wynik = wpływ × niepewność.

| # | Założenie | Wpływ | Niepewność | Wynik | Koszt testu | Kategoria |
|---|---|---|---|---|---|---|
| Z1 | System znajdzie właściwy wzorzec w bibliotece | 5 | 4 | **20** | n | wysoki wpływ, wysokie ryzyko → eksperyment |
| Z3 | Czyste naczepy dostają 0 zaznaczeń (a: pusta bez wyboru, b: załadowana z wyborem) | 5 | 4 | **20** | n | → eksperyment |
| Z5 | Wybór towaru gasi ramki na ładunku, nie gasi skrytki | 4 | 4 | 16 | n | → eksperyment |
| Z8 | Wynik z łatwego wariantu przenosi się na trudniejszy | 4 | 4 | 16 | n | → eksperyment |
| Z2 | Limit 5 wystarcza na złapanie dodatków | 5 | 3 | 15 | n | → eksperyment |
| Z7 | B i C mieszczą się w 4 GB karty | 3 | 3 | 9 | n | wpływ średni; sprawdzić przy okazji |
| Z6 | < 1 min na obraz ~50 MB | 4 | 2 | 8 | n | wpływ wysoki, ryzyko niskie → wdrożyć i mierzyć |
| Z4 | Operator zdąży w ≤ 2 min (demo) | 2 | 2 | 4 | ś | odroczyć do pokazu |

Ryzyka ze spec §7.7 wchodzą do rankingu przez Z1 (zgodność wzorca zależy od biblioteki), Z3 (ocena organizatora może podać załadowane czyste naczepy) i Z2 (limit 5 ukrywa skrytkę poza piątką).

### Trzy najgroźniejsze i najtańsze sondy (dla Programisty, karta OMENa)

Każda sonda sprawdza kilka hipotez jednym przebiegiem na zbiorze testowym z generatora (`rtg/generator.py`, ocena `rtg/ocena.py`; trafienie = część wspólna ≥ 30%).

**Sonda 1 — Z1 + Z3(a): dobór wzorca i czyste bez wyboru** (najgroźniejsze: oba wynik 20)
- H1a: wzorzec wybrany dla badanego obrazu to ten sam typ naczepy.
- H1b: gdy typu brak w bibliotece, pasek „wzorzec niepewny” się zapala.
- H3a: pusta naczepa kontra pusta naczepa tego samego typu → 0 zaznaczeń.
- Policzyć: trafność doboru (% obrazów, gdzie typ wzorca = typ badanego); odsetek obrazów „typ nieznany” z zapaloną niepewnością; liczba zaznaczeń na czystych pustych (FP).
- Rozstrzyga (propozycja): trafność doboru ≥ 90% i FP = 0 na czystych pustych → założenia trzymają. Trafność < 70% albo jakikolwiek FP przy poprawnym wzorcu → zmiana podejścia (np. rejestracja wzorca przed różnicą, mniej czuły próg) przed dalszą pracą nad makietą.

**Sonda 2 — Z3(b) + Z5 + Z2: załadowane naczepy, wybór towaru i limit 5**
- H3b: załadowana naczepa z prawidłowym wyborem towaru → 0 zaznaczeń.
- H5a: wybór towaru obniża liczbę ramek na zgodnym ładunku.
- H5b: ten sam ładunek z dodatkiem → dodatek nadal zaznaczony po wyborze.
- H2: FN na pierwszej piątce vs na pełnej liście (także przy „nie wiem”).
- Policzyć: FP/FN para po parze (z wyborem i bez), FN@5 i FN@pełna lista.
- Rozstrzyga (propozycja): FP = 0 w H3b; H5b: ≥ 95% dodatków nadal zaznaczonych (ostatecznie wprost 100% w wersji demo); FN@5 − FN@pełna ≤ 5 pp. Dodatek zgaszony po wyborze towaru w jakimkolwiek przypadku = Z5 obalone, wybór towaru tylko obniża ocenę pewności, nie usuwa ramki.

**Sonda 3 — Z8 + Z6 + Z7: trudniejszy wariant, czas, pamięć**
- H8: progi dobrane na łatwym wariancie (szum, przesunięcie) → FN na trudniejszym rośnie najwyżej o 10 pp, FP zostaje 0 (próg ze spec KA8).
- H6: pełny obraz ~50 MB < 1 min (cel ≤ 30 s).
- H7: PatchCore i EfficientAD mieszczą się w 4 GB (pomiar szczytu).
- Policzyć: FP/FN na obu wariantach, czas od wczytania .bmp do raportu, szczyt pamięci karty.
- Rozstrzyga: KA6 i KA8 ze spec wprost (< 1 min; +10 pp; FP 0); pamięć > 4 GB → zostaje podejście A + mniejszy model (KA7).

Wspólne dla trzech sond: zleca się je jednym zleceniem na karcie, z wypisanymi hipotezami (instrukcja Analityka: kilka wad w jednym przebiegu). Z4 (2 min) i Z6 nie wymagają osobnych sond.

## Część 2 — Atak na spec (strategy-red-team)

Roszczenia nośne: (1) system dobierze pustą naczepę właściwego typu; (2) 5 zaznaczeń + licznik wystarcza; (3) wybór towaru obniża szum, nie ukrywa skrytek; (4) operator oceni decyzje i raport jest z nich wiarygodny; (5) wynik ze zbioru sztucznego coś mówi o realnym RTG.

### 1. Zły wzorzec zalewa operatora fałszywymi alarmami
- **Claim:** biblioteka wzorców pokrywa typy naczep, które przyjadą.
- **Steelman:** system dobiera najbliższą podobną i pokazuje „wzorzec niepewny”.
- **Fails if:** najbliższa podobna naczepa różni się konstrukcją na tyle, że każda różnica to „zaznaczenie”; pasek niepewny wisi na większości aut, więc operator przestaje go czytać.
- **Evidence to get this week:** sonda 1 — trafność doboru i odsetek aut z paskiem niepewności.
- **Kill criterion:** trafność doboru < 70% albo pasek na > 30% obrazów testowych (propozycja).
- **Łagodzenie:** próg pewności podniesiony, gdy wzorzec niepewny; dobór po rejestracji; raport zawsze podaje użyty wzorzec.

### 2. Limit 5 ukrywa prawdziwą skrytkę (ranking pewności się myli)
- **Claim:** najpewniejsze pierwsze; reszta to „+N dalszych miejsc”.
- **Steelman:** Artur chce kilku zaznaczeń, a nie kilkudziesięciu (P5, P8); licznik przypomina o reszcie.
- **Fails if:** skrytka ma niską ocenę pewności (mała, w gąszczu konstrukcji) i ląduje na miejscu 6+ — operator widzi tylko licznik i nic z nim nie robi.
- **Evidence to get this week:** sonda 2 — FN@5 vs FN@pełna lista.
- **Kill criterion:** FN@5 przewyższa FN@pełna o > 5 pp (propozycja).
- **Łagodzenie:** licznik klikalny (podgląd reszty bez decyzji); ranking po pewności i po pozycji w typowych miejscach skrytek (podłoga, ściana przy kabinie, P3); wynik FN@5 pokazywany w README.

### 3. Dodatek podszywa się pod zgodny ładunek i znika po wyborze towaru
- **Claim:** wybór towaru gasi ramki tylko na zgodnym ładunku (Z5).
- **Steelman:** gdy dodatek jest poza kształtem ładunku, ramka zostaje.
- **Fails if:** skrytka z towarem tego samego rodzaju (np. dodatkowe beczki/palety) wygląda jak zgłoszony ładunek, więc wybór „zgodnego” towaru wygasza właśnie ją. Atakujący może też zgłosić towar, który mu to ułatwia.
- **Evidence to get this week:** sonda 2 — pary „ten sam ładunek z i bez dodatku”, w tym dodatek tego samego rodzaju co ładunek.
- **Kill criterion:** ≥ 1 dodatek tego samego rodzaju co ładunek znika po wyborze towaru → wybór nie wygasza, tylko obniża pewność.
- **Łagodzenie:** wybór towaru zmienia kolejność i ocenę, nie usuwa pozycji (zostaje w „+N”); raport zapisuje wybrany towar.

### 4. Ocena organizatora i prawdziwe RTG dadzą inny rozkład niż nasz zbiór
- **Claim:** progi dobrane na zbiorze sztucznym pozostaną dobre (Z8, Z3).
- **Steelman:** trudniejszy wariant (szum, przesunięcie) odtwarza główne zakłócenia.
- **Fails if:** obrazy organizatora mają inną rozdzielczość, kontrast, rozjazd względem wzorca albo „czyste” naczepy są załadowane i podane bez wyboru towaru — wtedy FP > 0 mimo poprawnej pracy.
- **Evidence to get this week:** sonda 3 — FP/FN na dwóch wariantach; test załadowanej czystej bez wyboru (przy „nie wiem”) jako znana słabość.
- **Kill criterion:** FP > 0 na czystych trudniejszego wariantu albo wzrost FN > 10 pp.
- **Łagodzenie:** mówić wprost w README, slajdach i na pokazie, że dane są sztuczne; podać osobno wyniki łatwego i trudnego wariantu; przy „nie wiem” w przebiegu partiowym trzymać próg bardziej konserwatywny.

### 5. Operator odrzuca z nawyku i raport staje się dowodem „sprawdzone”
- **Claim:** „do kontroli” / „odrzuć” z powodem daje operatorowi kontrolę i wiarygodny raport (P7, P9, P10).
- **Steelman:** odrzucenie wymaga powodu; decyzje zostają w raporcie; odrzucone miejsca nie uczą systemu.
- **Fails if:** przy kilku autach dziennie i kilku minutach na auto operator odrzuca masowo powodem „zwykły ładunek”, a raport z odrzuconą skrytką chroni formalnie wszystkich — zamiast pomagać znaleźć skrytkę.
- **Evidence to get this week:** pokaz na dwóch autach (P18) — czy operator-tester z powodem „zwykły ładunek” odrzuci pozycję, która jest dodatkiem; czas ścieżki (KA4).
- **Kill criterion:** > 1 z 5 prawdziwych dodatków odrzucony powodem „zwykły ładunek” bez oglądania obu obrazów (propozycja, mała próba).
- **Łagodzenie:** klik w pozycję pokazuje miejsce na obu obrazach zanim aktywuje się „odrzuć”; wysoka pewność wymaga drugiego kliknięcia; raport pokazuje pewność obok decyzji.

### Co jest dobrze uzasadnione
- Nieuczenie się na odrzuceniach — świadoma decyzja Artura z powodem (P5).
- Limit 5 z licznikiem oraz osobne FN@5 i FN@pełna (KA2, KA9) — spec nazywa ryzyko i ma pomiar.
- Szczerość o danych sztucznych (spec §3, §7.7) — nie zawyża skuteczności.
- Kryteria KA1–KA10 są sprawdzalne, progi liczbowe czekają na przebieg bazowy.

### Czego nie umiem ocenić
- Ile aut dziennie i ile typów naczep przyjeżdża (P14 — założenie, brak danych KAS).
- Wielkości biblioteki wzorców i realnych różnic między typami.
- Zachowania operatora w stresie — dopiero pokaz.
- Liczb bazowych (wynik Programisty niewypchnięty).

### Co zrobić teraz
1. Programista: sonda 1 → sonda 2 → sonda 3 jednym zleceniem na OMENie, z wypisanymi hipotezami i meldunkiem „obalone/potwierdzone, liczby”.
2. Projektant: do speca dopisać, że wybór towaru zmienia ocenę pewności i kolejność, nie usuwa pozycji (łagodzenie nr 3), jeśli sonda 2 to potwierdzi — to zmiana produktowa, więc przez pytanie do Artura.
3. Prezenter: zdanie o danych sztucznych z §7.7 w README i na slajdzie.

<!-- skill: prioritize-assumptions -->
<!-- skill: strategy-red-team -->
