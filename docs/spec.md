## Product Requirements Document: Wyszukiwarka anomalii na obrazach RTG naczep (KAS)

**Author**: Projektant (zespół Hackathon) — z ustaleń Artura (produkt) i Pawła (technika)
**Date**: 2026-11-19
**Status**: Draft (wejście: docs/pm/01–03, docs/decyzje.md P1–P38; P40–P46 rozstrzygnięte, patrz 7.8)

## 1. Summary
Narzędzie dla operatora RTG KAS: system sam porównuje obraz badanej naczepy z obrazem wzorcowej, pustej naczepy tego samego typu i zaznacza do 5 miejsc podejrzanych (najpewniejsze pierwsze). Operator na jednym ekranie z podziałem (wzorzec obok badanego) zatwierdza „do kontroli” albo odrzuca z powodem. Wynik trafia do raportu z auta. Dane: sztuczne obrazy .bmp (zdjęć KAS nie mamy); wynik z usługi na karcie OMENa (GTX 1050 4 GB).

## 2. Contacts
Artur — kształt produktu (pokój Produkt); Paweł — technika, wygląd, użyteczność; zespół: Szef, Projektant, Analityk, Programista, Prezenter.

## 3. Background
- Zadanie KAS (docs/zadanie.md): operatorzy przeoczają małe skrytki (najczęściej podwójna podłoga lub ściana przy kabinie) wśród detali konstrukcji; obecne narzędzie (papierosy) ich nie łapie (P3).
- Porównanie ze wzorcem to znany prior art (ACXIS, patenty); wyróżnia nas dobór wzorca, ocena pewności z limitem 5 i decyzja operatora z powodem w raporcie (01).
- Perspektywa: funkcje dla operatora, nie cena ani rynek (P12, decyzja Szefa 11:22).
- Dane sztuczne nie dowodzą skuteczności na RTG z KAS — mówimy to wprost w materiałach (README, slajdy, pokaz).

## 4. Objective
- **Cel użytkownika:** mniej przeoczonych skrytek (P4). Przeoczony dodatek jest gorszy niż zbędny alarm — minuta więcej przy aucie (P5).
- **Metryki (zadanie §6):** FP = każde zaznaczenie na czystym obrazie (cel **0**); FN = pominięty dodatek; trafienie = część wspólna ≥ 30% pola dodatku lub ramki (ocena Programisty); czas < 1 min na obraz ~50 MB (cel ≤ 30 s).
- **Liczby progów** (zgodność doboru wzorca, FN przy limicie 5, wpływ wyboru towaru) poda Programista po krzywej z przebiegu bazowego — do tego czasu bez liczb (założenie).
- Operator ma kilka minut na auto (P2); liczby aut nie znamy, zakładamy kilkadziesiąt dziennie (P14, **założenie**).

## 5. Market Segment(s)
Jeden segment: operator RTG (Służba Celno-Skarbowa) przy stanowisku na granicy zewnętrznej UE, w trakcie kontroli (P2). Wtórnie: kontroler fizyczny, który czyta raport (P16).

## 6. Value Proposition(s)
- **Kto:** operator RTG. **Dlaczego:** musi znaleźć małą skrytkę w gąszczu konstrukcji w kilka minut. **Co dziś:** ocena „na oko” + narzędzie tylko na papierosy. **Jak:** system zaznacza do 5 różnic względem pustej naczepy tego samego typu, najpewniejsze pierwsze. **Co potem:** mniej przeoczonych skrytek, decyzje i powody w raporcie. **Alternatywy:** ACXIS i patenty na porównanie ze wzorcem (dostawcy: dane „?” niezweryfikowane), ocena ręczna.

## 7. Solution

