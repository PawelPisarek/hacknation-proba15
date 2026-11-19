# Recenzja zrzutów MVP — R1 (Analityk)

Zakres: `docs/zrzuty/mvp-*.png` (17 plików) wobec `docs/spec.md` (KA1–KA18) i `docs/decyzje.md` (P21, P27, P29–P38, P40–P46, reguła granicy z 15:14). Tylko braki, bez poprawek kodu.

## Braki (od najważniejszego)

1. **[produkt] Auto A ma 15 miejsc, nie 7** (`mvp-E2-A.png`, `mvp-E2-A-rozwiniete.png`, `mvp-E2-A-towar-*.png`): nagłówek „Zaznaczenia (5) i +10 dalszych miejsc”, komunikat „Brakuje decyzji: 15, w tym 10…”, po rozwinięciu „Zaznaczenia (15)”. Spec 7.1/7.5, KA9, KA18 i P41 zakładają auto A z 7 miejscami i raport „Zaznaczenia (7)”. Żaden zrzut nie pokazuje raportu A z 7 pozycjami (`mvp-E4-A.png`: 3 pozycje, towar „maszyny”), więc KA18 i demo 2 min (P45 A) nie mają potwierdzenia na zrzutach.
2. **[produkt] Brak zrzutu z dopiskiem „na granicy ładunku — nie wygaszone wyborem towaru”** (reguła 15:14; KA13, KA17): na żadnym z 6 zrzutów wyboru towaru dopisku nie widać (`mvp-E2-A-towar-maszyny.png`: miejsca 12, 14, 15 mają tylko „typowe miejsce skrytki: podwójna podłoga”). Tekst dopisku jest w kodzie, ale nie ma dowodu, że pokazuje się przy pozycji. Dodatkowo „maszyny” wygasza 12 z 15 miejsc, w tym wszystkie 5 pierwszych (78–60%), zostają 3 pozycje po 30–31% — brak zrzutu, który pokazuje, że prawdziwy dodatek w podłodze nie ginie (sonda: „jak towar” w maszynach).
3. **[produkt] Brak zrzutów stanów po decyzji**: kontur zielony/szary i „cofnij decyzję” (KA15, P32), aktywny przycisk „Raport z auta” po decyzjach przy wszystkich, także rozwiniętych (KA14, P30, P35), rozwinięta lista z decyzjami przy miejscach 6–15, zmiana towaru po decyzjach z zachowaniem decyzji (KA17, P44 B). Dostępne tylko E3 (okno powodu) i końcowy E4.
4. **[produkt] Własne zdjęcie** (`mvp-E2-wlasne.png`, `mvp-E4-wlasne.png`): przy „wzorzec niepewny” (W-kontener) wszystkie pozycje mają 98–99% (czerwone, KA18/P37 — czerwień = wysoka pewność), więc pewność nie odzwierciedla niepewności wzorca; napis „różnica podświetlona na czerwono”, a na obrazie różnicy nie widać (P15, P22); +56 dalszych miejsc i raport 61 wierszy (KA11/P21: lista 5 + licznik zachowana, ale raport nie do użycia).
5. **[produkt] Zrzuty aut A i B pokazują czerwony pasek „Tryb awaryjny: usługa na karcie OMENa nie odpowiada”** (E1 bez paska; `mvp-E2-*`, `mvp-E3.png`): brak zrzutu wyniku z żywej usługi; użytkownik pokazu i KA4/KA6 widzą błąd na ścieżce głównej.
6. **[produkt] Nagłówek listy i numery na obrazach**: „Zaznaczenia (5) i” łamie się od „+10 dalszych miejsc ▼ rozwiń” (P28, KA12: jedno zdanie „Zaznaczenia (5) i +N dalszych miejsc”; tylko `towar-plyny` w jednej linii); numery 10–15 na obrazach nakładają się i są nieczytelne (`mvp-E2-A-rozwiniete.png`, `mvp-E2-A-towar-maszyny.png`: „11/14”); numeracja z dziurami (12, 14, 15) bez wyjaśnienia.
7. **[produkt] Licznik „wygaszone: N”** (P29, KA13): wypis wygaszonych to powtarzające się nazwy bez rozróżnienia („przestrzeń ładunkowa, przód; …” ×4, `mvp-E2-A-towar-maszyny.png`), nie da się ustalić które; drobnica i meble/AGD wygaszają 0 na aucie A (zrzuty), co nie pokazuje, że „każdy z 5 rodzajów wygasza swoje typowe miejsca” (KA13).

## Wynik
7 braków (7 „produkt”, 0 „technika”). Brak zrzutu auta B z wybranym towarem (KA3b) — poza listą, nie zmienia kryteriów (B jest ujęciem poza 2 min, P45 A).

<!-- skill: przesluchanie-hackathon -->
