# 07 — Historyjki użytkownika (z docs/spec.md, ekrany E1–E4, KA1–KA10)

Źródło: `docs/spec.md` (P1–P26). Bez nowych funkcji poza specem. Kolejność = kolejność budowy MVP. Dane pokazu są udawane (sztuczne .bmp). Skilla historyjek „Jako…” nie mam — użyłem skilla przeplywy-pm (ze specu), kryteria w stylu skilla job-stories.

| # | Historyjka | Ekran | KA |
|---|---|---|---|
| H1 | Wybór auta | E1 | KA4 |
| H2 | Wybór rodzaju towaru | E2 | KA3, KA5 |
| H3 | Dobór wzorca i pasek „wzorzec niepewny” | E2 | KA1 |
| H4 | Porównanie obok siebie z różnicą | E2 | KA6, KA7 |
| H5 | Lista do 5 zaznaczeń + „+N dalszych miejsc” | E2 | KA2, KA9 |
| H6 | Dopisek przy podwójnej podłodze | E2 | KA10 |
| H7 | „Do kontroli” / „odrzuć” z powodem | E2, E3 | KA4 |
| H8 | „Brak zaznaczeń” na czystym aucie | E2 | KA3 |
| H9 | Raport z auta | E4 | KA4 |
| H10 | Wynik wiarygodny na trudniejszych danych | — | KA8 |

## H1. Wybór auta (E1)
**Jako** operator RTG, **chcę** wczytać jedno z dwóch aut (A „z dodatkiem”, B „czyste”), **żeby** zacząć kontrolę bez przygotowań.
Kryteria: (1) widać dwa auta do wczytania; (2) po wyborze wchodzę na E2; (3) cała ścieżka od wyboru towaru do raportu ≤ 2 min (KA4).

## H2. Wybór rodzaju towaru (E2)
**Jako** operator, **chcę** przed analizą wybrać rodzaj zgłoszonego towaru z listy w jednej linii nad obrazami, **żeby** zgodny ładunek nie dostawał zbędnych ramek.
Kryteria: (1) 7 pozycji: drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa, „nie wiem”; (2) bez wyboru = „nie wiem” (zaznaczamy wszystko, nadal ≤ 5); (3) dodatek zostaje zaznaczony po wyborze towaru (KA5); (4) pusta naczepa bez wyboru oraz załadowana z prawidłowym wyborem dają 0 zaznaczeń na czystych (KA3).

## H3. Dobór wzorca i ostrzeżenie (E2)
**Jako** operator, **chcę** żeby system sam dobrał wzorzec (pusta naczepa tego samego typu) i ostrzegł, gdy go nie ma, **żeby** wiedzieć, na ile ufać porównaniu.
Kryteria: (1) widać nazwę wzorca (np. W-PL-014); (2) gdy brak naczepy tego typu, użyta najbliższa podobna i nad obrazami widać pasek „wzorzec niepewny”; (3) trafność doboru zmierzona i podana (KA1).

## H4. Porównanie obok siebie (E2)
**Jako** operator, **chcę** widzieć wzorzec i badany obraz obok siebie z podświetloną różnicą na jednym monitorze, **żeby** ocenić miejsce bez przełączania ekranów.
Kryteria: (1) podział ekranu, dwa obrazy; (2) różnica podświetlona; (3) obraz ~50 MB analizowany < 1 min na karcie OMENa (KA6); (4) wybrane podejścia mieszczą się w 4 GB, inaczej podejście A + mniejszy model (KA7).

## H5. Lista zaznaczeń (E2)
**Jako** operator, **chcę** listę najwyżej 5 zaznaczeń z oceną pewności, najpewniejsze pierwsze, z „+N dalszych miejsc” gdy było więcej, **żeby** zacząć od najbardziej podejrzanych i wiedzieć, że coś jeszcze jest.
Kryteria: (1) zawsze ≤ 5 pozycji, także przy „nie wiem” (KA9); (2) licznik „+N dalszych miejsc” nie jest zaznaczeniem; (3) klik w pozycję pokazuje miejsce na obu obrazach; (4) FN przy limicie 5 podane obok FP, na pełnej liście i na pierwszej piątce osobno (KA2). Dane pokazu: auto A — 7 miejsc → 5 + „+2” (udawane).

## H6. Dopisek przy podwójnej podłodze (E2)
**Jako** operator, **chcę** przy pozycji leżącej w podłodze krótki dopisek „typowe miejsce skrytki: podwójna podłoga”, **żeby** szybciej ocenić najczęstszą skrytkę.
Kryteria: (1) dopisek przy pozycji listy, bez osobnego okna; (2) na aucie A z dodatkiem w podłodze widać go przy właściwej pozycji (KA10).

## H7. „Do kontroli” i „odrzuć” (E2, E3)
**Jako** operator, **chcę** jednym kliknięciem przy pozycji zatwierdzić „do kontroli” albo odrzucić z powodem, **żeby** moja decyzja trafiła do raportu.
Kryteria: (1) przyciski przy każdej pozycji listy; (2) odrzucenie wymaga powodu z listy: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne (E3); (3) „do kontroli” to samo oznaczenie w raporcie, bez komunikatu do kontrolera; (4) decyzje nie zmieniają wyniku wykrywania ani nie uczą systemu; (5) czas ścieżki ≤ 2 min (KA4).

## H8. „Brak zaznaczeń” (E2)
**Jako** operator, **chcę** na czystym aucie komunikat „brak zaznaczeń” z pokazanym użytym wzorcem, **żeby** mieć pewność, że system analizował, a nie zawiódł.
Kryteria: (1) auto B: zero zaznaczeń, komunikat i wzorzec widoczne; (2) 0 zaznaczeń na czystych w obu wariantach (KA3).

## H9. Raport z auta (E4)
**Jako** operator, **chcę** raport z auta powstający po moich decyzjach, **żeby** kontroler i archiwum miały zaznaczenia, wzorzec i moje powody.
Kryteria: (1) jedna strona: pole identyfikujące kontrolę (miejsce i przedmiot, §9, numer sztuczny), użyty wzorzec (+ „wzorzec niepewny”), zaznaczenia z oceną, decyzje z powodem; (2) przy braku zaznaczeń: „brak zaznaczeń” i wzorzec; (3) raport dostępny w czasie ścieżki ≤ 2 min (KA4).

## H10. Wiarygodność na trudniejszych danych (bez ekranu)
**Jako** zespół (Programista), **chcę** sprawdzić, że wynik przenosi się z łatwego na trudniejszy wariant zbioru, **żeby** nie oszukać się wynikiem na danych sztucznych.
Kryteria: (1) FN na trudniejszym wariancie rośnie najwyżej o 10 pp, FP na czystych 0 (KA8); (2) w materiałach jawnie: dane sztuczne nie dowodzą skuteczności na RTG z KAS.

<!-- skill: przeplywy-pm -->