### 7.1 Ścieżka główna (demo ≤ 2 min w pełni na aucie A — P45 A; auto B i własne zdjęcie jako krótkie ujęcia poza 2 min; dwa auta pokazu, P18)
1. Wybór auta (A: z dodatkiem — najwyżej 7 miejsc na auto = 5 widocznych + „+2 dalszych miejsc” do rozwinięcia, P47; B: czyste) albo wczytanie własnego zdjęcia (przycisk „wczytaj własne zdjęcie”, P27).
2. Operator wybiera rodzaj zgłoszonego towaru (P19, P20, P23) — 6 grup + „nie wiem”.
3. Wynik: wzorzec i badany obraz obok siebie z podświetloną różnicą (P15, P22), z boku lista zaznaczeń.
4. Klik w pozycję listy pokazuje miejsce na obu obrazach (P22).
5. Przy każdej pozycji „do kontroli” albo „odrzuć” (powód z listy) (P7, P24).
6. „+2 dalszych miejsc” (limit 7 na auto, P47) operator może rozwinąć i też zdecydować (P35). Raport z auta (E4) powstaje po decyzjach przy wszystkich miejscach, także rozwiniętych, i je zawiera (P7, P10, P35). Auto B (krótkie ujęcie poza 2 min): „brak zaznaczeń” + użyty wzorzec (P17). W 2 min mieści się auto A od wyboru towaru do raportu (P45 A).

### 7.2 Ekran główny (wariant 3 + lista z wariantu 2; makieta: https://pawelpisarek.github.io/hacknation-proba15/makieta/warianty/3/)
- **Linia nad obrazami:** wybór rodzaju towaru: drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa, „nie wiem” (zaznaczamy wszystko) (P20, P23). Bez wyboru = „nie wiem”. Każdy z 5 rodzajów ładunku (drobnica, płyny, sypkie, maszyny, meble/AGD) wygasza swoje typowe miejsca, **ale tylko wnętrze ładunku — nigdy dachu, podłogi ani ściany przedniej** (P40 A), a ekran pokazuje „wygaszone: N” (P29). **„Pusta naczepa” i „nie wiem” nic nie wygaszają** (N = 0) — miejsca w podłodze i ścianach zostają na liście (P34).
- **Pasek „wzorzec niepewny”** nad obrazami, widoczny, gdy brak naczepy tego typu i użyto najbliższej podobnej (P11, P25).
- **Dwa obrazy obok siebie** (jeden monitor, podział ekranu): wzorzec (nazwa, np. W-PL-014) i badany; różnica podświetlona; zaznaczone miejsce widać na obu.
- **Lista zaznaczeń z boku:** do 5, najpewniejsze pierwsze, z oceną pewności (P8). **Na jedno auto najwyżej 7 miejsc (P47):** wchodzą do nich najpierw miejsca w podłodze i w ścianie przy kabinie, potem najpewniejsze; kolejność na liście nadal od najpewniejszych. Gdy było więcej niż 5: „+N dalszych miejsc” (N ≤ 2) (P21) — także przy „nie wiem”. To przycisk **rozwijający** resztę listy: operator może je obejrzeć i zdecydować przy każdym (P35). Licznik „+N dalszych miejsc” jest tylko raz, przy nagłówku, nie pod listą (P36). Nagłówek zwiniętej listy: „Zaznaczenia (5) i +N dalszych miejsc” (P28; auto A: +2); nagłówek po rozwinięciu: „Zaznaczenia (N)” z liczbą wszystkich miejsc, N ≤ 7 (P41 A, P47; auto A: 7); ta sama zasada w raporcie.
- **Kolory (P37):** pewność w skali (wysoka czerwona, średnia pomarańczowa, niska żółta); napis decyzji przy pozycji w kolorze decyzji (zatwierdzone zielony, odrzucone szary). Progi w makiecie R3: ≥80% / 50–79% / <50%; przycisk „do kontroli” w neutralnym niebieskim, czerwień tylko dla wysokiej pewności, odrzucone pozycje z wyraźniejszym tekstem (P43 A).
- **Przy każdej pozycji:** „do kontroli” / „odrzuć”; odrzucenie wymaga powodu: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne (P9). Po decyzji kontur zmienia kolor (zatwierdzone zielony, odrzucone szary) i jest „cofnij decyzję” (P32).
- **Przycisk „Raport z auta”:** dopóki jakiekolwiek miejsce (także w zwiniętych „dalszych miejscach”) nie ma decyzji, jest wyszarzony, a obok stoi komunikat „Brakuje decyzji: N, w tym M w dalszych miejscach” z przyciskiem „rozwiń” (P42 A; auto A na starcie: „7, w tym 2”). Po decyzji przy wszystkich przycisk jest aktywny (P30).
- **Zmiana towaru po decyzjach (P44 B):** linia towaru działa także po decyzjach. Po zmianie lista liczy się od nowa; decyzje przy miejscach, które zostają, zachowujemy (miejsce „zostaje” = to samo miejsce: jego kontur pokrywa się z wcześniejszym i jest na liście po zmianie — decyzja przechodzi), miejsca nowe są bez decyzji, a decyzje przy miejscach, które zniknęły z listy, odpadają. Bez pytania o skasowanie.
- **Brak zaznaczeń:** komunikat „brak zaznaczeń” i pokazany użyty wzorzec (P17).
- **Podpowiedź przy podwójnej podłodze** — tylko ta część pomysłu „typowe miejsca” (P3, moment b). Pokazanie (P26): krótki dopisek „typowe miejsce skrytki: podwójna podłoga” przy pozycji listy zaznaczeń leżącej w podłodze, bez osobnego okna. Kryterium: na pokazie na aucie z dodatkiem w podłodze dopisek widać przy właściwej pozycji.

