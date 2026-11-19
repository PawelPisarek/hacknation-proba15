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
