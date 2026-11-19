# Lista odbioru MVP (ksefbot.pl)

Źródła: `docs/spec.md` (KA1–KA18, §7.1–7.4), `docs/pm/09-pre-mortem.md` (działania BLOK #1, #2, #3, #5, #6, #7), `docs/pm/06-scenariusze-testow.md` (A1–A11), `app/server.js` (trasy `/api/wersja`, `/api/*` → usługa). Nie testowane — MVP w budowie. Liczb progów nie wpisuję (spec: poda Programista po krzywej).

Skróty: **A** = auto z dodatkiem (7 miejsc → 5 + „+2 dalszych miejsc”), **B** = auto czyste, **WŁ** = własne zdjęcie (przycisk „wczytaj własne zdjęcie”), **AW** = tryb awaryjny (usługa nie odpowiada → zapisany wynik aut pokazu). „curl” = sprawdzenie z terminala; kod HTTP ma wejść do meldunku. Adres: `S=https://ksefbot.pl`.

## Część 1 — wdrożenie i usługa (BLOK #1, #6)

| # | Kryterium | Co kliknąć / wczytać | Oczekiwany wynik | Komenda sprawdzająca |
|---|---|---|---|---|
| O1 | Strona wdrożona, nie stara makieta (pre-mortem #6) | otwórz `ksefbot.pl` | ekran E1 z prawdziwą aplikacją; stopka z commit SHA zgodnym z ostatnim wdrożeniem | `curl -s -o /dev/null -w "%{http_code}\n" $S/` → 200; `curl -s $S/api/wersja` → JSON z `sha` = `git rev-parse --short HEAD` |
| O2 | Wynik z usługi, nie udawany (#6) | A → wynik | w odpowiedzi `zrodlo` ≠ makieta (usługa na karcie); czas „s na karcie OMENa” widoczny w E2 | `curl -s -X POST "$S/api/analiza?auto=A" -w "\n%{http_code}\n"` → 200, JSON z `wzorzec`, `miejsca`, `czas_s` |
| O3 | Usługa odpowiada na B | B → wynik | `miejsca` puste, `wzorzec` podany | `curl -s -X POST "$S/api/analiza?auto=B" -w "\n%{http_code}\n"` → 200, `miejsca: []` |
| O4 | Praca bez internetu (zadanie §3, A10) | odłącz sieć zewnętrzną, wykonaj O5–O12 | działa tak samo, brak żądań do chmury (zakładka sieci: tylko ksefbot.pl/lokalnie); język polski | DevTools → Network: 0 żądań na obce domeny |
| O5 | Tryb awaryjny (#1) | zatrzymaj usługę na OMENie (lub zła `OMEN_URL`), kliknij A | czerwony/żółty pasek „Tryb awaryjny: usługa na karcie OMENa nie odpowiada — pokazuję zapisany wynik…”; wynik A i B z zapisu, cały przebieg do raportu działa; pasek z datą zapisu | `curl -s -X POST "$S/api/analiza?auto=A" -w "\n%{http_code}\n"` → 502 z `awaryjny: true` (ekran i tak pokazuje zapis) |
| O6 | Usługa wraca po awarii | po O5 uruchom usługę, odśwież, kliknij A | brak paska awaryjnego, wynik na żywo | jak O2 → 200 |

## Część 2 — ścieżka główna (auto A; limit 2 min od wyboru towaru do raportu, KA4/P45 A)

| # | Kryterium (KA) | Co kliknąć / wczytać | Oczekiwany wynik na ekranie | Komenda |
|---|---|---|---|---|
| O7 | E1 dwa auta + własne (P18, P27) | otwórz E1 | dwa auta pokazu (A „z dodatkiem”, B „czyste”) + przycisk „wczytaj własne zdjęcie” | `curl -s $S/api/auta` → 200, 2 pozycje |
| O8 | Linia towaru: 6 grup + „nie wiem” (A1, P20/P23) | A → linia nad obrazami | dokładnie: drobnica na paletach, płyny w beczkach, materiały sypkie, maszyny, meble/AGD, pusta naczepa, „nie wiem”; bez wyboru = „nie wiem” | — (ekran) |
| O9 | Dwa obrazy obok siebie (A2, P15/P22) | A → klik w pozycję listy | wzorzec (z nazwą, np. W-PL-014) i badany obok siebie, różnica podświetlona, miejsce widać na obu | — |
| O10 | Limit 5 + licznik (KA9, KA12, P28/P36) | A, towar „nie wiem” | lista 5 pozycji, najpewniejsza pierwsza; nagłówek dokładnie „Zaznaczenia (5) i +2 dalszych miejsc”; licznik tylko raz (przy nagłówku, nie pod listą) | JSON O2: `len(miejsca)` = 7 |
| O11 | Limit 5 przy każdym towarze (A3) | A × każdy z 6 towarów | zawsze ≤ 5 pozycji na liście | — |
| O12 | Rozwinięcie „+2” (KA9, KA12, P35/P41) | kliknij „+2 dalszych miejsc” | 7 pozycji, nagłówek „Zaznaczenia (7)”; każdą z 7 da się rozstrzygnąć | — |
| O13 | Dopisek podłogi (KA10, P26) | A, odszukaj pozycję w podłodze (też po każdym towarze z O8) | przy niej dopisek „typowe miejsce skrytki: podwójna podłoga”, bez osobnego okna; przy pozostałych brak | JSON: pozycja z `podloga: true` istnieje dla każdego towaru (z `smoke`: pole `podloga`) |
| O14 | Wygaszanie tylko wnętrza ładunku (KA13, KA17, P40 A, #3) | A × 5 towarów ładunkowych | przy każdym ekran „wygaszone: N”; żadna pozycja w dachu, podłodze, ścianie przedniej nie znika (pozycja podłogi z O13 zostaje) | JSON: `gasi` tylko dla miejsc we wnętrzu |
| O15 | „Pusta naczepa” i „nie wiem” nic nie wygaszają (KA13, KA16, P34) | A → „pusta naczepa”, potem „nie wiem” | „wygaszone: 0”, wszystkie 7 miejsc nadal (5 + „+2”) | — |
| O16 | Dodatek zostaje po wyborze towaru (KA5) | A × każdy towar | dodatek (pozycja o wysokiej pewności) nadal na liście | JSON O2 z wyborem towaru, jeśli usługa przyjmuje parametr |
| O17 | Kolory pewności (KA16, P37, P43) | A, patrz lista | ≥ 80% czerwona, 50–79% pomarańczowa, < 50% żółta; „do kontroli” niebieski, czerwień tylko ≥ 80% | — |
| O18 | „Do kontroli” (A7, P16) | kliknij „do kontroli” przy pozycji | kontur zielony, napis decyzji zielony; brak komunikatu do kontrolera; lista i kolejność bez zmian | — |
| O19 | Odrzucenie z powodem (A6, E3, P9) | kliknij „odrzuć” | E3 z 4 powodami: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne; bez wyboru powodu nic się nie zapisuje; po wyborze kontur szary, napis szary i czytelny (wyraźny kontrast, KA18) | — |
| O20 | „Cofnij decyzję” (KA15, P32) | po O18/O19 kliknij „cofnij decyzję” | pozycja wraca do bez decyzji, kolor konturu jak przed | — |
| O21 | Blokada raportu (KA14, P30, P42 A) | A, zdecyduj przy 1 pozycji z 7 | przycisk „Raport z auta” wyszarzony; komunikat „Brakuje decyzji: 6, w tym 2 w dalszych miejscach” + przycisk „rozwiń”; po rozwinięciu i decyzjach zniknie | — |
| O22 | Raport po wszystkich 7 (KA14, KA18, P41 A, P35) | zdecyduj wszystkie 7 (≥ 2 do kontroli, ≥ 2 odrzucone z różnymi powodami) → „Raport z auta” | przycisk aktywny; E4 na jednej stronie: pole kontroli, wzorzec (+ „wzorzec niepewny”, gdy był), nagłówek „Zaznaczenia (7)” z 7 pozycjami bez „+N dalszych miejsc”, ocena, decyzje z powodem, wiersz „wygaszone wyborem ładunku: N” | — |
| O23 | Raport przy pustej naczepie / „nie wiem” (P38) | jak O22, towar „nie wiem” | wiersz „wygaszone wyborem ładunku: 0” | — |
| O24 | Zmiana towaru po decyzjach (KA17, P44 B) | A, zdecyduj 3 miejsca, zmień towar (np. na „płyny w beczkach”) | bez pytania o skasowanie; decyzje przy miejscach, które zostały (kontur pokrywa się z wcześniejszym), zachowane; nowe miejsca bez decyzji; decyzje przy zniknętych odpadają; raport liczy się z aktualnych decyzji i wymaga decyzji przy nowych | — |
| O25 | Odrzucenie nie uczy (A11, P5) | odrzuć pozycję, wróć do E1, wybierz A ponownie | ta sama lista i kolejność jak wcześniej | dwa razy `curl` O2 → identyczne `miejsca` (`diff`) |
| O26 | Czas ścieżki A (KA4) | stoper od wyboru towaru do E4 | ≤ 2 min | — |

## Część 3 — auto B, własne zdjęcie, wzorzec niepewny

| # | Kryterium | Co kliknąć / wczytać | Oczekiwany wynik | Komenda |
|---|---|---|---|---|
| O27 | B: brak zaznaczeń (A4, P17, KA3, #2) | B → każdy z 7 wyborów towaru | „brak zaznaczeń” + użyty wzorzec (np. W-PL-014); lista pusta, brak „+N”. **Jeśli są zaznaczenia (FP > 0)** — odbiór „niezaliczony”; wg pre-mortem #2 jawnie zgłosić w README/demo | `curl` O3: `miejsca: []` |
| O28 | B: raport (A8) | B → „Raport z auta” | raport „brak zaznaczeń” + wzorzec, bez wymogu decyzji | — |
| O29 | WŁ .bmp ~50 MB (KA11, KA6, #5) | E1 → „wczytaj własne zdjęcie” → plik .bmp 50 MB (np. `g005_*dodatki.bmp` z biblioteki, 7300×2300) przez **publiczny adres** | wynik z tymi samymi zasadami: ≤ 5 zaznaczeń + „+N dalszych miejsc”, wzorzec dobrany sam; czas < 1 min (cel ≤ 30 s), bez 413/502/timeoutu | `curl -s -X POST --data-binary @plik.bmp "$S/api/analiza?nazwa=plik.bmp" -w "\n%{http_code} %{time_total}s\n"` → 200, czas < 60 s |
| O30 | WŁ .png i .jpg (KA11, #5) | wczytaj .png i .jpg o innym rozmiarze niż 1825×575/7300×2300 | wynik albo czytelny komunikat o formacie; bez zawieszenia; pasek „wzorzec niepewny”, gdy brak dopasowania | `curl … --data-binary @wl.png "$S/api/analiza?nazwa=wl.png"` → 200 |
| O31 | WŁ zły plik (#5) | wczytaj .txt / plik uszkodzony | czytelny komunikat „zły format”, aplikacja nie pada; można wrócić do E1 | `curl -s -X POST --data-binary @/etc/hostname "$S/api/analiza?nazwa=x.txt" -w "%{http_code}"` → 4xx z komunikatem (nie 500 bez treści) |
| O32 | WŁ tryb awaryjny | usługa wyłączona, wczytaj własny plik | czytelny komunikat „usługa niedostępna — własne zdjęcie wymaga usługi” (nie fałszywy wynik z zapisu aut) | `curl` → 502 z treścią |
| O33 | Wzorzec niepewny (A5, KA1, P11/P25) | WŁ ze zdjęciem naczepy typu, którego nie ma w bibliotece (lub A z wzorcem spoza typu) | pasek „wzorzec niepewny” nad obrazami; raport (E4) powtarza oznaczenie; przy dobrze dobranym wzorcu (A, B) paska nie ma | JSON: `niepewny: true` / `false` |

## Część 4 — tryb partiami i liczby (zadanie §6; nie ekran)

| # | Kryterium | Komenda (OMEN przez orkiestrator) | Oczekiwany wynik |
|---|---|---|---|
| O34 | Tryb partiami (§8, KA6) | `python -m rtg.wykryj --dane <katalog z .bmp>` | na obraz JSON z ramkami + obraz z zaznaczeniem; ≤ 5 + licznik; czas na obraz < 1 min; linia z pamięcią karty |
| O35 | Ocena FP/FN (KA2, KA3, KA8) | `python -m rtg.ocena --dane … --wyniki …` | podane FP (czyste: pusta naczepa i załadowana) i FN (pełna lista i pierwsza piątka osobno); bez progów wymyślonych przez Analityka — liczby tylko z wyjścia skryptu |

## Powiązanie z BLOK z pre-mortem

| Działanie BLOK (09) | Pozycje listy |
|---|---|
| #1 usługa / tryb awaryjny z zapisem | O2, O5, O6, O32 |
| #2 FP na czystych | O27, O28, O35 |
| #3 wygaszanie nie gasi dodatków | O13, O14, O15, O16 |
| #5 upload 50 MB / własny plik | O29, O30, O31 |
| #6 wdrożenie, `zrodlo` / SHA, `curl` 200 | O1, O2, O3 |
| #7 pełny zakres A1–A11, zrzuty 6 towarów + pusta naczepa | O7–O26 (A1–A11 → O8, O9, O10/O11, O27, O33, O19, O18, O22, O13, O4, O25); zrzut ekranu E2 po każdym z 7 wyborów towaru zapisać w `docs/zrzuty/` |

## Zasady odbioru
- Skrypt Programisty (05:00) przepuszcza O1–O33 (O34–O35 liczy Programista na OMENie). Pozycja bez wyniku = niezaliczona.
- Analityk po meldunku: powtórzenie O1–O3, O5, O27, O29 przez publiczny adres + przegląd zrzutów; wynik: liczba zaliczonych / N i lista niezaliczonych z oznaczeniem „produkt”/„technika”.
- Pola JSON (`zrodlo`, `podloga`, `gasi`, `niepewny`, `miejsca`) wzięte z `skrypty/dymny_usluga.sh` i pre-mortem #6; jeśli aplikacja nazywa je inaczej, Programista poprawia komendę, nie kryterium.

<!-- skill: pre-mortem -->