### 7.3 Raport z auta (P10, P16, §9)
Jedna strona: pole identyfikujące kontrolę (miejsce i przedmiot, §9), użyty wzorzec (+ „wzorzec niepewny”), zaznaczenia z oceną, decyzje operatora z powodem oraz wiersz „wygaszone wyborem ładunku: N” (P38; przy pustej naczepie i „nie wiem” N = 0). „Do kontroli” = samo oznaczenie w raporcie, bez komunikatu do kontrolera (P16). Decyzje zostają w raporcie. Raport jest dostępny dopiero, gdy każde miejsce — także w rozwiniętych „dalszych miejscach” — ma decyzję (P30, P35); do tego czasu przycisk jest wyszarzony z komunikatem „Brakuje decyzji: N, w tym M w dalszych miejscach” i przyciskiem „rozwiń” (P42 A). Nagłówek listy zaznaczeń w raporcie: „Zaznaczenia (N)” z liczbą wszystkich miejsc i wszystkimi pozycjami z decyzjami, bez „+N dalszych miejsc” (P41 A, P47; auto A: „Zaznaczenia (7)”). Raport liczy się z aktualnych decyzji; po zmianie towaru (P44 B) zawiera decyzje przy miejscach, które zostały, a nowe miejsca muszą dostać decyzję przed raportem.

