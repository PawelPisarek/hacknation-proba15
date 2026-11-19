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
P20 11:31 odpowiedź (Artur w pokoju): tak — 6 grup (drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa) + „nie wiem” (wtedy zaznaczamy wszystko)
11:31 Szef: 1b poprawione po R1 (1c1f7be) → R2 Analityk
11:31 Analityk: recenzja 1b R2 — 4 braki (2 produkt: nr 1, 2; 2 technika: nr 3, 4); lista w odpowiedzi do Szefa
11:32 Szef: 1b R2 (4 braki) → poprawka Projektant, ostatnia przed R3. Rozstrzygam: (1) 02 aktualizuje do odpowiedzi P20 (6 grup + „nie wiem”); (2) przebieg automatyczny i partiami bez operatora = „nie wiem”, czyli bez wygaszania czegokolwiek; czyste obrazy w ocenie wg §6 to puste naczepy (§3), więc wzorzec pusty kontra badany pusty ma dać 0 zaznaczeń także bez wyboru. Nasz test czystych ma dwa warianty: pusta bez wyboru oraz załadowana z prawidłowym wyborem, w obu cel 0. Ryzyko: ocena organizatora może podać załadowane czyste, wtedy pojawią się FP — zapisane jako ryzyko; (3) próg Z8: FN na trudniejszym wariancie rośnie najwyżej o 10 pkt proc., a FP na czystych zostaje 0. „Strojenie” to dobór progów i parametrów na łatwym wariancie; „nauka” to model z obrazów czystych (§5). Progi Z1, Z2 i Z5 wpisuje Programista po krzywej z przebiegu bazowego; (4) przywrócić zdanie, że wynik na danych sztucznych nie dowodzi skuteczności na RTG z KAS i że mówimy to wprost.
11:32 Projektant: 1b R2 poprawione w docs/pm/02 (P20, Z3 dwa warianty, Z8, ograniczenie danych sztucznych)
11:33 Szef: 1b poprawione po R2 (cd48c25) → R3 Analityk (ostatnia)
11:33 Analityk: recenzja 1b R3 — 2 braki (2 produkt: nr 1, 2); lista w odpowiedzi do Szefa
11:33 Szef: 1b R3 — 2 braki → po 3 rundach pytam Artura (P21, przez Projektanta). Brak 1 (sprzeczność sekcji P19 z Z3a) rozstrzygnięty o 11:32: wariant „pusta bez wyboru” wchodzi do oceny czystych — Projektant poprawia sekcję P19. Brak 2 → P21.
P21 11:33 Artur: gdy towar „nie wiem” (albo nie wybrany), pokazujemy też najwyżej 5 zaznaczeń, najpewniejsze pierwsze — czy wszystkie? Rekomendacja: zawsze najwyżej 5; „wszystko” znaczy tylko, że nie pomijamy ładunku; resztę braków zapisujemy jako ryzyka w specu i idziemy dalej — czeka
11:34 Projektant: 1b R3 pkt 1 — sekcja „W MVP wprost z P19” i Z3 poprawione w 02 (pusta bez wyboru wchodzi do oceny czystych), kosmetyka tabeli; P21 zadane Arturowi w pokoju (linia P21 z 11:33, ntfy już poszło)
P21 11:34 odpowiedź (Artur w pokoju): zawsze najwyżej 5 zaznaczeń, najpewniejsze pierwsze; gdy system wie, że było więcej, pokazuje „+N dalszych miejsc”
11:36 Szef: P21 odpowiedziane (Artur w pokoju 11:34) — 1b: Projektant wpisuje P21 i ryzyka R3 do 02, po meldunku ze skillem 1b zamknięte, start pytań (c)
11:36 Projektant: 1b — P21 (5 + „+N dalszych miejsc”) i ryzyka R3 wpisane w docs/pm/02; 1b zamknięte, start pytań (c)
11:36 Projektant: (c) — N1–N5 z 03 mają odpowiedzi (pytania 14–18); szkice 3 wariantów ekranu w docs/pm/03 przekazane Szefowi; pytania o układ po linkach do makiet
11:37 Szef: 1b zamknięte (778bb05, znacznik przeplywy-pm w 02). Szkice 3 wariantów (03) → Programista robi 3 makiety wariantów przed pytaniem o wybór; potem /write-prd
11:40 Programista: warianty https://pawelpisarek.github.io/hacknation-proba15/makieta/warianty/1/ https://pawelpisarek.github.io/hacknation-proba15/makieta/warianty/2/ https://pawelpisarek.github.io/hacknation-proba15/makieta/warianty/3/ (curl 200×3; udawane dane: auto A z dodatkiem — 7 miejsc, 5 + „+2 dalszych miejsc”; auto B czyste — „brak zaznaczeń” z wzorcem W-PL-014)
11:40 Szef: warianty https://pawelpisarek.github.io/hacknation-proba15/makieta/warianty/1/ https://pawelpisarek.github.io/hacknation-proba15/makieta/warianty/2/ https://pawelpisarek.github.io/hacknation-proba15/makieta/warianty/3/
P22 11:41 Artur: który wariant ekranu — 1) jeden obraz na cały ekran, 2) najpierw lista zaznaczeń, 3) porównanie obok siebie (makiety: .../makieta/warianty/1/, /2/, /3/)? Rekomendacja: 3 — czeka
P22 11:42 odpowiedź (Artur w pokoju): wariant 3 (porównanie obok siebie) + z wariantu 2 lista zaznaczeń z boku (najpewniejsze pierwsze); klik w pozycję pokazuje miejsce na obu obrazach
P23 11:42 Artur: gdzie na ekranie wybór rodzaju towaru — nad obrazami przed analizą czy w oknie na starcie? — czeka
P24 11:42 Artur: przyciski „do kontroli”/„odrzuć” przy każdej pozycji listy czy jedna para pod obrazami dla wybranej? — czeka
P25 11:42 Artur: wzorzec niepewny — pasek ostrzeżenia nad obrazami czy znaczek przy nazwie wzorca? — czeka
P23 11:43 odpowiedź (Artur w pokoju): wybór rodzaju towaru nad obrazami, w jednej linii
P24 11:43 odpowiedź (Artur w pokoju): „do kontroli”/„odrzuć” przy każdej pozycji listy (wynika z P7)
P25 11:43 odpowiedź (Artur w pokoju): „wzorzec niepewny” jako pasek nad obrazami
11:47 Szef: (c) zamknięte (P22–P25) → /write-prd docs/spec.md zlecone Projektantowi; kamień ~11:45 przekroczony
11:48 Projektant: /write-prd gotowe — docs/spec.md (+ docs/pm/04-write-prd.md) na 01–03 i P1–P25; ekran: wariant 3 + lista z boku, towar nad obrazami, decyzje przy pozycjach, pasek wzorca niepewnego
11:48 Szef: 2 /write-prd zameldowane (docs/spec.md 7749bbd, znacznik przeplywy-pm) → recenzja przejścia R1 Analityk
11:49 Analityk: recenzja 2 R1 (spec.md 7749bbd) — 3 braki (2 produkt: nr 1, 2; 1 technika: nr 3); lista w odpowiedzi do Szefa
11:49 Szef: recenzja 2 R1 — 3 braki. Brak 1 (kolejność decyzji i raportu) rozstrzygam: wykrywanie i zaznaczenia powstają samodzielnie; raport z auta (E4) tworzy się po decyzjach operatora i je zawiera (Artur: „decyzje w raporcie z auta”, P7); „krok po raporcie” z 11:21 = po wyniku wykrywania. Brak 3 (logowanie): UPROSZCZENIE: logowanie i role operatora — jedno stanowisko bez logowania — ok. 2 h dorobienia (zadanie nie wymaga). Brak 2 (wygląd podpowiedzi przy podwójnej podłodze) → Artur, P26.
P26 11:49 Artur: gdy zaznaczone miejsce leży w podłodze, jak operator ma zobaczyć podpowiedź „typowe miejsce skrytki: podwójna podłoga”? Rekomendacja: krótki dopisek przy tej pozycji na liście zaznaczeń (bez osobnego okna); sprawdzimy go na pokazie na aucie z dodatkiem w podłodze — czeka
11:50 Projektant: spec po recenzji 2 R1 — pkt 1 (kolejność: raport po decyzjach), pkt 3 (logowanie wg Szefa 11:49), przykład 7→5+2 jako udawane dane; pkt 2 rozstrzygnięty przez P26 (odpowiedź 11:50)
11:50 Szef: krok 6 zameldowany (docs/hacktribe.md, znaczniki product-name, value-prop-statements). Nazwa: „Drugie Spojrzenie” (rekomendacja Prezentera) — przyjmuję; Prezenter zmienia nazwę w README. Recenzja tekstu: Analityk.
P26 11:50 odpowiedź (Artur w pokoju): tak — krótki dopisek „typowe miejsce skrytki: podwójna podłoga” przy pozycji na liście zaznaczeń, bez osobnego okna
11:51 Analityk: recenzja hacktribe R1 (hasło 98/120, opis 380/500, nazwa 17/30) — brak braków zmieniających zakres lub kryteria
11:51 Szef: spec poprawiony po R1 (65e2f20) → R2 Analityk (pkt podpowiedzi czeka na odpowiedź Artura)
11:51 Analityk: recenzja 2 R2 (spec.md 65e2f20) — brak braków zmieniających zakres lub kryteria (podpowiedź przy podwójnej podłodze: P26 odpowiedziane 11:50, spec jeszcze bez dopisku — do wpisania przez Projektanta, nie brak R2)
11:52 Szef: hacktribe R1 — brak braków (2 kosmetyczne → Prezenter). Spec R2 — brak braków; P26 (11:50) dopisuje Projektant; potem recenzja odbiorcy (Programista)
11:52 Projektant: spec z P26 — 7.2, E2 (auto A, pozycja w podłodze z dopiskiem), KA10, nagłówek P1–P26
11:53 Analityk: krok 3 — docs/pm/05-zalozenia-atak.md (ranking Z1–Z8, 3 sondy, 5 ataków); liczby progów to propozycje do potwierdzenia
11:54 Szef: krok 2 /write-prd — pętla przejścia zamknięta (R2 czyste, P26 w specu: 7.2, E2, KA10); recenzja odbiorcy → Programista
11:55 Szef: krok 3 — 05-zalozenia-atak.md przyjęty (znaczniki ok); sondy 1–3 → Programista (OMEN, po linii bazowej); propozycja z ataku 3 czeka na wynik sondy 2, dopiero wtedy ewentualne pytanie do Artura
11:55 Szef: krok 4 zlecony — test-scenarios → Analityk (docs/pm/06), historyjki → Projektant (docs/pm/07)
11:55 Programista: recenzja odbiorcy speca R1 — 4 braki: (1, produkt) §8 „MVP E1–E4 z udawanymi danymi” to makieta — brak: czy MVP pod linkiem liczy naprawdę na OMENie i czy operator wczytuje własny .bmp (E1 ma tylko 2 auta); rek.: 2 auta pokazu + „wczytaj plik .bmp”, wynik z OMENa; (2, technika) brak trybu partiami do oceny §6: wejście katalog .bmp, wyjście na obraz ramki z pewnością (JSON) + obraz z zaznaczeniem, komenda; rek.: python -m rtg.wykryj --dane <katalog> → JSON + PNG, towar „nie wiem” (7.4); (3, technika) KA1 bez definicji trafnego doboru wzorca (ta sama naczepa czy ten sam typ) i bez zbioru z naczepą spoza biblioteki (pasek „wzorzec niepewny”); rek.: trafny = ten sam typ, zbiór z jedną grupą wyjętą z biblioteki; (4, technika) KA5 bez metody i danych dla wyboru towaru — generator ma tylko „pusta”/„ta sama”, bez 6 grup; rek.: generator z 6 rodzajami ładunku, wybór towaru = wzorzec/model z tym ładunkiem, „nie wiem” = pusta naczepa
11:55 Projektant: docs/pm/07-historyjki.md — 10 historyjek H1–H10 z odwołaniami do KA1–KA10
11:56 Szef: recenzja odbiorcy R1 — brak 1a (MVP liczy naprawdę): rozstrzygnięte ustaleniem Pawła ze startu — MVP pod linkiem bierze wynik z usługi na karcie OMENa, dane udawane tylko w makiecie; braki 2–4 (technika, wynikają z zadania) wg rekomendacji Programisty; poprawia Projektant w docs/spec.md, potem R2 odbiorcy
P27 11:56 Artur: czy operator może wczytać własne zdjęcie naczepy, czy pokazujemy tylko dwa przygotowane auta? (rekomendacja: dwa auta do pokazu + przycisk „wczytaj własne zdjęcie”) — czeka
11:56 Analityk: krok 4a — docs/pm/06-scenariusze-testow.md (A1–A11 ekrany, B1–B8 ocena, 10 braków skryptu → Programista)
11:56 Szef: krok 4 — 06-scenariusze-testow.md i 07-historyjki.md przyjęte (znaczniki ok); 06 część C (braki skryptu oceny) → Programista przed kodem MVP; ekrany (część A) testuje Programista testem przeglądarkowym makiety/MVP; progi „propozycja” (dobór ≥ 90%, FN@5 − FN@pełna ≤ 5 pp) przyjęte jako robocze do pomiaru
P27 11:57 odpowiedź (Artur w pokoju): tak — dwa auta do pokazu + przycisk „wczytaj własne zdjęcie”
11:57 Szef: spec po odbiorcy R1 (4 poprawki w §8, KA1, KA5) → recenzja odbiorcy R2 (Programista); pytanie 27 do Artura otwarte (odpowiedź 11:57)
11:57 Programista: recenzja odbiorcy speca R2 — brak braków zmieniających zakres lub kryteria (P27 z 11:57 — „wczytaj własne zdjęcie” w E1 — do dopisania w specu, nie brak R2)
11:58 Szef: recenzja odbiorcy R2 czysta — krok 2 zamknięty; P27 → E1 dopisuje Projektant; krok 5 makieta R1 wg speca (wariant 3 + lista) → Programista przed MVP
11:58 Projektant: spec z P27 — E1 (przycisk „wczytaj własne zdjęcie”), KA11, nagłówek P1–P27; historyjka H1b w 07
12:07 Szef: README „Użyte narzędzia” przyjęte; przeplywy-pm zostaje jako skill zespołu (poza pm-skills)
12:09 Programista: wynik bazowy 0P (OMEN GTX 1050, przebieg na karcie, H1 roznica / H2 nauka): ta_sama (12 grup, 1825x575): H1 FP=30 FN=45/56 0,23 s/obraz; H2 FP=20 FN=23/56 0,18 s. P19 pusta-vs-załadowana: H1 FP=1208 (1196 na załadowanych) FN=12/55; H2 FP=197 (196 na załadowanych, 1 na pustych) FN=1/55 0,30 s. Pełne 50 MB: H1 FP=0 FN=3/3 0,80 s; H2 FP=0 FN=1/3 0,34 s, karta max 243 MB. Obalone: H1 „FP=0 przy FN ≤ 30%”. Potwierdzone: H2 < FN niż H1; H3 czas < 60 s (≤ 1 s). Wniosek: bez modelu zgłoszonego towaru (P19) załadowany towar daje FP — następny krok: wzorzec/model z wybranym towarem.
12:09 Szef: linia bazowa 0P przyjęta (H2 nauka prowadzi); kolejność bez zmian: 06 C → sondy 1–3 → makieta R1
