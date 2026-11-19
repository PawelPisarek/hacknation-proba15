# 06 — Scenariusze testów

Źródło: `docs/spec.md` (KA1–KA10, E1–E4), `docs/pm/05-zalozenia-atak.md`, skrypty Programisty `rtg/ocena.py`, `rtg/generator.py`, `rtg/wykryj.py`, `bazowy.sh` (stan klonu Analityka po `git pull`). Skryptów nie uruchamiałem (ciężkie liczenie tylko na OMENie) — braki poniżej wynikają z czytania kodu.
Progi liczbowe: z speca tylko < 1 min, FN +10 pp, FP = 0, ≤ 5 zaznaczeń, ≤ 2 min. Reszta (oznaczona „propozycja”) pochodzi z `05` i czeka na potwierdzenie.
Propozycja z ataku 3 (wybór towaru zmienia kolejność zamiast usuwać pozycję) **nie jest tu wymaganiem** — czeka na wynik sondy 2.

## Część A — Scenariusze użytkownika (ekrany E1–E4)

Rola we wszystkich: operator RTG (tester gra operatora). Dane: pokaz z udawanymi danymi (auto A „z dodatkiem”, auto B „czyste”).

**A1. Wybór auta i towaru (KA4, E1→E2)**
Cel: ścieżka od wyboru auta do raportu ≤ 2 min.
Warunek: aplikacja uruchomiona offline, E1 pokazuje auto A i B.
Kroki: 1) wybierz auto A (E1) → E2 się otwiera; 2) w linii nad obrazami wybierz jeden z 6 rodzajów towaru lub „nie wiem” → lista aktualizuje się; 3) zdecyduj przy każdej pozycji; 4) otwórz raport (E4). Zmierz stoperem od kroku 2 do E4.
Oczekiwane: lista towaru ma dokładnie 6 grup + „nie wiem” (drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa); bez wyboru działa jak „nie wiem”; czas ≤ 2 min.

**A2. Widok obok siebie i klik w pozycję (P15, P22)**
Warunek: E2 dla auta A.
Kroki: kliknij pozycję z listy.
Oczekiwane: wzorzec i badany obraz obok siebie, różnica podświetlona, miejsce widać na obu obrazach; podany jest identyfikator wzorca (np. W-PL-014).

**A3. Limit 5 i licznik (KA9)**
Warunek: auto A (7 miejsc z udawanych danych), towar „nie wiem”.
Kroki: otwórz E2; powtórz dla każdego z 6 towarów.
Oczekiwane: na liście zawsze ≤ 5 pozycji, najpewniejsza pierwsza, pod nimi „+2 dalszych miejsc” (licznik, nie zaznaczenie); liczba pozycji nigdy > 5, także przy „nie wiem”.

**A4. Brak zaznaczeń (P17)**
Warunek: auto B (czyste).
Kroki: otwórz E2.
Oczekiwane: komunikat „brak zaznaczeń” i pokazany użyty wzorzec; lista pusta, licznik „+N” nieobecny.

**A5. Wzorzec niepewny (KA1, P11, P25)**
Warunek: auto, dla którego w bibliotece nie ma naczepy tego typu.
Kroki: otwórz E2.
Oczekiwane: pasek „wzorzec niepewny” nad obrazami; raport (E4) powtarza oznaczenie. Przy dobrze dobranym wzorcu paska nie ma.

**A6. Odrzucenie z powodem (P7, P9, E3)**
Kroki: kliknij „odrzuć” przy pozycji → E3.
Oczekiwane: bez wyboru powodu odrzucenie się nie zapisuje; powody: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne; po wyborze pozycja oznaczona jako odrzucona z powodem.

**A7. „Do kontroli” (P16)**
Kroki: kliknij „do kontroli” przy pozycji.
Oczekiwane: tylko oznaczenie w raporcie, żadnego komunikatu do kontrolera; decyzja nie zmienia wyniku wykrywania (lista i kolejność bez zmian).

**A8. Raport z auta (E4, P10, §9)**
Warunek: decyzje podjęte w A6/A7.
Kroki: otwórz raport.
Oczekiwane: raport powstaje po decyzjach i je zawiera; jedna strona: identyfikator kontroli, użyty wzorzec (+ „wzorzec niepewny”, gdy był), zaznaczenia z oceną pewności, decyzje z powodem. Dla auta B: „brak zaznaczeń” + wzorzec.