### 7.4 Zachowania i reguły
- Wzorzec dobiera system z biblioteki (P6, P11, P19 A): pusta naczepa tego samego typu; wybór towaru ogranicza ramki na zgodnym ładunku, ale nie wygasza miejsc z ładunkiem tam, gdzie wybór go nie obejmuje (Z5); pusta naczepa i „nie wiem” nic nie wygaszają (P34); wygaszanie dotyczy tylko wnętrza ładunku, nie dachu, podłogi ani ściany przedniej (P40 A).
- Zmiana towaru po decyzjach: decyzje przy tych samych miejscach (kontur pokrywa się z wcześniejszym) zostają, nowe miejsca są bez decyzji, decyzje przy miejscach, które zniknęły z listy, odpadają (P44 B).
- Wykrywanie i zaznaczenia powstają samodzielnie; zatwierdzanie/odrzucanie to krok po wyniku wykrywania i nie wpływa na wynik wykrywania (Szef 11:21). Raport z auta (E4) tworzy się po decyzjach operatora i je zawiera (Szef 11:49). Przebieg automatyczny i partiami = „nie wiem”.
- **Wybór miejsc na auto (P47):** najwyżej 7 miejsc (5 widocznych + 2 dalsze). Kolejność pierwszeństwa przy wyborze tych 7: (1) miejsca w podłodze, (2) miejsca w ścianie przy kabinie, (3) pozostałe od najpewniejszych. Kolejność wyświetlania na liście: od najpewniejszych.
- Odrzucone miejsca **nie uczą** systemu (odrzucony pomysł 7: mogłyby ukryć skrytki, P5).
- Język ekranu: polski. Praca bez internetu i chmury; pliki .bmp ~50 MB, przetwarzanie partiami i skalowalność (§3, §9).

### 7.5 Opis makiety dla Programisty (ekrany i udawane dane)
| Ekran | Zawartość | Udawane dane |
|---|---|---|
| E1 Wybór auta | dwa auta pokazu (w 2 min tylko A, P45) + przycisk „wczytaj własne zdjęcie” (P27) | A „z dodatkiem”, B „czyste” |
| E2 Analiza (główny) | linia towaru (wygaszanie tylko wnętrza ładunku, P40; „pusta naczepa” i „nie wiem”: wygaszone 0), pasek niepewności, 2 obrazy, lista (nagłówek „Zaznaczenia (5) i +N dalszych miejsc”, po rozwinięciu „Zaznaczenia (N)”), przyciski; przycisk raportu wyszarzony z komunikatem „Brakuje decyzji: N, w tym M w dalszych miejscach” + „rozwiń” (P42); „do kontroli” niebieski (P43); zmiana towaru zachowuje decyzje przy tych samych miejscach (P44) | A: najwyżej 7 miejsc → 5 + „+2 dalszych miejsc” rozwijane (P47; w tych 7 pierwszeństwo mają podłoga i ściana przy kabinie), jedna pozycja w podłodze z dopiskiem „typowe miejsce skrytki: podwójna podłoga” (P26); B: brak zaznaczeń, wzorzec W-PL-014 |
| E3 Powód odrzucenia | lista 4 powodów | element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne |
| E4 Raport z auta | identyfikator kontroli, wzorzec, zaznaczenia, decyzje, wiersz „wygaszone wyborem ładunku: N” (P38) (dostępny po decyzjach przy każdym miejscu, także rozwiniętych, P30, P35) | numer kontroli sztuczny; auto A: tabela decyzji wszystkich miejsc (najwyżej 7, P47), nagłówek „Zaznaczenia (N)” (P41; auto A: 7) |

