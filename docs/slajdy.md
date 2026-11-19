# Drugie Spojrzenie — slajdy (DRAFT po R1, później PDF)

Źródła liczb: `docs/pm/05-sondy.md` (pomiary, dane **syntetyczne**, nie obrazy KAS), `docs/decyzje.md` (P2, P40–P45), `docs/spec.md`, `docs/zadanie.md`. Co nie jest zmierzone (MVP, ksefbot.pl) — „do uzupełnienia”.
Zrzuty: `docs/zrzuty/` (makieta R3, udawane dane).

---

## 1. Drugie Spojrzenie

- Pusta naczepa obok badanej: system zaznacza do 5 miejsc, w których mogła zostać ukryta skrytka (spec §7).
- Decyzję o kontroli fizycznej podejmuje człowiek.
- Zadanie KAS „Automatyczna wyszukiwarka anomalii”.

**Pokaż:** `makieta-R3-E2-A.png` (ekran główny jako okładka).

## 2. Problem operatora

- Operator przy stanowisku RTG ma kilka minut na auto (P2, Artur).
- Mała skrytka ginie wśród detali konstrukcji naczepy; obraz oceniany „na oko”.
- Zadanie ocenia dwa błędy: fałszywy alarm (FP, czysta naczepa oznaczona) i przeoczony dodatek (FN) — `docs/zadanie.md` §6.

**Pokaż:** `makieta-R3-E1.png` (wybór auta — punkt wyjścia operatora).

## 3. Rozwiązanie

- Obok siebie: pusta naczepa tego samego typu (albo najbliższej podobnej — z ostrzeżeniem „wzorzec niepewny”) i badana.
- Podświetlone do 5 miejsc różnicy; reszta jako „+N dalszych miejsc”.
- Operator przy każdym wybiera „do kontroli” albo „odrzuć” z powodem; decyzje trafiają do raportu.
- System pokazuje, gdzie spojrzeć drugi raz — nie decyduje za operatora.

**Pokaż:** `makieta-R3-E2-A.png`.

## 4. Ścieżka operatora E1–E4

- E1 Wybór auta: dwa auta pokazu (A „z dodatkiem”, B „czyste”) albo własne zdjęcie.
- E2 Analiza: linia towaru, pasek niepewności, dwa obrazy, lista miejsc.
- E3 Powód odrzucenia: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne.
- E4 Raport z auta: numer kontroli, wzorzec, zaznaczenia, decyzje; dostępny, gdy każde miejsce ma decyzję (także w dalszych — P42).

**Pokaż:** `makieta-R3-E1.png`, `makieta-R3-E2-A.png`, `makieta-R3-E3.png`, `makieta-R3-E4.png`.

## 5. Co nowe i jak skalujemy

- Nowe: wzorzec dobierany przez system (z flagą „niepewny”), wybór zgłoszonego towaru, lista do 5 miejsc z oceną pewności, decyzje operatora w raporcie.
- Wygaszanie wyborem towaru: tylko wnętrze ładunku, nie dach, podłoga ani ściana przednia (P40 A, Artur 14:05). Czy MVP to już robi — **do uzupełnienia** (po MVP).
- Wejście: obrazy .bmp ok. 50 MB, bez konwersji (zadanie §3); praca bez internetu i chmury (spec).
- Skala zadania: ok. 200 obrazów, ok. 10 GB (zadanie §7). Ze zmierzonego czasu (max 1,10 s na obraz 50 MB, metoda różnicy, 05-sondy) wychodzi ok. 3,7 min na 200 obrazów sekwencyjnie — **wyliczenie, nie pomiar**; przetwarzanie partiami w MVP — **do uzupełnienia**.

**Pokaż:** `makieta-R3-E2-A-ladunek.png`.

## 6. Wyniki mierzone — co działa (wariant łatwy)

Dane syntetyczne, 36 grup, karta GTX 1050 (`docs/pm/05-sondy.md`):
- Dobór wzorca: 100% poprawnych (n=90), w obu metodach — **wariant łatwy**; w trudnym tylko 80% (slajd 7).
- Typ spoza biblioteki → „niepewny”: 100% (n=18), 0% w bibliotece — wariant łatwy.
- Czas na obraz 50 MB (metoda różnicy): średnio 1,02 s, max 1,10 s; metoda nauki 0,52 / 0,68 s, ale nauka na 50 MB jest **niesprawdzona** w pełnym zakresie (3 grupy; wg 05 — „Niesprawdzone”).
- Pamięć karty: 243 MB / 269 MB (limit 4 GB).

**Pokaż:** tabela z `05-sondy.md`.

## 7. Wyniki mierzone — FP i FN (słabe strony)

Metoda różnicy (H1) / nauki (H2), wariant łatwy, towar „nie wiem” / zgłoszony:
- FP na czystych pustych: **82 / 125** — cel 0 **obalony**; sam próg nie wystarcza.
- FP na załadowanych z wyborem towaru: **165 / 173** — cel 0 obalony. Wybór towaru obniża FP o ok. 35% / 33% (382 → 247, 443 → 298), ale to wciąż setki.
- FN pełna: „nie wiem” **43,1% / 37,6%**, zgłoszony **61,5% / 58,7%**; wybór towaru gasi 20/62 i 23/70 dodatków (wg 05, głównie dach i ściana przednia).
- Trudny wariant: dobór wzorca 80%, FN rośnie o 26,6 / 29,4 pp (zgł.) i 38,6 / 37,6 pp („nie wiem”).
- Wynik MVP na usłudze: **do uzupełnienia**.

**Pokaż:** wiersze „obalona” z `05-sondy.md`.

## 8. Ograniczenia

- Obrazów KAS nie mamy — zbiór sztuczny; wyniki nie zastępują prawdziwych RTG.
- Niezmierzone: PatchCore / EfficientAD (4 przebiegi karty przerwane przez inny projekt), nauka i zgłoszony towar na 50 MB.
- Makieta ma udawane dane; wykrywanie pod linkiem to MVP — **do uzupełnienia**.
- Ryzyka MVP: dostępność karty, FP na czystych, upload własnego pliku (`docs/pm/09-pre-mortem.md`).

**Pokaż:** `makieta-R3-E2-wlasne.png` (własne zdjęcie, pasek „wzorzec niepewny”).

## 9. Użyte narzędzia i zespół

- OpenMausBot (Apache-2.0) — zespół 5 botów; modele Claude (Anthropic).
- pm-skills (MIT): analiza konkurencji, założenia i ich atak, PRD, scenariusze testów, nazwa, przekaz.
- NumPy, Pillow, PyTorch (CUDA); makieta w czystym HTML/CSS/JS.
- Ludzie: Paweł (technika, wygląd, użyteczność), Artur (kształt produktu).

**Pokaż:** tabela „Użyte narzędzia” z `README.md`.

## 10. Linki i co dalej

- Repo: https://github.com/PawelPisarek/hacknation-proba15
- Makieta: https://pawelpisarek.github.io/hacknation-proba15/makieta/
- Wersja na ksefbot.pl: **do uzupełnienia**
- Dalej: lepsze wyrównanie (FP na pustych → 0), kalibracja progu „niepewny” na trudnym wariancie, MVP E1–E4 na karcie.

**Pokaż:** QR do makiety (do wygenerowania).

<!-- skill: value-prop-statements -->
