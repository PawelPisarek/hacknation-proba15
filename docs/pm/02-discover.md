# 02 — Odkrywanie produktu (/discover)

Oparte na: `docs/pm/01-competitive-analysis.md` (wersja końcowa po R3), `docs/decyzje.md` (P2–P20, moment (b)), `docs/zadanie.md`.
Kontekst: **nowy produkt** (narzędzie dla KAS), odkrywanie ma ustawić decyzję, co wchodzi do pierwszej wersji (MVP) i co pokazujemy w demo.

## Co wiemy (krok 1)
- **Użytkownik (P2):** operator przy stanowisku RTG, w trakcie kontroli, ma kilka minut na auto. Liczby aut nie znamy — zakładamy kilkadziesiąt dziennie (P14, **założenie**).
- **Problem (P3):** małe skrytki — najczęściej podwójna podłoga lub ściana przy kabinie — giną wśród detali konstrukcji; obecne narzędzie KAS (papierosy) ich nie łapie.
- **Zysk (P4):** mniej przeoczonych skrytek.
- **Cena błędu (P5):** przeoczony dodatek jest gorszy niż zbędny alarm (minuta więcej przy aucie); zaznaczeń na auto kilka, nie kilkadziesiąt → limit **5** (P8), najpewniejsze pierwsze.
- **Z zadania §6 (ustalone, nie pytanie):** na czystym obrazie zero zaznaczeń; każde zaznaczenie = alarm FP; pominięty dodatek = FN.
- **Z analizy konkurencji (01):** porównanie ze wzorcem to znany prior art (ACXIS, patenty); wyróżnia nas dobór wzorca, ocena pewności z limitem 5 i decyzja operatora z powodem w raporcie.
- **Wzorzec (P19, A):** pusta naczepa tego samego typu. Operator przed analizą wybiera z listy rodzaj zgłoszonego towaru (plus „pusta naczepa”), by zgodny ładunek nie dostawał ramek; bez wyboru zaznaczamy wszystko (P5). Gdy brak naczepy tego typu: najbliższa podobna + „wzorzec niepewny” (P11).
- **Perspektywa przeglądu (P12):** funkcje dla operatora. **P13:** bez zmian w wyborze.

## Decyzja, którą to odkrywanie ustawia
Co wchodzi do MVP i demo (jedno auto czyste + jedno z dodatkiem, P18, główna ścieżka do 2 min) oraz co sprawdzamy eksperymentem przed zaufaniem wynikowi.

## W MVP wprost z P19
Wybór zgłoszonego towaru z listy (plus „pusta naczepa”) jest w MVP, bo wynika z odpowiedzi Artura P19 — nie z założenia Z5. Bez wybranego towaru (albo przy „nie wiem”) nie wygaszamy niczego (P19). Wariant „pusta naczepa bez wyboru” **wchodzi do oceny czystych** z celem 0 zaznaczeń (Z3a, decyzja Szefa 11:32); do oceny czystych nie wchodzi tylko załadowana naczepa bez wyboru towaru.

## Pomysły (krok 2) i wybór Artura (moment (b), 11:25)
Wybrane:
1. **Dobór wzorca** — system sam szuka najbliższej pustej naczepy tego typu w bibliotece; gdy typu brak: najbliższa podobna + „wzorzec niepewny” (P6, P11, P19). **Wybór zgłoszonego towaru z listy jest częścią tego pomysłu i jest w MVP (P19).**
2. **Zaznaczenia z oceną pewności** — do 5 na auto, najpewniejsze pierwsze (P8).
3. **Zatwierdź / odrzuć jednym kliknięciem** — „do kontroli” albo odrzucenie z powodem z listy: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne (P7, P9). Po „do kontroli” samo oznaczenie w raporcie (P16).
4. **Widok obok siebie** — jeden monitor, podział ekranu: wzorzec i badany obraz, różnica podświetlona (P15).
5. **Raport z auta** — jedna strona z zaznaczeniami, decyzjami operatora, użytym wzorcem i polem identyfikującym kontrolę (P10, §9 zadania). Przy braku zaznaczeń: komunikat „brak zaznaczeń” i pokazany użyty wzorzec (P17).
6. **Podpowiedź przy podwójnej podłodze** — tylko ta część pomysłu „typowe miejsca” (P3).

Odrzucone (Artur): uczenie na odrzuceniach — odrzucone miejsca mogłyby ukryć prawdziwe skrytki (P5); pozostała część „typowych miejsc”. P13: nic nie zmieniać, nic z odrzuconych nie brać w części.

## Założenia (krok 3) i najryzykowniejsze (krok 4, potwierdzone przez Artura 11:25)
Najryzykowniejsze: **Z1 dobór wzorca**.