### 7.6 Kryteria akceptacji (z eksperymentów i ryzyk 02)
- **KA1 (Z1, najryzykowniejsze):** trafność doboru wzorca (trafny dobór = ten sam typ naczepy; sprawdzany także na zbiorze z jedną grupą naczep wyjętą z biblioteki — wtedy pasek „wzorzec niepewny”) zmierzona na zbiorze testowym i podana; przy złym typie widoczne „wzorzec niepewny”; próg po krzywej.
- **KA2 (Z2):** FN przy limicie 5 podane obok FP, także przy „nie wiem”; FN liczone na pełnej liście i na pierwszej piątce osobno.
- **KA3 (Z3):** 0 zaznaczeń na czystych w dwóch wariantach: (a) pusta naczepa bez wyboru towaru, (b) załadowana z prawidłowym wyborem. Krzywa próg → FP/FN osobno.
- **KA4 (Z4, P45 A):** ścieżka od wyboru towaru do raportu na aucie A ≤ 2 min; auto B i własne zdjęcie to osobne krótkie ujęcia poza tym limitem.
- **KA5 (Z5):** dane z 6 rodzajami ładunku; wybór towaru = wzorzec z tym ładunkiem, „nie wiem” = pusta naczepa; dodatek nadal zaznaczony po wyborze towaru; ramki na zgodnym ładunku spadają.
- **KA6 (Z6):** < 1 min na obraz ~50 MB na karcie OMENa.
- **KA7 (Z7):** podejścia B (PatchCore) i C (EfficientAD) mieszczą się w 4 GB; inaczej podejście A + mniejszy model.
- **KA8 (Z8):** FN na trudniejszym wariancie rośnie najwyżej o 10 pp, FP na czystych zostaje 0 („strojenie” = progi na łatwym wariancie; „nauka” = model z czystych, §5).
- **KA9 (P21, P35):** domyślnie widać ≤ 5 zaznaczeń + „+N dalszych miejsc”; po rozwinięciu widać wszystkie (najwyżej 7 na auto, P47) i każde da się rozstrzygnąć.
- **KA10 (P26):** na aucie z dodatkiem w podłodze właściwa pozycja listy ma dopisek „typowe miejsce skrytki: podwójna podłoga”, bez osobnego okna.
- **KA12 (P28, P36):** nagłówek zwiniętej listy brzmi „Zaznaczenia (5) i +N dalszych miejsc” (auto A: +2), nie „Zaznaczenia (N)”; licznik „dalszych miejsc” jest tylko raz. Po rozwinięciu nagłówek „Zaznaczenia (N)” (P41 A; auto A: 7).
- **KA16 (P34–P38):** pusta naczepa nic nie wygasza; „+N dalszych miejsc” (tylko przy nagłówku) rozwija się i każde miejsce dostaje decyzję przed raportem; kolory pewności: wysoka czerwona, średnia pomarańczowa, niska żółta, napis decyzji w kolorze decyzji; raport ma wiersz „wygaszone wyborem ładunku: N”.
- **KA13 (P29, P34):** wybór rodzaju towaru (poza „pusta naczepa” i „nie wiem”) wygasza jego typowe miejsca i ekran pokazuje „wygaszone: N”; „pusta naczepa” i „nie wiem” nic nie wygaszają (N = 0). Wygaszane jest tylko wnętrze ładunku, nie dach, podłoga ani ściana przednia (P40 A).
- **KA18 (P41, P43):** raport auta A ma nagłówek „Zaznaczenia (N)” z N pozycjami (N ≤ 7 wg KA19, P47); przycisk „do kontroli” jest niebieski, czerwień tylko przy wysokiej pewności (≥ 80%), tekst odrzuconych pozycji jest czytelny (wyraźniejszy kontrast).
- **KA17 (P40–P45):** wygaszanie nie obejmuje dachu, podłogi ani ściany przedniej; po rozwinięciu nagłówek „Zaznaczenia (N)”, N ≤ 7 (P47); zablokowany raport pokazuje „Brakuje decyzji: N, w tym M w dalszych miejscach” z przyciskiem „rozwiń”; zmiana towaru zachowuje decyzje przy tych samych miejscach (kontur pokrywa się z wcześniejszym), nowe miejsca są bez decyzji (P44 B); demo 2 min tylko na aucie A.
- **KA19 (P47):** na jedno auto zaznaczamy najwyżej 7 miejsc (5 widocznych + „+2 dalszych miejsc”, po rozwinięciu „Zaznaczenia (7)”); do tych 7 miejsca w podłodze i w ścianie przy kabinie wchodzą w pierwszej kolejności, resztę wypełniają najpewniejsze; kolejność na liście nadal od najpewniejszych. Auto A pokazuje 7, nie 15.
- **KA14 (P30):** raport z auta jest niedostępny, dopóki jakiekolwiek miejsce nie ma decyzji.
- **KA15 (P32):** po decyzji kontur zmienia kolor (zielony lub szary), a „cofnij decyzję” przywraca pozycję.
- **KA11 (P27, P31):** własny plik .bmp, .png lub .jpg wczytany przyciskiem „wczytaj własne zdjęcie” daje wynik z tymi samymi zasadami: ≤ 5 zaznaczeń + „+N dalszych miejsc”, wzorzec dobrany sam (z paskiem „wzorzec niepewny”, gdy trzeba).

