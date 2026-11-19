# Scenariusz demo (≤ 2 min) — **DRAFT**

> **DRAFT** — oparty na makiecie R3 i `docs/spec.md` §7.1. Zostanie zaktualizowany do MVP (wynik z usługi na karcie OMENa, ten sam układ ekranów). Nagrywa człowiek.

**Link:** makieta https://pawelpisarek.github.io/hacknation-proba15/makieta/ (po MVP: link z wersji na ksefbot.pl — do wpisania).
**Czas łącznie: 120 s** (zapas ~0 s — nie improwizować; jeśli brakuje czasu, pomiń krok 7).
**Uwaga prawdziwościowa:** dane to sztuczne obrazy; w makiecie wynik jest udawany. Mówimy to wprost (krok 1 i 9).

## Przed nagraniem
- Otwórz link, ekran E1 „Wybierz auto”. Przygotuj plik zdjęcia/obrazu do kroku 8 (.bmp, .png lub .jpg).
- Okno przeglądarki na pełny ekran; kolumna listy zaznaczeń z boku widoczna bez przewijania.

## Kroki

| # | Czas | Co klikamy / pokazujemy | Co mówimy |
|---|---|---|---|
| 1 | 0–15 s (15) | E1 „Wybierz auto” — widać Auto A, Auto B i „Wczytaj własne zdjęcie”. | „Operator RTG ma kilka minut na auto, a małą skrytkę łatwo przeoczyć wśród konstrukcji naczepy. Nasze narzędzie porównuje obraz z pustą naczepą tego samego typu i zaznacza do 5 podejrzanych miejsc. Pracujemy na sztucznych obrazach — zdjęć KAS nie mamy.” |
| 2 | 15–25 s (10) | **Auto A — z dodatkiem**: „Analizuj” → E2. | „Auto A, z ukrytym dodatkiem.” |
| 3 | 25–40 s (15) | Linia „Zgłoszony towar”: klik **maszyny**. Wskaż napis „wygaszone: N” nad listą. | „Operator wybiera zgłoszony towar. System wygasza typowe miejsca tego ładunku, a ekran mówi, ile wygasił. Bez wyboru jest „nie wiem” i zaznaczamy wszystko.” |
| 4 | 40–60 s (20) | Dwa obrazy obok siebie: wzorzec W-PL-014 po lewej, badane auto po prawej, różnica podświetlona. Wskaż listę: nagłówek „Zaznaczenia (5)” + przycisk „+N dalszych miejsc”. | „Po lewej pusta naczepa wzorcowa, po prawej badana. Różnice są podświetlone, a lista z boku ma najwyżej 5 pozycji, najpewniejsza pierwsza. Reszta to licznik „dalszych miejsc”, nie kolejne alarmy.” |
| 5 | 60–75 s (15) | Klik pozycji 1 (podłoga, przód): miejsce świeci na obu obrazach; wskaż dopisek „typowe miejsce skrytki: podwójna podłoga”. | „Klik w pozycję pokazuje to miejsce na obu obrazach. Tu najpewniejsze: podłoga — i podpowiedź, że to typowe miejsce skrytki.” |
| 6 | 75–95 s (20) | Pozycja 1: **do kontroli** (kontur zielony). Pozycja 2 lub inna: **odrzuć** → okno z powodem → wybierz „element konstrukcji”. Wskaż „cofnij decyzję”. | „Operator decyduje przy każdym miejscu: „do kontroli” albo „odrzuć” z powodem. Decyzję można cofnąć. Odrzucenia niczego nie uczą systemu, żeby nie ukryć prawdziwej skrytki.” |
| 7 | 95–105 s (10) | Rozwiń „+N dalszych miejsc”, zdecyduj pozostałe (zatwierdź/odrzuć szybko). | „Dalsze miejsca też dostają decyzję — raport jest dostępny dopiero, gdy każde ją ma.” |
| 8 | 105–115 s (10) | „Raport z auta →”: jedna strona — kontrola, użyty wzorzec, zaznaczenia, decyzje z powodem. | „Raport z auta zawiera użyty wzorzec, zaznaczenia z oceną i decyzje operatora z powodem.” |
| 9 | 115–120 s (5) | (opcjonalnie, tylko jeśli starczy czasu: wróć do „wybór auta”). | „Auto B — czyste — pokazuje „brak zaznaczeń”; własne zdjęcie wczytujemy jednym przyciskiem. Dziękujemy.” |

> **Do rozstrzygnięcia przed nagraniem:** w limicie 2 min mieszczą się **auto A + raport**. Auta B i własnego zdjęcia nie da się pokazać w pełni w tym samym nagraniu — **wariant A (rekomendowany):** jedno nagranie 2 min z A, a B i własne zdjęcie jako dodatkowe 2 krótkie ujęcia (kroki poniżej) dołączone do slajdów. **Wariant B:** skrócić A (kroki 5–7 po 5 s mniej) i dołożyć B + własne w ~25 s.

## Dodatkowe ujęcia (poza limitem 2 min — do slajdów lub jako B, jeśli Szef zdecyduje)

### Auto B — czyste (≈ 10 s)
- E1 → **Auto B — czyste** → „Analizuj”.
- Widać komunikat „Brak zaznaczeń. Użyty wzorzec: W-PL-014 (pusta naczepa, plandeka 13,6 m)” i obrazy bez podświetleń.
- Mówimy: „Czysta naczepa — zero zaznaczeń. Fałszywy alarm to strata czasu przy aucie, więc celem jest 0.”

### Własne zdjęcie (≈ 15 s)
- E1 → **Wczytaj własne zdjęcie** → plik .bmp / .png / .jpg.
- Widać pasek „Wzorzec niepewny — w bibliotece brak naczepy tego typu, użyto najbliższej podobnej” (w makiecie wynik udawany).
- Mówimy: „Własny obraz dostaje te same reguły: do 5 zaznaczeń plus licznik. Gdy w bibliotece nie ma tego typu naczepy, mówimy to wprost: wzorzec niepewny.”

## Czego nie obiecujemy
- Skuteczność na prawdziwych RTG KAS (dane sztuczne).
- Liczby (FP/FN, czas na obraz) — podamy dopiero po pomiarach Programisty; do tego czasu bez liczb w nagraniu.

## Do uzupełnienia po MVP
- Link do wersji na ksefbot.pl; czasy kroków zmierzone na działającej usłudze (OMEN, cel ≤ 30 s na obraz — ewentualny czas oczekiwania wpisać jako osobny krok).
- Liczba „wygaszone: N” i „+N dalszych miejsc” — odczytać z ekranu po zmianach R3/MVP (w opisie wyżej to udawane dane pokazu).
