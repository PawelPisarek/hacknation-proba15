# Krytyk makiety R3 (Analityk)

Wejście: https://pawelpisarek.github.io/hacknation-proba15/makieta/ (HTTP 200), 9 zrzutów `docs/zrzuty/makieta-R3-*.png`, `docs/spec.md`, P2–P38 z `docs/decyzje.md`, wniosek 13:46 w `docs/zadania/01-mvp-z-makiety.md`. Ocenione tylko zrzuty i spec.

**Ocena: 7/10**

## Braki (od najważniejszego)

1. **[produkt] E2-A-ładunek — „drobnica na paletach” wygasza „podłoga, tył” (miejsce 7).** Podłoga to typowa skrytka (P3, P26), a wniosek z sond (01-mvp, pkt 2; 05-sondy: Z5 obalone, wybór gasi 20/62 i 23/70 prawdziwych dodatków) mówi: wygaszać tylko wnętrze ładunku, nigdy dachu/podłogi/ściany przedniej. Makieta pokazuje zachowanie, które MVP ma wykluczyć; spec 7.2/KA13 (P29) nie wyłącza stref konstrukcyjnych.
2. **[technika] `docs/spec.md` nie dogonił P34–P38 poza KA16.** 7.2: „każdy rodzaj towaru wygasza swoje typowe miejsca” bez wyjątku „pusta naczepa nic nie wygasza” (P34); „+N dalszych miejsc (licznik, nie zaznaczenie)” wobec P35 (rozwijane, decyzja przy każdym); wiersz „wygaszone wyborem ładunku: N” (P38) tylko w KA16, nie w 7.3 i tabeli E4 (7.5); nagłówek „P1–P27/P33”; KA9 „zawsze ≤ 5 zaznaczeń” przeczy rozwinięciu do 7 (KA16).
3. **[produkt] E2-A (rozwinięte) i E4 auta A — liczba przeczy temu, co widać.** Nagłówek „Zaznaczenia (5)” nad 7 wierszami; w E4 „5 + 2 dalszych miejsc” nad tabelą 7 decyzji. Po rozwinięciu P28/P35 dają dwie liczby dla tej samej listy; spec nie mówi, jak nagłówek wygląda po rozwinięciu.
4. **[produkt] E3 — przyczyna blokady raportu niewidoczna.** „bez decyzji: 6” przy 5 widocznych pozycjach (1 zdecydowana, więc widać 4 bez decyzji). Brakujące 2 to zwinięte „+2 dalszych miejsc” — jedyny sygnał to mały żółty znaczek przy nagłówku (P30, P35, P36). Operator nie wie, czemu przycisk jest wyszarzony.
5. **[produkt] Kolory kolidują z P37 (E2-A-ładunek, E2-własne).** Czerwony przycisk „do kontroli” przy każdej pozycji, także 47% (żółta), pokrywa się z czerwoną „wysoką pewnością”; odrzucone pozycje w E2-A (np. 7: 31% żółta na szarym) są nieczytelne (niski kontrast).
6. **[produkt] Zmiana towaru po decyzjach — nie pokazana ani w specu.** Linia towaru zostaje aktywna po zatwierdzeniu wszystkich miejsc (E2-A); nie wiadomo, czy decyzje (P32) i raport się zerują, ani co z miejscami nowo wygaszonymi/przywróconymi (P29, P34). Do tego raport nie ma wiersza o decyzjach cofniętych/zresetowanych.
7. **[technika] Brak zrzutu z wybraną „pusta naczepa”** — główna zmiana R3 (P34: nic nie wygaszane, podłoga i ściany zostają na liście) nie da się ocenić ze zrzutów (są tylko „drobnica” i „nie wiem”); płyny, sypkie, maszyny, meble też bez zrzutu (P29: „każdy z 6”).
