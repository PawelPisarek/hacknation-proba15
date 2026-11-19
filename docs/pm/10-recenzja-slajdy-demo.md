# Recenzja slajdy/demo R1 (Analityk) — 14:07

Względem: `docs/zadanie.md`, `docs/decyzje.md` (P40–P46), `docs/pm/05-sondy.md`, `docs/spec.md`. Bez pochwał; niczego nie poprawiam.
Liczby w `docs/slajdy.md` slajdy 6–7 zgadzają się z `05-sondy.md` (sprawdzone po kolei); braki dotyczą tego, czego brakuje.

## `docs/slajdy.md` (5 braków)

1. **[produkt]** Brak podstawowych miar z zadania §6 (FP i FN). Slajdy nie podają: FN pełna (nie wiem 43,1% / 37,6%; zgł. 61,5% / 58,7%) ani FP po wyborze towaru (165 / 173 — „obalona”); slajd 6 pokazuje tylko „−35% / −33%”, co brzmi jak sukces. Ocena zadania liczy FP i FN — muszą być na slajdach 6–7 (źródło: `05-sondy.md`, wiersze 2 i „FN pełna”).
2. **[produkt]** Brak skalowalności i innowacyjności (kryteria zadania §6) oraz obsługi .bmp i przetwarzania partiami (zadanie §3). Slajdy mają tylko czas na 50 MB; żaden slajd nie mówi, jak system skaluje się na ~10 GB / ~200 obrazów ani co jest nowe (dobór wzorca + niepewność + wybór towaru). Źródło danych: `spec.md` l. 58, `materialy.md` T4.
3. **[produkt]** Slajd 7 pkt 2 („do ograniczenia do wnętrza ładunku”) i slajd 10 („dalej: wygaszanie tylko we wnętrzu”) opisują jako plan to, co Artur już rozstrzygnął (P40 A: dach, podłoga, ściana przednia nie są wygaszane). Brak informacji, że tak jest w MVP/makiecie (albo że MVP tego jeszcze nie ma — wynik na usłudze „do uzupełnienia”).
4. **[technika]** Slajd 6: „100% (n=90)” i „0% fałszywych” bez etykiety „wariant łatwy” — w `05-sondy.md` werdykt to „potwierdzona (łatwy)”; obok slajd 7 pokazuje 80% na trudnym. Czas „0,52 s metodą nauki” bez adnotacji, że nauka/zgł. na 50 MB jest niesprawdzona (`05`, „Niesprawdzone”).
5. **[technika]** Nagłówek pliku: „liczby tylko z `05-sondy.md`”, a slajdy 1–3 mają „kilka minut na auto” i „do 5 miejsc” — źródło to `decyzje.md` P2 / spec, nie `05`. Slajd 2 „każdy przeoczony dodatek to ryzyko; zbędna kontrola” bez źródła w zadaniu/ustaleniach.

## `docs/demo.md` (5 braków)

1. **[produkt]** Auto B: „Czysta naczepa — zero zaznaczeń… celem jest 0” oraz „Brak zaznaczeń” jako obietnica ekranu. `05-sondy.md`: FP na czystych pustych 82 / 125, cel 0 **obalony**; w MVP czyste auto może dać zaznaczenia. Demo i slajd 7 się wykluczają; „Czego nie obiecujemy” nie wymienia FP.
2. **[produkt]** Sprzeczność z P45 A (rozstrzygnięte 14:05): krok 9 wciska auto B i własne zdjęcie do 120 s („opcjonalnie”), a blok „Do rozstrzygnięcia przed nagraniem” i „wariant B” nadal wiszą jako otwarte; P45 A = tylko auto A w 2 min, B i własne jako osobne ujęcia.
3. **[produkt]** Krok 7–8 nie pokazuje stanów z P41/P42: po rozwinięciu nagłówek „Zaznaczenia (7)” (P41), a przy zablokowanym raporcie komunikat „Brakuje decyzji: N, w tym M w dalszych miejscach” z przyciskiem „rozwiń” (P42). Krok 7 mówi „zatwierdź/odrzuć”, a przycisk to „do kontroli” / „odrzuć” (P43: „do kontroli” niebieski, czerwień tylko dla wysokiej pewności).
4. **[technika]** „Czego nie obiecujemy: liczby… podamy dopiero po pomiarach… bez liczb w nagraniu” — pomiary już są (`05-sondy.md`) i slajdy ich używają; zdanie jest nieaktualne. Krok 1 wspomina tylko „sztuczne obrazy”, a nie, że ekran w makiecie ma udawany wynik, choć nagłówek tak mówi (kroki 3–5 bez tej uwagi przy „wygaszone: N”).
5. **[technika]** Krok 8: „Wzorzec W-PL-014 (pusta naczepa, plandeka 13,6 m)” w ujęciu auta B — „13,6 m” bez źródła w `spec.md` (jest tylko „W-PL-014”); „wygaszone: N” w kroku 3 ustalić, czy dotyczy wnętrza ładunku (P40) i czy auto A tak pokaże.

<!-- skill: brak (recenzja przejścia, bez skilla pm) -->
