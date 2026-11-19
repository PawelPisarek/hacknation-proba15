# Zadanie 01: Przeniesienie wszystkich decyzji z makiety (P2–P39) do działającego MVP

**Dla:** Programista (po zakończeniu sond 1–3 i zamknięciu krytyki makiety R3)  
**Cel:** Zbudować działającą aplikację MVP pod adresem wdrożenia (`ksefbot.pl`), która liczy prawdziwe wyniki z usługi na karcie OMENa i realizuje **każdą** decyzję z makiety R3 oraz `docs/spec.md` (KA1–KA16). Udawane dane zostają wyłącznie w makiecie (`makieta/index.html`).

## Sytuacja i źródła
- Specyfikacja: `docs/spec.md` (E1–E4, KA1–KA16, §8).
- Decyzje: `docs/decyzje.md` (P2–P39).
- Wzorzec wyglądu i zachowania ekranów: `makieta/index.html` (R3, `https://pawelpisarek.github.io/hacknation-proba15/makieta/`).
- Scenariusze testów: `docs/pm/06-scenariusze-testow.md` (A1–A11 ekrany, B1–B8 ocena).
- Liczenie: wyłącznie na karcie OMENa (`--klasa gpu-tlo`, GTX 1050 4 GB), nigdy na procesorze. Adresów sieci lokalnej nie commitujemy (repo publiczne).

## Lista decyzji z makiety do przeniesienia do MVP (wszystkie obowiązkowe)
- **P2, P4, P5, P14:** ścieżka dla operatora przy stanowisku (kilka minut na auto, pokaz ≤ 2 min); priorytet — mniej przeoczeń.
- **P6, P11, P19, P25:** system sam dobiera wzorzec z biblioteki pustych naczep tego samego typu; gdy brak tego typu — najbliższa podobna + pasek ostrzeżenia **„wzorzec niepewny”** nad obrazami (E2) i informacja w raporcie (E4).
- **P7, P9, P10, P16, P24:** przyciski „do kontroli” / „odrzuć” przy każdej pozycji listy; odrzucenie wymaga powodu z listy (E3: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne); decyzje zapisują się w raporcie z auta (E4); bez automatycznego komunikatu do kontrolera i bez uczenia modelu na odrzuceniach.
- **P8, P21, P28, P35, P36:** na liście domyślnie ≤ 5 zaznaczeń (najpewniejsze pierwsze) z oceną pewności; gdy miejsc jest więcej, licznik **„+N dalszych miejsc”** dokładnie raz, przy nagłówku listy, z możliwością rozwinięcia i podjęcia decyzji przy wszystkich miejscach.
- **P15, P22:** jeden monitor, widok obok siebie (wzorzec i badany obraz) + lista zaznaczeń z boku; klik w pozycję podświetla miejsce na obu obrazach.
- **P17:** przy braku zaznaczeń (czyste auto B) komunikat „brak zaznaczeń” i pokazany użyty wzorzec (E2 i E4).
- **P18, P27, P31:** na ekranie startowym (E1) dwa gotowe auta pokazu (A z dodatkiem, B czyste) + jeden przycisk **„wczytaj własne zdjęcie”** obsługujący `.bmp`, `.png`, `.jpg` (z tymi samymi zasadami wykrywania, doboru wzorca i raportu; nazwa wczytanego pliku w polu Kontrola w E4).
- **P20, P23, P29, P34:** linia wyboru zgłoszonego towaru nad obrazami (6 grup: drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa + „nie wiem”); każdy rodzaj ładunku wygasza swoje typowe miejsca i ekran pokazuje „wygaszone: N”; **pusta naczepa nic nie wygasza** (miejsca w podłodze i ścianach zostają na liście).
- **P26 (KA10):** przy zaznaczeniu leżącym w podłodze krótki dopisek **„typowe miejsce skrytki: podwójna podłoga”** na karcie pozycji (bez osobnego okna).
- **P30, P35:** przycisk „Raport z auta” (E4) dostępny dopiero, gdy każde widoczne miejsce (w tym rozwinięte dalsze miejsca) ma decyzję; po zmianie auta decyzje zaczynają się od zera.
- **P32:** po decyzji kontur i karta zmieniają kolor (zatwierdzone zielony, odrzucone szary) oraz jest przycisk „cofnij decyzję”.
- **P37:** pewność w skali kolorów (wysoka czerwona, średnia pomarańczowa, niska żółta), napis decyzji w kolorze decyzji.
- **P38:** w raporcie z auta (E4) zostaje wiersz „wygaszone wyborem ładunku: N”.

## Część obliczeniowa i tryb partiami
- Prawdziwa analiza obrazów z usługi na karcie OMENa (czas < 1 min / obraz ~50 MB, mieści się w 4 GB karty).
- Działający tryb partiami z wiersza poleceń (`python -m rtg.wykryj --dane <katalog>` → JSON z ramkami i pewnością + obraz z zaznaczeniem; towar „nie wiem”).
- Wdrożenie na `ksefbot.pl` (Coolify, wyłącznie aplikacja z `/data/hacknation.json`).

## Po czym poznać, że gotowe
1. Link produkcyjny (`ksefbot.pl`) odpowiada `HTTP 200` i zwraca prawdziwe wyniki z usługi na OMENie (nie udawane dane z tablicy JS).
2. Każda pozycja z listy P2–P38 powyżej działa w aplikacji MVP — potwierdzone zrzutami ekranu (w tym stan z wybranym ładunkiem, rozwinięte „+N”, czyste auto B w E2/E4, własny plik w E2/E4) albo automatycznym testem przeglądarkowym pokrywającym A1–A11.
3. Meldunek zawiera linię wyniku uruchomienia: kod HTTP wdrożenia, wynik testów ekranów A1–A11, wynik oceny B1–B8 (FP, FN@5, FN pełna, czas/obraz, pamięć karty).
4. Wpis w `docs/decyzje.md` z godziną z `date +%H:%M` (bez łączenia numeru P ze słowem „czeka”).
