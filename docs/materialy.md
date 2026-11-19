# Materiały zadania KAS — wykrywanie „dodatków” na RTG naczep (.bmp)

Źródło wszystkiego poniżej: `docs/zadanie.md` (rozdz. w nawiasach), `docs/decyzje.md`. Liczby „wyliczone” = moje wyliczenia z liczb zadania, oznaczone jako takie.

## 1. Wymagania twarde (z zadania)

| # | Wymaganie | Źródło | Uwaga |
|---|---|---|---|
| W1 | Wejście: obrazy RTG w formacie `*.bmp` | §3 | bez konwersji do innych formatów po stronie użytkownika |
| W2 | Pliki duże, ~50 MB każdy; „w tym kompresja, przetwarzanie partiami” | §3, §7 | kompresja = np. wewnętrzna redukcja/kafelkowanie; nie wymaga formatu wyjściowego |
| W3 | Czas analizy jednego obrazu < 1 min | §7 | wyliczone: dla 200 obrazów ≤ 200 min sekwencyjnie; partie/równoległość opcjonalnie |
| W4 | Działanie samodzielne, bez interwencji człowieka, na parach/grupach obrazów | §3 | |
| W5 | Porównanie z obrazem wzorcowym (pusty/prawidłowy środek przewozowy vs z „dodatkami”) | §1, §3 | |
| W6 | Nauka wyłącznie na obrazach „prawidłowych” (bez anomalii) | §5 | trening bez etykiet anomalii → detekcja anomalii / porównanie ze wzorcem |
| W7 | Skalowalność na większe zbiory w przyszłości | §3, §6 | ocena: skalowalność |
| W8 | Docelowo bez chmury / silnika AI w internecie; w hackathonie AI wolno do tworzenia kodu | §9 | wnioskowanie lokalne, bez wywołań API zewnętrznych |
| W9 | Dane KAS = dane chronione: zakaz dalszego udostępniania/kopiowania; użycie tylko w hackathonie | §7 | nie commitować danych ani próbek do publicznego repo; slajdy/README bez prawdziwych obrazów KAS |
| W10 | Dane tylko z pendrive na stoisku KAS | §7 | patrz: brak danych (pkt 4) |

## 2. Co ma powstać (oddanie)

| Element | Obowiązkowy | Źródło |
|---|---|---|
| Model/aplikacja: wykrywa i wskazuje nieprawidłowości | tak | §3 |
| Raport z wykrytymi anomaliami — zaznaczone obszary na obrazie | tak | §3 |
| Szczegółowy opis i tytuł projektu | tak | §4 |
| Repozytorium kodu | tak | §4 |
| Prezentacja PDF, maks. 10 slajdów | tak | §4 |
| Zrzuty ekranu, linki do demo, materiały graficzne | opcjonalnie | §4 |

Kryteria oceny §6: skuteczność (FP i FN), innowacyjność, skalowalność. §8 „kryteria oceny” — odsyła do Szefa (nie ma tu treści).

## 3. Sposób sprawdzania (§6) → testy mierzalne

Organizator ma dwa zestawy: „czyste” i z „dodatkami” (nie będące elementami konstrukcyjnymi). Progi liczbowe w zadaniu **nie występują** — poniższe progi to propozycje robocze do zatwierdzenia (Artur/Paweł), nie wymóg.

