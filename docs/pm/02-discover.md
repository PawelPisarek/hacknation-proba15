# 02 — Odkrywanie produktu (/discover)

Oparte na: `docs/pm/01-competitive-analysis.md` (wersja końcowa po R3), `docs/decyzje.md` (P2–P19, moment (b)), `docs/zadanie.md`.
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

## Pomysły (krok 2) i wybór Artura (moment (b), 11:25)
Wybrane:
1. **Dobór wzorca** — system sam szuka najbliższej pustej naczepy tego typu w bibliotece; gdy typu brak: najbliższa podobna + „wzorzec niepewny” (P6, P11, P19).
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
| Z1 | System znajdzie właściwy wzorzec w bibliotece (**najryzykowniejsze**) | wykonalność | Na zbiorze testowym: dla każdego badanego obrazu sprawdzić, czy wybrany wzorzec to ten sam typ naczepy | trafność doboru zmierzona i podana; przy złym typie widoczne „wzorzec niepewny” |
| Z2 | Do 5 zaznaczeń wystarcza na złapanie dodatków | wartość | Policzyć FN przy limicie 5 | FN na zbiorze testowym podane obok FP |
| Z3 | Czyste naczepy nie dostają zaznaczeń | wykonalność | Przebieg na czystych parach (pusta naczepa vs czysta) | 0 zaznaczeń lub podany odsetek FP; krzywa próg → FP/FN |
| Z4 | Operator zdąży ocenić zaznaczenia w kilka minut | użyteczność | Demo: przejście 1 auta od wyboru towaru do raportu | główna ścieżka w demo ≤ 2 min |
| Z5 | Wybór zgłoszonego towaru z listy ogranicza zbędne ramki na zgodnym ładunku, nie ukrywając skrytek | wartość / ryzyko | Para: ten sam ładunek z i bez dodatku; porównać ramki przy wyborze towaru i bez wyboru | dodatek nadal zaznaczony po wyborze towaru; ramki na zgodnym ładunku spadają |
| Z6 | Wynik na danych sztucznych jest wiarygodnym wskaźnikiem | wykonalność | Zbiór z szumem, przesunięciem, różnymi typami; uczciwy opis ograniczeń | w slajdach i README: wynik na danych sztucznych, nie KAS |

Te eksperymenty wracają w `/write-prd` i specu jako kryteria akceptacji i ryzyka.

## Czego nie wiem o produkcie
Wszystkie pytania z listy mają odpowiedź (P2–P19). Otwarte tylko założenia: liczba aut dziennie (P14); próg zaznaczeń — ustalają ludzie po krzywej FP/FN (01).

UPROSZCZENIE: biblioteka wzorców — mały zbiór sztucznych naczep — zamiast realnych zdjęć KAS — dorobienie: duże (dane KAS).
UPROSZCZENIE: lista rodzajów towaru — kilka pozycji (plandeka, chłodnia, kontener, pusta) — zamiast pełnej klasyfikacji — dorobienie: małe.
UPROSZCZENIE: bez integracji z repozytorium RTG i urządzeniami — pole identyfikujące kontrolę w raporcie — zamiast integracji (§9) — dorobienie: duże.

<!-- skill: przeplywy-pm -->
<!-- skill: brainstorm-ideas-new -->
<!-- skill: identify-assumptions-new -->
