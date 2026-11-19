# Drugie Spojrzenie — slajdy (DRAFT, później PDF)

Zasady: liczby tylko z `docs/pm/05-sondy.md` (dane **syntetyczne**, nie obrazy KAS); to, czego nie mamy (MVP, ksefbot.pl) — „do uzupełnienia”.
Zrzuty: `docs/zrzuty/` (makieta R3, udawane dane).

---

## 1. Drugie Spojrzenie

- Pusta naczepa obok badanej: system zaznacza do 5 miejsc, w których mogła zostać ukryta skrytka.
- Decyzję o kontroli fizycznej podejmuje człowiek.
- Zadanie KAS „Automatyczna wyszukiwarka anomalii”.

**Pokaż:** `makieta-R3-E2-A.png` (ekran główny jako okładka).

## 2. Problem operatora

- Kilka minut na auto, obraz RTG oceniany „na oko”.
- Mała skrytka ginie wśród detali konstrukcji.
- Każdy przeoczony dodatek to ryzyko; każdy fałszywy alarm to zbędna kontrola.

**Pokaż:** `makieta-R3-E1.png` (wybór auta — punkt wyjścia operatora).

## 3. Rozwiązanie

- Obok siebie: pusta naczepa tego samego typu (albo najbliższej podobnej — z ostrzeżeniem) i badana.
- System podświetla do 5 miejsc różnicy; reszta jako „+N dalszych”.
- Operator przy każdym wybiera „do kontroli” albo „odrzuć” z powodem.
- Hasło: system pokazuje, gdzie spojrzeć drugi raz — nie decyduje za operatora.

**Pokaż:** `makieta-R3-E2-A.png`.

## 4. Ścieżka E1–E2

- E1 Wybór auta: dwa auta pokazu (A „z dodatkiem”, B „czyste”) albo własne zdjęcie.
- E2 Analiza: linia towaru, pasek niepewności, dwa obrazy, lista miejsc, przyciski.
- Auto B: „brak zaznaczeń” + użyty wzorzec.

**Pokaż:** `makieta-R3-E1.png`, `makieta-R3-E2-A.png`, `makieta-R3-E2-B.png`.

## 5. Ścieżka E3–E4

- E3 Powód odrzucenia: element konstrukcji, zwykły ładunek, zakłócenie obrazu, inne.
- E4 Raport z auta: numer kontroli, wzorzec, zaznaczenia i decyzje operatora.
- Własne zdjęcie: ta sama ścieżka.

**Pokaż:** `makieta-R3-E3.png`, `makieta-R3-E4.png`, `makieta-R3-E2-wlasne.png`.

## 6. Wyniki mierzone — co działa

Dane syntetyczne, 36 grup, karta GTX 1050 (`docs/pm/05-sondy.md`):
- Dobór wzorca: 100% poprawnych (n=90), w obu metodach.
- Typ spoza biblioteki → „niepewny”: 100% (n=18), 0% fałszywych w bibliotece.
- Czas na obraz 50 MB: średnio 1,02 s (max 1,10 s) metodą różnicy; 0,52 s (max 0,68 s) metodą nauki.
- Pamięć karty: 243 MB / 269 MB (limit 4 GB).
- Wybór towaru obniża fałszywe alarmy o ok. 35% (382 → 247) i 33% (443 → 298).

**Pokaż:** tabela z `05-sondy.md` (wykres do zrobienia po MVP).

## 7. Wyniki mierzone — czego jeszcze nie osiągnęliśmy

- Fałszywe alarmy na czystych pustych: 82 (różnica) i 125 (nauka) — cel 0 **obalony**; sam próg nie wystarczy.
- Wybór towaru gasi 20/62 i 23/70 dodatków (głównie dach, ściana przednia) — do ograniczenia do wnętrza ładunku.
- Trudny wariant: dobór wzorca spada do 80%, brakujące dodatki rosną o 26,6–38,6 pp.
- Wynik MVP na usłudze: **do uzupełnienia**.

**Pokaż:** wyróżnione wiersze „obalona” z `05-sondy.md`.

## 8. Ograniczenia

- Obrazów KAS nie mamy — cały zbiór jest sztuczny; wyniki nie zastępują prawdziwych RTG.
- Niezmierzone: PatchCore / EfficientAD (4 przebiegi karty przerwane przez inny projekt), nauka i zgłoszony towar na 50 MB.
- Makieta ma udawane dane; wykrywanie pod linkiem to MVP — **do uzupełnienia**.
- Ryzyka MVP: dostępność karty, fałszywe alarmy, upload własnego pliku (`docs/pm/09-pre-mortem.md`).

**Pokaż:** `makieta-R3-E2-A-ladunek.png` (przypomina, że to udawane dane — opis na ekranie).

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
- Dalej: lepsze wyrównanie (FP na pustych → 0), wygaszanie tylko we wnętrzu ładunku, kalibracja progu „niepewny” na trudnym wariancie, MVP E1–E4 na karcie.

**Pokaż:** QR do makiety (do wygenerowania).

<!-- skill: value-prop-statements -->
