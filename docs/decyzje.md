# Decyzje

11:17 Szef: start próby 15; zadanie KAS „Automatyczna wyszukiwarka anomalii” zapisane w docs/zadanie.md; typ A (wynik mierzony na zbiorze testowym: FP/FN).
11:17 Szef: dane — własny sztuczny zbiór .bmp (naczepy „czyste” i z „dodatkami”), bo zdjęć KAS nie mamy (uwaga ludzi).
11:17 Szef: liczenie przez orkiestrator; sieć/model na karcie OMENa (--klasa gpu-tlo), nigdy na procesorze; reszta --maszyna dowolna; ≥ 2 hipotezy na przebieg na karcie.
11:17 Szef: aplikacja pod linkiem dostaje wynik z usługi na karcie OMENa (sieć lokalna); adresów sieci lokalnej nie commitujemy (repo publiczne).
11:17 Szef: nazwa zespołu „Hackathon”.
P1 11:17 Paweł: kto jest kim — Paweł technika, Artur produkt, nikt więcej? — czeka
P1 11:18 odpowiedź: tak — Paweł technika (rozmowa z Szefem), Artur produkt (pokój Produkt), nikt więcej
11:19 Projektant: pominięte (jaki to produkt/kategoria, których konkurentów, perspektywa, do czego analiza) — z zadania: wyszukiwarka anomalii RTG KAS, konkurenci to dostawcy sprzętu i podejścia do porównania obrazów
P2 11:19 Artur: kto jest głównym użytkownikiem — operator przy stanowisku RTG czy analityk później z repozytorium? — czeka
P3 11:19 Artur: jaki problem ma dziś użytkownik przy ocenie obrazu (czas, przeoczone skrytki)? — czeka
P4 11:19 Artur: co użytkownik ma zyskać najbardziej — mniej przeoczonych skrytek czy mniej czasu na obraz? — czeka
P5 11:19 Artur: co gorsze — alarm na czystej naczepie czy przeoczony dodatek? — czeka
P6 11:19 Artur: wzorzec do każdego obrazu wskazuje użytkownik czy system dobiera go sam? — czeka
P7 11:19 Artur: po alarmie użytkownik zatwierdza/odrzuca miejsca czy tylko czyta raport? — czeka
11:20 Szef: 1a — znacznik przeplywy-pm jest; recenzja przejścia R1 → Analityk
P2 11:21 odpowiedź (Artur w pokoju): operator przy stanowisku, w trakcie kontroli, ma kilka minut na auto
P3 11:21 odpowiedź (Artur w pokoju): tak — najczęściej podwójna podłoga albo ściana przy kabinie
P4 11:21 odpowiedź (Artur w pokoju): mniej przeoczonych skrytek
P5 11:21 odpowiedź (Artur w pokoju): przeoczony dodatek gorszy; zbędny alarm = minuta więcej przy aucie; zaznaczeń na auto kilka, nie kilkadziesiąt
P6 11:21 odpowiedź (Artur w pokoju): system dobiera wzorzec sam (operator zwykle nie ma czystego zdjęcia tej samej naczepy) — inaczej niż rekomendacja
P7 11:21 odpowiedź (Artur w pokoju): operator zatwierdza („do kontroli”) albo odrzuca jednym kliknięciem; przy odrzuceniu powód z listy — inaczej niż rekomendacja
11:21 Projektant: P7 zmienia zakres (ekran zatwierdzania, lista powodów) — wygrywa odpowiedź Artura; do Szefa: sprzeczność z „bez udziału człowieka” w zadaniu do rozstrzygnięcia przy P8+ jeśli zajdzie potrzeba
11:20 Analityk: recenzja 1a R1 — 5 braków (2 produkt: nr 2, 4; 3 technika: nr 1, 3, 5); lista w odpowiedzi do Szefa
P8 11:23 Artur: ile zaznaczeń na jedno auto jest jeszcze OK (3, 5, 7)? — czeka
P9 11:23 Artur: jakie powody odrzucenia na liście (np. element konstrukcji, ładunek zwykły, zakłócenie obrazu, inne)? — czeka
P10 11:23 Artur: czy zatwierdzone „do kontroli” i odrzucone miejsca zostają zapisane w raporcie z auta? — czeka
P11 11:23 Artur: skąd system bierze wzorzec — z biblioteki czystych naczep tego samego typu? — czeka
11:21 Szef: P7 a „bez interwencji człowieka” — bez sprzeczności: wykrywanie i raport działają samodzielnie; zatwierdzanie/odrzucanie przez operatora to krok po raporcie i nie wpływa na wynik wykrywania.
11:22 Szef: 1a R1 — 5 braków → Projektant poprawia cały plik; brak 4 (perspektywa, kto szuka konkurentów) rozstrzygam: z zadania — porównanie funkcji i sposobu działania, nie cena/rynek; konkurentów szukamy sami poza wymienionymi
P8 11:25 odpowiedź (Artur w pokoju): do 5 zaznaczeń na auto, najpewniejsze pierwsze
P9 11:25 odpowiedź (Artur w pokoju): lista powodów: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne
P10 11:25 odpowiedź (Artur w pokoju): tak, decyzje operatora zostają w raporcie z auta
P11 11:25 odpowiedź (Artur w pokoju): tak, z biblioteki; gdy brak tego typu — najbliższa podobna z ostrzeżeniem „wzorzec niepewny”
11:25 Artur w pokoju (moment b): wybrane pomysły 1 dobór wzorca, 2 zaznaczenia z oceną pewności, 4 zatwierdź/odrzuć z powodem, 5 widok obok siebie, 6 raport z auta; 3 tylko podpowiedź przy podwójnej podłodze; 7 odrzucony (odrzucone miejsca mogłyby ukryć prawdziwe skrytki — P5); najryzykowniejsze założenie: dobór wzorca
11:25 Projektant: z zadania §6 (Analityk, R1 pkt 2) — na czystym obrazie nie wolno zaznaczyć żadnych miejsc, każdy alarm to FP; ustalone, nie pytanie. Z P5 „kilka zaznaczeń” = górna granica P8 (5), nie cel na czystym aucie
P12 11:25 Artur: perspektywa przeglądu rynku — porównujemy wg funkcji dla operatora czy wg ceny/wejścia na rynek? — czeka
P13 11:25 Artur: co w wybranych pomysłach zmienić i czy któryś z odrzuconych (3 poza podwójną podłogą, 7) warto wziąć w części? — czeka
11:23 Projektant: pominięte (perspektywa porównania, kto szuka konkurentów) — decyzja Szefa 11:22: z zadania (narzędzie dla KAS, nie produkt na rynek) perspektywa = funkcje i sposób porównania, nie cena/rynek; konkurentów szukamy sami poza wymienionymi; nie pytamy Artura (P12 dublował — do zamknięcia przez Szefa)
11:23 Projektant: 1a R1 poprawione w docs/pm/01 (5 pozycji: prior art ACXIS/patenty, FP zależne od P5, podejście E tylko na zbiorze sztucznym, perspektywa, źródła/niezweryfikowane)
11:23 Programista: dane syntetyczne (rtg/generator.py, skill dummy-dataset) — grupa = jedna naczepa (typ plandeka/chłodnia/kontener + ułożenie towaru); obrazy grupy różnią się jak kolejne prześwietlenia (przesunięcie, skala wzdłuż przejazdu ±1,5%, wzmocnienie, szum, pasy detektora, przesunięcie palet). Role: nauka (4 czyste, pierwszy = wzorzec), czysty (test), dodatki (1–2 z: podwójna podłoga, ściana przednia, rama, dach, w towarze). Pełny rozmiar 7300x2300x24 bit ≈ 50 MB. Założenie łatwe do zmiany: wzorzec ma ten sam towar co badany (para „ta sama naczepa”); wariant „pusta vs załadowana” dorobimy, gdy spec tak powie.
11:23 Programista: ocena (rtg/ocena.py) wg rozdz. 6 — czysty: każda ramka = FP; dodatki: dodatek bez trafienia = FN; trafienie = część wspólna ≥ 30% pola dodatku lub ramki; ramki obok dodatków liczone osobno (FP_dod). Czas/obraz = od wczytania do ramek (bez budowy modelu grupy).
11:23 Programista: przebieg bazowy na karcie OMENa sprawdza naraz: H1 „różnica po wyrównaniu do jednego wzorca” daje FP=0 na czystych przy FN ≤ 30%? H2 „model nauczony na 4 czystych (średnia+rozrzut piksela)” daje mniej FN niż H1 przy FP=0? H3 czas/obraz ~50 MB < 60 s na GTX 1050?
11:23 Szef: 1a R2 → Analityk; docs/pm/02-discover.md powstał przed zamknięciem 1a — wersja robocza, recenzja 1b dopiero po zamknięciu 1a
P12 11:24 odpowiedź (Artur w pokoju): według funkcji dla operatora (zgodne z decyzją Szefa 11:22)
P13 11:24 odpowiedź (Artur w pokoju): nic więcej do zmiany — wybór z 11:25 zostaje (3 tylko podwójna podłoga, 7 odrzucony)
11:24 Analityk: recenzja 1a R2 — 5 braków (1 produkt: nr 2; 4 technika: nr 1, 3, 4, 5); lista w odpowiedzi do Szefa
P14 11:24 Artur: ile aut/dzień i ile minut na auto? — czeka
P15 11:24 Artur: jeden monitor czy wzorzec i badany obok siebie? — czeka
P16 11:24 Artur: po „do kontroli” samo oznaczenie w raporcie czy komunikat dla kontrolera? — czeka
P17 11:24 Artur: co operator widzi, gdy nic nie zaznaczono? — czeka
P18 11:24 Artur: pokaz na jednym aucie czy na dwóch (czyste + z dodatkiem)? — czeka
11:25 Szef: 1a R2 — 5 braków → Projektant poprawia; brak 2 (jaki wzorzec: pusta naczepa vs z podobnym ładunkiem) → pytanie do Artura przez Projektanta; R3 = ostatnia runda
P19 11:25 Artur: z czym system porównuje auto — A) z obrazem pustej naczepy tego samego typu (ładunek zgłoszony operator oznacza sam) czy B) z naczepą tego typu z podobnym ładunkiem? Rekomendacja A (tak opisuje to zadanie, pustych obrazów jest najwięcej); „wzorzec niepewny” widać, gdy brak naczepy tego typu — czeka
11:25 Projektant: 1a R2 poprawione w docs/pm/01 (macierz: wyróżnienia i §9, „?” zamiast „tak/niejasne”, linki, wzorzec zależny od P19)
11:25 Szef: 1a poprawione po R2 (2025dc1) → R3 Analityk; pytanie o wzorzec — linia P19 wyżej
P14 11:26 odpowiedź (Artur w pokoju): kilka minut na auto (z P2); liczby aut nie zna — zakładamy kilkadziesiąt dziennie (założenie)
P15 11:26 odpowiedź (Artur w pokoju): jeden monitor, podział ekranu
P16 11:26 odpowiedź (Artur w pokoju): samo oznaczenie w raporcie
P17 11:26 odpowiedź (Artur w pokoju): tak — komunikat „brak zaznaczeń” i pokazany użyty wzorzec
P18 11:26 odpowiedź (Artur w pokoju): dwa auta (czyste + z dodatkiem)
P19 11:26 odpowiedź (Artur w pokoju): A — wzorzec to pusta naczepa tego samego typu; operator przed analizą wybiera rodzaj zgłoszonego towaru z listy (plus „pusta naczepa”), by zgodny ładunek nie dostawał ramek; bez wyboru zaznaczamy wszystko (P5)
11:26 Analityk: recenzja 1a R3 — brak braków zmieniających zakres lub kryteria (wzorzec zależny od P19, nie brak)
11:26 Szef: P19 (A) → Programista: generator i ocena także w wariancie pusta naczepa vs załadowana; Projektant: 03-przed-prd i pytania (c) wstrzymane do zamknięcia 1b
11:26 Projektant: P19 (A: pusta naczepa + wybór zgłoszonego towaru z listy) wpisane w docs/pm/01 i 02; docs/pm/03 nie meldowany, nowych pytań (c) nie zadaję do zamknięcia 1b (zlecenie Szefa)
11:27 Szef: 1a zamknięte po R3 (brak braków); 1b /discover → Projektant (02-discover na końcowym 01 i P2–P19)
11:27 Projektant: 1b — docs/pm/02-discover.md dokończony na końcowym 01 i P2–P19; kosmetyka R3 w 01
11:28 Szef: 1b zameldowane (5a30b18, znacznik jest) → recenzja przejścia 1b R1 Analityk
11:29 Analityk: recenzja 1b R1 — 5 braków (3 produkt: nr 1, 2, 3; 2 technika: nr 4, 5); lista w odpowiedzi do Szefa
11:29 Szef: 1b R1 (5 braków) → poprawka Projektant. Rozstrzygam: (1) wybór zgłoszonego towaru jest w MVP — wynika z odpowiedzi Artura P19, nie z Z5; (2) czyste obrazy testowe oceniamy z prawidłowo wybranym towarem, cel Z3 = 0 zaznaczeń na czystych (zadanie §6), bez „podanego odsetka”; (4) pokaz ≤ 2 min to ustalenie Szefa; (5) do założeń: < 1 min na obraz ~50 MB i zmieszczenie B/C w 4 GB karty, Z6 zastąpić mierzalnym. Brak (3) treść listy towarów → Artur przez Projektanta (P20).
P20 11:30 Artur: jakie rodzaje zgłoszonego towaru ma mieć lista dla operatora? Rekomendacja: 6 grup — drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa — czeka
11:30 Projektant: 1b R1 poprawione w docs/pm/02 (5 pozycji; lista towarów zależna od P20)
