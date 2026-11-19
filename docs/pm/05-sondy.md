# Wyniki sond 1–3 (docs/pm/05-zalozenia-atak.md)

Dane syntetyczne `rtg.generator --wariant biblioteka` (36 grup, 1825×575, biblioteka pustych wzorców plandeka/chłodnia/kontener,
co 6. grupa „skrzyniowa” spoza biblioteki, 5 towarów + pusta, 109 dodatków w 6 rodzajach), trudny wariant `--trudny`
(kontrast ×0,65, zakłócenia ×2), pełny rozmiar 7300×2300×24 bit (50,4 MB) dla czasu i pamięci.
Wykrywanie na karcie OMENa (GTX 1050, przebieg 18:28–18:33), ocena `rtg.ocena` bez karty. Punkt pracy: zapas progu 1,1.
H1 = różnica z jednym wzorcem, H2 = nauka (średnia/odchylenie). „nie wiem” = bez wyboru towaru, „zgł.” = wybrany zgłoszony towar.

| Sonda | Hipoteza / próg (propozycja) | H1 zmierzone | H2 zmierzone | Werdykt |
|---|---|---|---|---|
| 1 | dobór wzorca = właściwy typ ≥ 90% | 100% (n=90) | 100% (n=90) | potwierdzona (łatwy) |
| 1 | „niepewny” dla typu spoza biblioteki | 100% spoza (n=18), 0% w bibliotece | to samo | potwierdzona |
| 1 | FP = 0 na czystych pustych | **82** | **125** | obalona |
| 2 | FP = 0 na załadowanych z wyborem towaru | **165** | **173** | obalona |
| 2 | wybór towaru obniża FP (nie wiem → zgł.) | 382 → 247 (−35%) | 443 → 298 (−33%) | potwierdzona |
| 2 | wybór towaru nie gasi dodatków (Z5) | gasi **20/62** dodatków w strefie towaru (głównie dach, ściana przednia) | gasi **23/70** | obalona |
| 2 | FN@5 − FN pełna ≤ 5 pp | nie wiem: 66,1−43,1 = **23 pp**; zgł.: 64,2−61,5 = 2,7 pp | nie wiem: 60,6−37,6 = **23 pp**; zgł.: 2,8 pp | obalona przy „nie wiem” |
| 2 | FN pełna (bez progu w 05; dla porządku) | nie wiem 43,1%, zgł. 61,5% | nie wiem 37,6%, zgł. 58,7% | — |
| 3 | trudny wariant: FN +≤ 10 pp | zgł. **+26,6 pp**, nie wiem **+38,6 pp** | zgł. **+29,4 pp**, nie wiem **+37,6 pp** | obalona |
| 3 | trudny wariant: dobór ≥ 90% | **80%** | **80%** | obalona |
| 3 | czas < 60 s na obraz 50 MB | śr. 1,02 s, max 1,10 s | śr. 0,52 s, max 0,68 s | potwierdzona |
| 3 | pamięć karty ≤ 4 GB (metoda obecna) | 243 MB | 269 MB | potwierdzona |
| 3 | pamięć PatchCore / EfficientAD ≤ 4 GB (H7) | — | — | **niezmierzona**: przebieg przerywany (patrz niżej) |

Krzywa próg → FP/FN (łatwy, nie wiem): zapas 1,0→3,0 obniża FP H1 499→305 i H2 490→302, ale FP na czystych pustych nie spada do 0
(H1 29, H2 47 przy 3,0), a FN H1 rośnie 43→61%. Samym progiem FP = 0 nie da się osiągnąć — fałszywe alarmy są w miejscach
konstrukcji/ładunku, nie w szumie. Pełny rozmiar 50 MB (3 grupy): FP na pustych 0, FN 0/4 (nie wiem), wybór towaru gasi 4/4 (H1).

**Wnioski dla MVP:** (1) dobór wzorca i flaga „niepewny” działają — zostają; (2) próg nie wystarcza: potrzebne lepsze wyrównanie
(rozciągnięcie lokalne / siatka) zanim FP na pustych spadnie do 0; (3) wygaszanie wyborem towaru musi być ograniczone do wnętrza
ładunku, bez dachu i ściany przedniej (Z5 — dziś łamie); (4) trudny wariant psuje dobór (80%) — próg „niepewny” do kalibracji na trudnym.

**Niesprawdzone:** H7 (PatchCore/EfficientAD) i nauka/zgł. na 50 MB — 4 przebiegi na karcie (17:59, 18:25, 18:33, 18:43 czasu OMENa)
przerwane „DUE TO PREEMPTION” przez wyłączne pomiary czasu innego projektu co ~3 min.