| # | Założenie | Kategoria | Eksperyment | Kryterium |
|---|---|---|---|---|
| Z1 | System znajdzie właściwy wzorzec w bibliotece (**najryzykowniejsze**) | wykonalność | Na zbiorze testowym: dla każdego badanego obrazu sprawdzić, czy wybrany wzorzec to ten sam typ naczepy | trafność doboru zmierzona i podana; przy złym typie widoczne „wzorzec niepewny”; próg poda Programista po krzywej z przebiegu bazowego |
| Z2 | Do 5 zaznaczeń wystarcza na złapanie dodatków | wartość | Policzyć FN przy limicie 5 | FN na zbiorze testowym podane obok FP; próg poda Programista po krzywej z przebiegu bazowego |
| Z3 | Czyste naczepy dostają 0 zaznaczeń (zadanie §6). Przebieg automatyczny i partiami odbywa się bez operatora, więc obowiązuje „nie wiem” (nic nie jest wygaszane); czyste obrazy z oceny wg §6 to puste naczepy (§3) | wykonalność | Dwa warianty: (a) **pusta naczepa bez wyboru towaru** — pusty wzorzec kontra pusty badany; (b) **załadowana naczepa z prawidłowym wyborem towaru** | w obu wariantach 0 zaznaczeń; krzywa próg → FP/FN raportowana osobno |
| Z4 | Operator zdąży ocenić zaznaczenia w kilka minut (P2) | użyteczność | Demo: przejście 1 auta od wyboru towaru do raportu | główna ścieżka w demo ≤ 2 min (ustalenie Szefa) |
| Z5 | Wybór zgłoszonego towaru z listy ogranicza zbędne ramki na zgodnym ładunku, nie ukrywając skrytek | wartość / ryzyko | Para: ten sam ładunek z i bez dodatku; porównać ramki przy wyborze towaru i bez wyboru | dodatek nadal zaznaczony po wyborze towaru; ramki na zgodnym ładunku spadają; próg poda Programista po krzywej z przebiegu bazowego |
| Z6 | Czas analizy jednego obrazu ~50 MB mieści się w limicie (zadanie §7) | wykonalność | Pomiar na karcie OMENa: od wczytania .bmp do raportu | < 1 min na obraz (cel z zapasem ≤ 30 s) |
| Z7 | Podejścia B (PatchCore) i C (EfficientAD) mieszczą się w 4 GB pamięci karty | wykonalność | Przebieg na kaflach na GTX 1050, pomiar szczytu pamięci | mieści się w 4 GB; inaczej zostaje podejście A + mniejszy model |
| Z8 | Wynik na danych sztucznych z zakłóceniami (szum, przesunięcie) przenosi się na trudniejszy wariant zbioru | wiarygodność | „Strojenie” = dobór progów i parametrów na łatwym wariancie; „nauka” = model z obrazów czystych (§5). Stroić na łatwym, ocenić FP/FN na trudniejszym | FN na trudniejszym wariancie rośnie najwyżej o 10 punktów procentowych, a FP na czystych zostaje 0 |

Te eksperymenty wracają w `/write-prd` i specu jako kryteria akceptacji i ryzyka.

## Czego nie wiem o produkcie
Pytania P2–P20 mają odpowiedź. Otwarte tylko założenia: liczba aut dziennie (P14); progi Z1, Z2 i Z5 wpisze Programista po krzywej z przebiegu bazowego (do tego czasu bez liczb).

**Ograniczenie:** wynik na danych sztucznych nie dowodzi skuteczności na RTG z KAS i mówimy to wprost w materiałach (slajdy, README, pokaz).

**Ryzyko:** ocena może podać załadowane czyste naczepy zamiast pustych; wtedy bez wyboru towaru pojawią się fałszywe alarmy (przy „nie wiem” zaznaczamy wszystko, P19).

UPROSZCZENIE: biblioteka wzorców — mały zbiór sztucznych naczep — zamiast realnych zdjęć KAS — dorobienie: duże (dane KAS).
UPROSZCZENIE: lista rodzajów zgłoszonego towaru (P20) — 6 grup + „nie wiem” (wtedy zaznaczamy wszystko): drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa — zamiast pełnej klasyfikacji towarów — dorobienie: małe. (Typy naczep — plandeka, chłodnia, kontener — to osobna sprawa: wybór wzorca z biblioteki.)
UPROSZCZENIE: bez integracji z repozytorium RTG i urządzeniami — pole identyfikujące kontrolę w raporcie — zamiast integracji (§9) — dorobienie: duże.

<!-- skill: przeplywy-pm -->
<!-- skill: brainstorm-ideas-new -->
<!-- skill: identify-assumptions-new -->
