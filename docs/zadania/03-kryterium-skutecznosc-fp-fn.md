# Kryterium (faza 2): Skuteczność (FP i FN) — 40%

**Dla:** Paweł (przegląd i wybór poprawek o 07:00 w fazie 2)  
**Kryterium z wagą:** Skuteczność (FP i FN) — 40% (typ A — wynik mierzony na zbiorze jury).

## Co jest (po sondach 1–3, `docs/pm/05-sondy.md`)
- Dobór wzorca na wariancie łatwym: **100%** (`n=90`), flaga „wzorzec niepewny” dla typu spoza biblioteki: **100%** (`n=18`, 0% fałszywych w bibliotece).
- Wybór zgłoszonego towaru obniża FP o **33–35%** (H1: 382 → 247, H2: 443 → 298).
- Czas i pamięć dla 50 MB (7300×2300×24 bit): **0,52–1,10 s** (próg < 60 s) i **243–269 MB** na GTX 1050 (próg ≤ 4 GB).

## Czego brakuje (niezgodności z kryterium)
1. **Wysokie FP na pustych i załadowanych:** na czystych pustych H1 = **82**, H2 = **125** (cel: 0); na załadowanych z wyborem towaru H1 = **165**, H2 = **173**. Samym progiem (zapas 1,0 → 3,0) FP na pustych nie spada do 0 (29–47), a FN rośnie (43% → 61%).
2. **Wygaszanie wyborem towaru gasi prawdziwe dodatki (Z5):** H1 gasi **20/62**, H2 **23/70** dodatków w strefie towaru (głównie dach i ściana przednia), przez co FN pełna rośnie z 37,6–43,1% („nie wiem”) do **58,7–61,5%** („zgłoszony”).
3. **Słaba odporność na trudny wariant (`--trudny`):** FN rośnie o **+26,6 do +38,6 pp** (próg +≤ 10 pp), dobór wzorca spada do **80%** (próg ≥ 90%).
4. **H7 (PatchCore / EfficientAD) niezmierzona** — 4 przebiegi na OMENie przerwane preempcją co ~3 min (`DUE TO PREEMPTION`).

## Proponowana poprawka (strojenie — bez nowych funkcji)
1. Ograniczyć maskę wygaszania towaru do wnętrza przestrzeni ładunkowej (wyłączyć dach, podłogę i ścianę przednią) — natychmiast ograniczy spadek FN przy wyborze towaru.
2. Dodać wyrównanie lokalne / normalizację kontrastu przed dopasowaniem wzorca i liczeniem różnicy, potem przestroić próg na krzywej FP/FN (priorytet: niskie FN przy akceptowalnym FP) dla wariantu łatwego i trudnego.
3. Wykonać krótki, wznawialny pomiar H7 (PatchCore/EfficientAD ≤ 4 GB) lub zdecydować o pozostaniu przy lżejszym potoku różnica/nauka z jawnym uzasadnieniem czasu (≤ 1,1 s na 50 MB) i pamięci (≤ 269 MB) w materiałach.