**A9. Dopisek przy podwójnej podłodze (KA10, P26)**
Warunek: auto z dodatkiem w podłodze (auto A).
Kroki: otwórz E2, odszukaj pozycję leżącą w podłodze.
Oczekiwane: przy niej krótki dopisek „typowe miejsce skrytki: podwójna podłoga”, bez osobnego okna; przy pozycjach poza podłogą dopisku nie ma.

**A10. Praca bez internetu (zadanie §3)**
Kroki: odłącz sieć, wykonaj A1.
Oczekiwane: działa tak samo, żadne żądanie do chmury; język ekranu polski.

**A11. Odrzucone nie uczą (decyzja P5)**
Kroki: odrzuć pozycję, przeładuj to samo auto.
Oczekiwane: ta sama lista i kolejność jak wcześniej — odrzucenie nie zmienia wyniku.

## Część B — Scenariusze oceny liczbowej (skrypt `rtg/ocena.py`)

Format: warunek → kroki → oczekiwany wynik; „ocena” = `python -m rtg.ocena --dane … --wyniki …`, ciężkie kroki tylko na OMENie przez orkiestrator.

**B1. Czyste → każde zaznaczenie = FP (KA3a, Z3)**
Warunek: zbiór `pusta`/`maly`, obrazy roli „czysty” z `towar_zgloszony = pusta`.
Kroki: wykryj → ocena.
Oczekiwane: `FP_pusta = 0`, `czyste_z_alarmem = 0/N`. Jakikolwiek FP = test niezaliczony (cel zadania §6, spec KA3).

**B2. Załadowane czyste z prawidłowym wyborem towaru (KA3b)**
Warunek: obrazy „czysty” z `towar_zgloszony ≠ pusta`, wybór = ich towar.
Kroki: wykryj z wyborem → ocena.
Oczekiwane: `FP_zaladowana = 0`. Wersja kontrolna bez wyboru („nie wiem”): FP wolno > 0 — to znane ryzyko (spec §7.7), raportować osobno.

**B3. Dodatek nietrafiony = FN (KA2, KA5, §6)**
Warunek: obrazy roli „dodatki”, ramki prawdy w `etykiety.json`.
Kroki: wykryj → ocena.
Oczekiwane: `FN = 0/M` jest celem; każdy dodatek bez ramki o części wspólnej ≥ 30% (jego pola lub pola ramki) liczy się jako FN. Po wyborze towaru (KA5): ten sam dodatek nadal zaznaczony.

**B4. FN przy limicie 5 (KA2, KA9)**
Warunek: wyniki z ramkami z oceną pewności (5. element ramki).
Kroki: z każdego obrazu weź 5 ramek o najwyższej pewności → ocena; porównaj z oceną na pełnej liście.
Oczekiwane: dwie wartości FN obok FP; różnica FN@5 − FN@pełna ≤ 5 pp (propozycja z 05).

**B5. Trafność doboru wzorca (KA1, Z1)**
Warunek: biblioteka wzorców ≥ 2 typów naczep; badany obraz bez wskazania wzorca.
Kroki: dla każdego badanego obrazu system wybiera wzorzec → porównaj typ wzorca z typem badanego (`typ` w etykietach); policz % trafień i % obrazów z paskiem „niepewny”.
Oczekiwane: trafność podana liczbą; propozycja z 05: ≥ 90% = zaliczone, < 70% = przerwanie. Przy złym typie „niepewny” = tak.

**B6. Czas i pamięć (KA6, KA7)**
Warunek: zbiór `duzy` (~50 MB .bmp, 7300×2300×24 bit), OMEN, karta GTX 1050.
Kroki: wykryj na wszystkich obrazach `duzy`, odczytaj `czas_max_s` i „pamięć karty max”.
Oczekiwane: `czas_max_s < 60` (cel ≤ 30); pamięć ≤ 4 GB dla B (PatchCore) i C (EfficientAD) — inaczej zostaje podejście A + mniejszy model.

