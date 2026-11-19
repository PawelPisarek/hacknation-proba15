# Scenariusz demo (≤ 2 min) — **DRAFT**

> **DRAFT** — oparty na makiecie R3 i `docs/spec.md` §7.1. Zostanie zaktualizowany do MVP (wynik z usługi na karcie OMENa, ten sam układ ekranów). Nagrywa człowiek.

**Link:** makieta https://pawelpisarek.github.io/hacknation-proba15/makieta/ (po MVP: link z wersji na ksefbot.pl — do wpisania).
**Czas łącznie: 120 s** (zapas ~0 s — nie improwizować; jeśli brakuje czasu, skróć krok 6). W 2 min tylko auto A (P45 A, Artur 14:05); auto B i własne zdjęcie to osobne krótkie ujęcia poniżej.
**Uwaga prawdziwościowa:** dane to sztuczne obrazy; w makiecie wynik jest udawany. Mówimy to wprost w kroku 1; „wygaszone: N” i „+N dalszych miejsc” (kroki 3–4) to udawane dane pokazu.

## Przed nagraniem
- Otwórz link, ekran E1 „Wybierz auto”. Przygotuj plik zdjęcia/obrazu do ujęcia „Własne zdjęcie” (.bmp, .png lub .jpg).
- Okno przeglądarki na pełny ekran; kolumna listy zaznaczeń z boku widoczna bez przewijania.

## Kroki

| # | Czas | Co klikamy / pokazujemy | Co mówimy |
|---|---|---|---|
| 1 | 0–15 s (15) | E1 „Wybierz auto” — widać Auto A, Auto B i „Wczytaj własne zdjęcie”. | „Operator RTG ma kilka minut na auto (ustalenie P2), a małą skrytkę łatwo przeoczyć wśród konstrukcji naczepy. Nasze narzędzie porównuje obraz z pustą naczepą tego samego typu i zaznacza do 5 podejrzanych miejsc. Pracujemy na sztucznych obrazach — zdjęć KAS nie mamy, a wynik w makiecie jest udawany.” |
| 2 | 15–25 s (10) | **Auto A — z dodatkiem**: „Analizuj” → E2. | „Auto A, z ukrytym dodatkiem.” |
| 3 | 25–40 s (15) | Linia „Zgłoszony towar”: klik **maszyny**. Wskaż napis „wygaszone: N” nad listą (N odczytać z ekranu). | „Operator wybiera zgłoszony towar. System wygasza typowe miejsca tego ładunku — tylko wnętrze ładunku, nie dach, podłogę ani ścianę przednią (ustalenie P40) — a ekran mówi, ile wygasił. Bez wyboru jest „nie wiem” i zaznaczamy wszystko.” |
| 4 | 40–60 s (20) | Dwa obrazy obok siebie: wzorzec W-PL-014 po lewej, badane auto po prawej, różnica podświetlona. Wskaż nagłówek „Zaznaczenia (5) i +2 dalszych miejsc”. | „Po lewej pusta naczepa wzorcowa, po prawej badana. Różnice są podświetlone, a lista z boku ma najwyżej 5 pozycji, najpewniejsza pierwsza. Reszta to licznik „dalszych miejsc”, nie kolejne alarmy.” |
| 5 | 60–75 s (15) | Klik pozycji 1 (podłoga, przód): miejsce świeci na obu obrazach; wskaż dopisek „typowe miejsce skrytki: podwójna podłoga”. | „Klik w pozycję pokazuje to miejsce na obu obrazach. Tu najpewniejsze: podłoga — i podpowiedź, że to typowe miejsce skrytki.” |
| 6 | 75–90 s (15) | Pozycja 1: **do kontroli** (niebieski; czerwień tylko dla wysokiej pewności, P43). Pozycja 2: **odrzuć** → okno z powodem → „element konstrukcji”. Wskaż „cofnij decyzję”. | „Operator decyduje przy każdym miejscu: „do kontroli” albo „odrzuć” z powodem. Decyzję można cofnąć. Odrzucenia niczego nie uczą systemu, żeby nie ukryć prawdziwej skrytki.” |
| 7 | 90–105 s (15) | Klik „Raport z auta →” przy niepełnych decyzjach: przycisk zablokowany, komunikat **„Brakuje decyzji: N, w tym M w dalszych miejscach”** (P42; liczby z ekranu). Klik „rozwiń” → nagłówek zmienia się na **„Zaznaczenia (7)”** (P41). Szybko: „do kontroli” / „odrzuć” przy pozostałych. | „Raport czeka na decyzję przy każdym miejscu — także w dalszych. Komunikat mówi, ilu brakuje; „rozwiń” pokazuje wszystkie, a nagłówek liczy teraz siedem.” |
| 8 | 105–116 s (11) | „Raport z auta →”: jedna strona — numer kontroli, użyty wzorzec, zaznaczenia, decyzje z powodem. | „Raport z auta zawiera użyty wzorzec, zaznaczenia z oceną i decyzje operatora z powodem.” |
| 9 | 116–120 s (4) | Zostań na raporcie. | „Dziękujemy. Auto B i własne zdjęcie — w osobnych ujęciach.” |

Rozstrzygnięte (Artur w pokoju, 14:05): **P45 A** — w pełni tylko auto A w 2 min; auto B i własne zdjęcie jako krótkie ujęcia poza limitem (niżej).

## Dodatkowe ujęcia (poza limitem 2 min — do slajdów)

### Auto B — czyste (≈ 10 s)
- E1 → **Auto B — czyste** → „Analizuj”.
- Na ekranie makiety: wzorzec W-PL-014 i obrazy bez podświetleń — **to udawany wynik**. Pomiar na czystych pustych naczepach (`docs/pm/05-sondy.md`, sonda 1) dał **82 fałszywe alarmy (różnica) i 125 (nauka)**; cel „FP = 0” nie został osiągnięty. W MVP czyste auto może więc dostać zaznaczenia.
- Mówimy: „To czyste auto. W makiecie wynik jest udawany; w pomiarze na sztucznych danych fałszywych alarmów na czystych naczepach mamy wciąż 82 i 125 — to nasz główny punkt do poprawy.”

### Własne zdjęcie (≈ 15 s)
- E1 → **Wczytaj własne zdjęcie** → plik .bmp / .png / .jpg.
- Widać pasek „Wzorzec niepewny — w bibliotece brak naczepy tego typu, użyto najbliższej podobnej” (w makiecie wynik udawany).
- Mówimy: „Własny obraz dostaje te same reguły: do 5 zaznaczeń plus licznik. Gdy w bibliotece nie ma tego typu naczepy, mówimy to wprost: wzorzec niepewny.”

## Czego nie obiecujemy
- Skuteczności na prawdziwych RTG KAS (dane sztuczne).
- Zera fałszywych alarmów: pomiary (`docs/pm/05-sondy.md`) dają FP na czystych 82 / 125 i FN pełną 43,1% / 37,6% (towar „nie wiem”). Liczby w nagraniu tylko z tego pliku, jako dane syntetyczne.

## Do uzupełnienia po MVP
- Link do wersji na ksefbot.pl; czasy kroków zmierzone na działającej usłudze (OMEN, cel ≤ 30 s na obraz — ewentualny czas oczekiwania wpisać jako osobny krok).
- Liczby „wygaszone: N”, „+N dalszych miejsc”, „Brakuje decyzji: N” — odczytać z ekranu MVP (w makiecie to udawane dane pokazu); sprawdzić, że w MVP wygaszanie nie obejmuje dachu, podłogi i ściany przedniej.
