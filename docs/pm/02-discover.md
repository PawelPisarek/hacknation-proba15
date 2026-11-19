# 02 — Discover (/discover)

Oparte na: `01-competitive-analysis.md`, `docs/decyzje.md` (P2–P11, moment (b)), `docs/zadanie.md`.

## Użytkownik i problem (P2–P5)
- **Operator przy stanowisku RTG**, w trakcie kontroli, ma kilka minut na auto.
- Problem: małe skrytki (najczęściej podwójna podłoga, ściana przy kabinie) giną wśród detali konstrukcji.
- Zysk: mniej przeoczonych skrytek. Przeoczony dodatek gorszy niż zbędny alarm (minuta więcej przy aucie), ale zaznaczeń na auto max 5 (P8).
- Z zadania §6: na czystym obrazie zero zaznaczeń (każdy alarm = FP).

## Pomysły wybrane przez Artura (b)
1. **Dobór wzorca** — system sam szuka najbliższej czystej naczepy tego typu w bibliotece; gdy typu brak: najbliższa podobna + ostrzeżenie „wzorzec niepewny” (P6, P11).
2. **Zaznaczenia z oceną pewności** — do 5 na auto, najpewniejsze pierwsze (P8).
3. **Zatwierdź / odrzuć jednym kliknięciem** — „do kontroli” albo odrzucenie z powodem z listy: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne (P7, P9).
4. **Widok obok siebie** — wzorzec i badany obraz, różnica podświetlona.
5. **Raport z auta** — jedna strona z zaznaczeniami i decyzjami operatora (P10).

**Uzupełnienie P19 (Artur w pokoju 11:26):** wzorzec = pusta naczepa tego samego typu (wariant A). Operator przed analizą wybiera z listy rodzaj zgłoszonego towaru (plus „pusta naczepa”), by zgodny ładunek nie dostawał ramek; bez wyboru zaznaczamy wszystko (P5). Dotyczy pomysłu 1 (dobór wzorca) i najryzykowniejszego założenia Z1.
6. **Podpowiedź przy podwójnej podłodze** — tylko ta (część pomysłu „typowe miejsca”).

Odrzucone: uczenie na odrzuceniach (odrzucone miejsca mogłyby ukryć prawdziwe skrytki — P5); pozostała część „typowych miejsc”.

## Najryzykowniejsze założenia (potwierdzone przez Artura)
| # | Założenie | Eksperyment | Kryterium |
|---|-----------|-------------|-----------|
| Z1 | System znajdzie właściwy wzorzec w bibliotece (najryzykowniejsze) | Na zbiorze testowym: dla każdego badanego obrazu sprawdzić, czy wybrany wzorzec to ten sam typ naczepy | trafność doboru zmierzona i podana; przy złym typie widoczne „wzorzec niepewny” |
| Z2 | Do 5 zaznaczeń wystarcza na złapanie dodatków | Policzyć FN przy limicie 5 | FN na zbiorze testowym podane obok FP |
| Z3 | Czyste naczepy nie dostają zaznaczeń | Przebieg na czystych parach | 0 zaznaczeń lub podany odsetek FP |
| Z4 | Operator zdąży ocenić zaznaczenia w kilka minut | Demo: przejście 1 auta ≤ 2 min | główna ścieżka w demo do 2 min |

Te eksperymenty wracają w `/write-prd` i specu jako kryteria akceptacji i ryzyka.

## Czego nie wiem o produkcie
P12 (perspektywa przeglądu rynku), P13 (co zmienić w wybranych pomysłach).

UPROSZCZENIE: biblioteka wzorców — mały zbiór sztucznych naczep — zamiast realnych zdjęć KAS — dorobienie: duże (dane KAS).

<!-- skill: przeplywy-pm -->
<!-- skill: brainstorm-ideas-new -->
<!-- skill: identify-assumptions-new -->