| Test | Definicja | Miara | Próg (propozycja, bez źródła w zadaniu) |
|---|---|---|---|
| T1 FP na czystych | obraz z zestawu „czystych”: czy zaznaczono jakikolwiek obszar? Zadanie: „nie zaznaczała jakichkolwiek miejsc” | FP_img = liczba czystych obrazów z ≥1 alarmem / liczba czystych; dodatkowo FP_obszarów na obraz | cel 0 (literalnie z zadania); realnie raportować krzywą |
| T2 FN na „dodatkach” | obraz z dodatkiem: czy któryś zaznaczony obszar pokrywa dodatek? | FN = dodatki bez trafienia / wszystkie dodatki | do ustalenia; raportować przy progu zerowego FP |
| T3 Lokalizacja | „wskazać miejsce w formie graficznej”: IoU / pokrycie maski dodatku przez zaznaczenie | IoU ≥ 0,1–0,3 (próg trafienia — decyzja zespołu, zadanie nie podaje) | do ustalenia |
| T4 Czas | czas jednego obrazu ~50 MB od wczytania .bmp do zapisu raportu | sekundy; < 60 s (z §7) | < 60 s, cel z zapasem (np. ≤ 30 s) |
| T5 Format/rozmiar | wczytanie .bmp ~50 MB bez błędu pamięci na maszynie docelowej | pass/fail, szczyt RAM | wymaga pomiaru na OMENie |
| T6 Partia | N obrazów w jednym uruchomieniu; czas ∝ N | obrazów/min | skalowalność (innowacyjność/skalowalność w §6) |
| T7 Bez chmury | uruchomienie bez sieci | pass/fail (np. odcięty internet) | wymóg §9 |
| T8 Raport | wynik: obraz z zaznaczonymi obszarami + lista (współrzędne, wynik) | obecny dla każdego obrazu | §3 |

Skrypt oceny (do napisania — Programista): dla zbioru ze znanymi maskami dodatków liczy T1–T3, wypisuje liczby FP/FN. Uwaga: „liczba alarmów” w §6 może znaczyć per obraz lub per obszar — **niejednoznaczne, raportować oba**.

## 4. Czego nie mamy → ryzyka

Braki:
- **Brak danych KAS** (pendrive tylko na stoisku, ~200 obrazów, ~10 GB; §7). Decyzja (docs/decyzje.md 11:17): własny sztuczny zbiór naczep „czystych” i z „dodatkami”.
- Nie wiemy: rozdzielczości i głębi bitowej BMP, producenta (Nuctech vs Multicontrol — inne geometrie/skale szarości), czy pary „przed/po” są tym samym pojazdem, czy rejestracja (wyrównanie) jest potrzebna, jak wyglądają „dodatki” (rozmiar, kontrast), ile obrazów czystych jest do nauki.
- Brak treści kryteriów oceny (§8) i progów FP/FN.
- Wyliczone: 50 MB w BMP 8 bit ≈ 50 mln px; w 24 bit ≈ 16,7 mln px (zakładając brak kompresji i mały nagłówek — hipoteza do sprawdzenia na pierwszym obrazie).

| ID | Ryzyko | Skutek | Mitygacja |
|---|---|---|---|
| R1 | Zbiór sztuczny ≠ prawdziwe RTG (inna fizyka, szum, artefakty skanera liniowego) → wyniki nie przenoszą się na dane KAS | nasze FP/FN zawyżone optymistycznie | uczciwy opis w slajdach; szum, zmienna geometria, nieliniowe zniekształcenia w generatorze; model parametryzowalny, bez „wyuczenia na generatorze” |
| R2 | Przesunięcia/skalowanie/inne ułożenie pojazdu względem wzorca → fałszywe alarmy na krawędziach | wysoki FP | rejestracja obrazów (cecha/korelacja), tolerancja lokalna, porównanie z wieloma wzorcami |
| R3 | „Wzorzec” dla danej naczepy może nie istnieć (inny model pojazdu) | brak punktu odniesienia | model anomalii uczony na zbiorze czystych (nie para 1:1) + opcjonalnie para |
| R4 | Cel „zero alarmów na czystych” sprzeczny z czułością na małe skrytki | FP vs FN trade-off | raportować krzywą próg → FP/FN; próg wybierany z czystych |
| R5 | Plik 50 MB × partie: pamięć (GTX 1050 4 GB, OMEN) i czas < 1 min | niespełnione W3 | kafelkowanie, redukcja rozdzielczości w 2 skalach, pomiar na karcie |
| R6 | Dane chronione (§7) wyciekną do publicznego repo (repo publiczne) | naruszenie warunków | .gitignore na obrazy/modele z danych KAS; w repo wyłącznie sztuczne |
| R7 | Działanie bez chmury (§9) — modele pobierane z sieci przy starcie | niespełnione W8 | wagi lokalnie; test z odciętą siecią (T7) |
| R8 | Nieznane kryteria §8 → optymalizacja nie tego | | pytać Szefa; nie zakładać |
| R9 | Zawieszone P1 (kto jest kim) | niejasny adresat decyzji produktowych | czeka na Pawła (docs/decyzje.md) |
| R10 | Dodatki bardzo małe (papierosy w konstrukcji — scenariusz z §1) vs wąskie pokrycie piksela | wysoki FN | testy na dodatkach o różnej wielkości; raportować FN wg rozmiaru |