### 7.7 Ryzyka
- Limit 5 może ukryć skrytkę poza piątką — łagodzi „+N dalszych miejsc”.
- Ocena organizatora może podać załadowane czyste naczepy — bez wyboru towaru pojawią się FP.
- Różne rozumienie „wszystko” — reguła: 5 + licznik.
- Dane sztuczne ≠ RTG KAS; podejście E (sieć na parze) tylko na zbiorze sztucznym.
- Zgodność wzorca zależy od biblioteki (mały zbiór sztuczny).

### 7.8 Założenia i pytania otwarte
Liczba aut dziennie (P14, założenie); progi Z1, Z2, Z5 — Programista po krzywej z przebiegu bazowego.

**Rozstrzygnięte (Artur, krytyk R3, wersja nocna):** P40 A wygaszanie tylko wnętrza ładunku; P41 A nagłówek „Zaznaczenia (N)” po rozwinięciu (auto A: 7, P47); P42 A blokada raportu z komunikatem „Brakuje decyzji: N, w tym M w dalszych miejscach” i przyciskiem „rozwiń”; P43 A kolory (niebieski „do kontroli”, czerwień tylko dla wysokiej pewności); **P44 B** zmiana towaru zachowuje decyzje przy miejscach, które zostają (bez pytania o skasowanie; decyzje przy miejscach, które znikną, odpadają, a raport liczy się z aktualnych decyzji, reguła w 7.2–7.4); P45 A pokaz 2 min w pełni na aucie A, auto B i własne zdjęcie jako krótkie ujęcia poza 2 min; P46 nic nie wyrzucamy; **P47 A** najwyżej 7 miejsc na auto (5 + „+2 dalszych”), z pierwszeństwem dla miejsc w podłodze i ścianie przy kabinie.

## 8. Release
**MVP (demo):** E1–E4; wynik pod linkiem bierze usługa na karcie OMENa (ustalenie Pawła ze startu), a udawane dane są tylko w makiecie. Dwa auta pokazu, 6 grup + „nie wiem”, ≤ 5 zaznaczeń + licznik, decyzje i raport.
**Tryb partiami do oceny (zadanie §6):** wejście — katalog plików .bmp; wyjście — na obraz lista ramek z pewnością (JSON) oraz obraz z zaznaczeniem; komenda `python -m rtg.wykryj --dane <katalog>`; towar „nie wiem” (nic nie wygaszane, nadal ≤ 5 + licznik).
**Poza MVP:** integracja z repozytorium RTG i urządzeniami (pole identyfikujące kontrolę zamiast), uczenie na odrzuceniach, pełna klasyfikacja towarów, realne dane KAS.

UPROSZCZENIE: biblioteka wzorców — mały zbiór sztucznych naczep — zamiast zdjęć KAS — dorobienie: duże (dane KAS).
UPROSZCZENIE: lista towarów — 6 grup + „nie wiem” — zamiast pełnej klasyfikacji — dorobienie: małe.
UPROSZCZENIE: bez integracji z repozytorium RTG i urządzeniami — pole identyfikujące kontrolę w raporcie — zamiast integracji (§9) — dorobienie: duże.
UPROSZCZENIE: logowanie i role operatora — jedno stanowisko bez logowania — ok. 2 h dorobienia (zadanie nie wymaga; Szef 11:49)

Na końcu jedna pozycja pominięta celowo: szczegółowa wersja PRD (rozwinięcie na życzenie).

<!-- skill: przeplywy-pm -->
<!-- skill: create-prd -->