**B7. Trudniejszy wariant (KA8, Z8)**
Warunek: dwa zbiory z generatora — łatwy (np. wyższy `--kontrast`, mniej zakłóceń) i trudniejszy (niższy `--kontrast`, więcej szumu/przesunięcia).
Kroki: dobierz progi (`--zapas`) na łatwym → zamroź → wykryj i oceń na trudniejszym.
Oczekiwane: FN_trudny − FN_łatwy ≤ 10 pp, FP na czystych = 0; ocena wypisuje obie wartości.

**B8. Krzywa próg → FP/FN (KA3)**
Warunek: kilka wartości `--zapas`.
Kroki: wykryj + ocena dla każdego.
Oczekiwane: tabela próg / FP / FN w raporcie liczb; wybrany próg to ten, który daje FP = 0 przy najmniejszym FN.

## Część C — Czego skryptom brakuje względem scenariuszy (do Programisty przed kodem)

Stan: `ocena.py` liczy FP na czystych (z podziałem pusta/załadowana), FN, FP na obrazach z dodatkami, czas śr./max. `wykryj.py` zapisuje ramki z 5. elementem = pewność względem progu i drukuje pamięć karty.

1. **FN@5 (B4):** `ocena.py` liczy FN na wszystkich ramkach, nie na pierwszych 5 po pewności; brak parametru `--limit` i FN pełna/FN@5 obok siebie, brak licznika „+N”.
2. **Dobór wzorca (B5, KA1):** `wzorzec` w etykietach to zawsze pierwszy obraz tej samej grupy (ten sam typ), więc dobór z biblioteki nie jest ani wykonywany, ani mierzony; brak metryki trafności (typ wzorca = typ badanego) i brak flagi „wzorzec niepewny”. Zbiór nie zawiera przypadku „brak naczepy tego typu”.
3. **Wybór towaru (B2, KA5):** `wykryj.py` nie czyta `towar_zgloszony`, więc nie ma trybu „z wyborem” i „nie wiem”; `ocena.py` tylko dzieli FP wg towaru w etykiecie. Brak testu par (ten sam ładunek z dodatkiem i bez).
4. **Trudniejszy wariant (B7, KA8):** brak narzędzia porównującego łatwy i trudny zbiór (różnica pp FN, FP na czystych) i zamrażania progu z łatwego; generator ma `--kontrast`, `--ziarno`, `--wariant`, ale nie ma nazwanej konfiguracji „trudny” z szumem i przesunięciem.
5. **Krzywa próg → FP/FN (B8, KA3):** `wykryj.py` ma jedno `--zapas` na przebieg; brak przeglądu kilku progów i tabeli wyniku.
6. **Werdykt zaliczone/niezaliczone (B1–B7):** `ocena.py` tylko drukuje liczby, nie porównuje z progami KA i zawsze kończy kodem 0 — brak `--wymagaj` i kodu wyjścia ≠ 0 przy FP > 0, czasie ≥ 60 s lub FN + 10 pp.
7. **Pamięć karty (B6, KA7):** szczyt pamięci wypisuje `wykryj.py` w osobnej linii na ekran, `ocena.py` go nie zbiera, nie ma go w wyniku JSON; brak przebiegu B (PatchCore) i C (EfficientAD) — `METODY` to dziś tylko `roznica` i `nauka`.
8. **Czas z podziałem (B6, KA6):** `czas_s` w wynikach to czas jednego obrazu (wczytanie, punktacja, ramki), ale zbiór `duzy` ma tylko 2–3 obrazy testowe; brak oznaczenia, czy czas obejmuje wczytanie .bmp 50 MB w pełnej rozdzielczości (`--roboczy 1800` zmniejsza szerokość roboczą) — trzeba potwierdzić, że mierzymy pełną ścieżkę.
9. **Ekrany A1–A11:** niczego z części A skrypty nie pokrywają — to testy makiety (Programista, ręcznie lub skryptem przeglądarkowym); do uzgodnienia, kto je wykonuje.
10. **Trafienie:** `trafia` uznaje trafienie przy ≥ 30% pola dodatku **lub** pola ramki (spec §4: „pola dodatku lub ramki”) — zgodne; uwaga: duża ramka w środku małego dodatku nie trafi, zgodnie z komentarzem w pliku.

Do `docs/decyzje.md`: braki 1–8 są techniczne, ich zakres (limit w ocenie, tryb wyboru towaru, test trudnego wariantu) wynika wprost z KA2, KA5, KA8 — Programista dopisuje bez pytania Artura.

<!-- skill: test-scenarios -->