## 5. Co zadanie daje wprost jako kontekst (§1, §9)
- Obecne narzędzie KAS wykrywa papierosy; słabe przy małych ilościach w elementach konstrukcyjnych → nasz kąt: zmiany konstrukcyjne, skrytki, przeróbki (§1).
- Dostawcy urządzeń: Nuctech, Multicontrol; wdrożenie przez integratorów, integracja z repozytorium RTG; wyniki przypisane do miejsca i przedmiotu kontroli (§9) → raport powinien mieć identyfikator obrazu/kontroli (pole, nie wymóg).
- Najlepsze rozwiązanie może być testowane na dodatkowym materiale KAS (§9).

## 6. Publiczne źródła (sprawdzone wyszukiwaniem 11:2x; pozostałe z mojej wiedzy, oznaczone)

Wyszukane w tej sesji:
- ACXIS — projekt UE: zautomatyzowane porównanie obrazów RTG cargo z referencyjną bazą, rejestracja obrazu i obraz różnicowy: https://openaccessgovernment.org/automated-comparison-x-ray-images-cargo-scanning-acxis/25162 oraz https://www.openaccessgovernment.org/wp-content/uploads/2016/04/EMPA-ACXIS-ebook-web.pdf
- Jaccard i in. (UCL), „Automated detection of smuggled high-risk security threats using Deep Learning” — małe zagrożenia ≈ 0,1% pikseli obrazu ~2600×850; autoenkoder uczony na pustych kontenerach: https://arxiv.org/pdf/1609.02805
- Patenty: porównanie obrazu cargo/pojazdu z poprzednimi obrazami, wykrywanie zmian piksel po pikselu progiem różnicy, skrytki poza kontenerem (np. koło zapasowe): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10302807 , …/10768338 , …/11287391
- Deep similarity / change detection dla obrazów pojazdów (OSTI): https://www.osti.gov/servlets/purl/1877523
- PIDray — benchmark przedmiotów zabronionych w bagażu (12 kategorii; 47 677 obrazów w wersji ICCV 2021, 124 486 w wersji czasopismo — liczby zależą od wersji): https://arxiv.org/abs/2108.07020 ; kod/dane: https://github.com/bywang2018/security-dataset
- SIXray (wg tabeli PIDray ≈ 1,06 mln obrazów, 8 929 z zakazanymi — do weryfikacji w oryginale).

Z mojej wiedzy, **nie sprawdzone w tej sesji** (zweryfikować przed cytowaniem w slajdach):
- PatchCore (arXiv 2106.08265), PaDiM (arXiv 2011.08785), MVTec AD — metody/benchmark detekcji anomalii uczone tylko na obrazach „dobrych” (pasuje do W6).
- Brak znalezionego publicznego zbioru RTG pełnych naczep/skrytek z maskami — nie liczymy na gotowy zbiór; potwierdza decyzję o zbiorze sztucznym.

## 7. Wnioski do pracy dalej
1. Trzymać literalnie §6: „czyste → zero zaznaczeń”; mierzyć FP na obraz i na obszar.
2. Zbiór sztuczny musi mieć maski dodatków (inaczej T2/T3 nie do policzenia) i warianty: rozmiar, kontrast, przesunięcie pojazdu, szum, producent.
3. Do zatwierdzenia przez ludzi: progi FP/FN, definicja „trafienia”, czy liczymy alarmy per obraz/obszar (zob. §3).

<!-- skill: brak (krok 0 – materiały) -->
