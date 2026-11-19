# 01 — Analiza konkurencji i podejść (/competitive-analysis)

**Data**: 2026-11-19 (sobota, start próby 15)
**Produkt**: wyszukiwarka anomalii na obrazach RTG naczep/ciężarówek (KAS) — porównanie badanego obrazu .bmp ze wzorcem, zaznaczenie różnic. Działa lokalnie (bez chmury), wynik z usługi na karcie OMENa (GTX 1050 4 GB).
**Źródła**: `docs/zadanie.md`, `docs/decyzje.md`, wyszukiwanie w sieci 19.11 (linki na dole). Czego nie dało się potwierdzić — oznaczone „założenie”.

## Przegląd rynku
Operatorzy RTG oceniają obrazy ręcznie; dostawcy sprzętu dokładają moduły AI dwóch rodzajów: wykrywanie zagrożeń (ATD, szukanie znanych przedmiotów, np. broni czy papierosów) oraz weryfikacja zawartości względem zgłoszenia/manifestu (ACV). KAS ma już detektor papierosów, który słabo radzi sobie z małymi skrytkami w konstrukcji pojazdu — tu potrzebne jest porównanie ze wzorcem i wykrywanie „czegoś, czego nie powinno być”, a nie szukanie znanego przedmiotu. Żadne znalezione źródło nie opisało gotowego, jawnego narzędzia porównującego obraz pojazdu z obrazem wzorcowym u Nuctech/Multicontrol (założenie: takie moduły mogą istnieć, ale są zamknięte).

## Konkurenci bezpośredni (ten sam użytkownik: operator RTG / służba celna)
| Konkurent | Pozycjonowanie | Mocna strona | Słaba strona |
|---|---|---|---|
| Nuctech — platforma inspekcji z AI | dostawca urządzeń KAS; głęboka sieć trenowana także na danych symulowanych | jest już w urządzeniu, integracja z obrazem | zamknięty; nie wiadomo, czy porównuje ze wzorcem (założenie: nie jawnie) |
| Multicontrol — oprogramowanie urządzeń | drugi dostawca KAS | jak wyżej | jak wyżej; dane nieznane |
| Rapiscan (Insight/eXaminer) | analiza kształtu, tekstury, intensywności + głębokie wykrywanie przedmiotów; zgodność z manifestem (patent) | dojrzały, certyfikowany | porównuje ze zgłoszeniem, nie z pustym wzorcem pojazdu; chmura/licencje |
| Smiths Detection | algorytmy wykrywania materiałów wybuchowych (bagaż), certyfikacje | renoma | nie dotyczy dużych pojazdów (według znalezionych źródeł) |
| Obecny detektor papierosów KAS | wykrywanie jednego rodzaju towaru | działa w produkcji | słaby przy małych ilościach w konstrukcji pojazdu (z zadania) |

## Konkurenci pośredni — podejścia do porównania obrazów (uruchamialne na GTX 1050 4 GB)
| Podejście | Jak działa | Plusy | Minusy / ryzyko |
|---|---|---|---|
| A. Różnica pikseli po dopasowaniu (rejestracja + różnica / SSIM) | wyrównuje wzorzec i badany obraz, odejmuje, progowanie, ramki | proste, szybkie, wyjaśnialne, bez uczenia; dobre na parę „przed/po” | wrażliwe na przesunięcie, skalę, szum i różne ułożenie naczepy → fałszywe alarmy |
| B. PatchCore / pamięć fragmentów „czystych” (anomalib) | uczy się na samych czystych obrazach, szuka fragmentów nietypowych | bardzo dobry na jakość wykrywania, uczenie w minutach; mapa ciepła | pamięć rośnie z liczbą obrazów (potrzebne ograniczenie, np. 10% fragmentów); pamięć 4 GB — do sprawdzenia; obrazy 50 MB trzeba ciąć na kafle |
| C. EfficientAD (mała sieć „uczeń–nauczyciel”) | wykrywanie anomalii w milisekundach | ~2–5 ms/obraz w publikacji (na dużej karcie); mały model | dłuższe uczenie (godziny w jednym teście); wynik na 1050 — założenie, do zmierzenia |
| D. Autoenkoder / rekonstrukcja | uczy się odtwarzać „czysty” obraz, różnica = anomalia | prosty, mały | rozmyta rekonstrukcja → fałszywe alarmy na krawędziach |
| E. Para obrazów w jednej sieci (porównanie wzorzec ↔ badany, wykrywanie zmian) | sieć dostaje oba obrazy, zwraca maskę zmian | najlepiej pasuje do „wzorzec vs badany” | potrzebuje obrazów z oznaczonymi dodatkami (sztuczny zbiór — możemy wygenerować) |
| F. Nadzorowane wykrywanie obiektów (YOLO itp.) | szuka znanych „dodatków” | szybkie, dokładne na znanych typach | nie wykryje nieznanych skrytek; jak obecny detektor KAS |

## Macierz funkcji
| Zdolność | Nasz produkt (cel) | Dostawcy sprzętu | Różnica pikseli (A) | PatchCore (B) | EfficientAD (C) |
|---|---|---|---|---|---|
| Porównanie ze wzorcem | tak | niejasne | tak | pośrednio (uczy się „normy”) | pośrednio |
| Zaznaczenie miejsca na obrazie | tak (ramki/maska) | tak | tak | tak (mapa ciepła) | tak |
| Bez chmury / bez internetu | tak | różnie | tak | tak | tak |
| Duże pliki ~50 MB, partie | tak (kafle) | tak | tak | tak (kafle) | tak (kafle) |
| Mało fałszywych alarmów | cel | zależy | słabo | dobrze | dobrze |
| Wykryje nieznany dodatek | tak | tylko znane | tak | tak | tak |

## Mapa pozycjonowania (oś: wiedza o wzorcu ↔ szukanie znanych rzeczy; oś: wyjaśnialność)
- Dostawcy ATD i YOLO: „szukają znanych rzeczy”, niska wyjaśnialność.
- Różnica pikseli: „porównuje ze wzorcem”, wysoka wyjaśnialność, wysoka fałszywa alarmowość.
- PatchCore/EfficientAD: „uczą się normy”, średnia wyjaśnialność (mapa ciepła).
- **Nasza przestrzeń**: porównanie ze wzorcem + uczenie normy + wynik, który operator rozumie („tu coś doszło”) — połączenie A (dopasowanie, różnica) z B/C (ocena, czy różnica jest istotna).

## Okazje do wyróżnienia
1. **Wzorzec + norma razem** — dopasowanie pary obrazów i ocena nietypowości fragmentów ogranicza fałszywe alarmy bez uczenia na „dodatkach”.
2. **Pokazanie różnic, nie werdyktu** — operator dostaje zaznaczone miejsca i może je odrzucić; wspiera, nie zastępuje.
3. **Skalowanie na duże pliki** — kafle i partie, przetwarzanie < 1 min na obraz (wymóg zadania).
4. **Wszystko lokalnie** — wymóg wdrożenia KAS (bez chmury).

## Zagrożenia
1. **Dostawcy dodadzą porównanie ze wzorcem we własnym oprogramowaniu** — dla nas: wartość w jakości i niezależności od dostawcy (Nuctech i Multicontrol).
2. **Różne ułożenie i długość naczep** — dopasowanie wzorca może zawieść; ryzyko dla wyniku (fałszywe alarmy).
3. **Dane sztuczne ≠ rzeczywiste RTG** — wynik na własnym zbiorze nie dowodzi skuteczności na danych KAS (założenie do powiedzenia na pokazie).

## Rekomendacje
- **Postawić na**: porównanie ze wzorcem (A) jako baza + ocena nietypowości (B lub C) jako filtr fałszywych alarmów.
- **Dorównać w**: czytelnym raporcie z zaznaczonymi miejscami i licznikiem alarmów na obraz.
- **Pominąć**: pełne wykrywanie znanych przedmiotów (F) i integrację z urządzeniami dostawców.
- Na karcie 4 GB: kafle obrazów i małe modele; do zmierzenia przez Programistę (założenie: PatchCore z ograniczoną pamięcią lub EfficientAD-S mieszczą się).

## Czego nie wiem o produkcie (pytania do Artura — moment (a))
Rozstrzyga zadanie (nie pytamy): praca bez internetu, dane sztuczne, działanie bez człowieka, format .bmp, ekran po polsku.
1. Kto jest głównym użytkownikiem: operator przy stanowisku RTG czy ktoś analizujący obrazy później z repozytorium?
2. Jaki ma dziś problem z oceną obrazu — co mu zabiera czas lub czego nie widzi?
3. Co zyska: mniej przeoczonych skrytek czy mniej czasu na obraz?
4. Co gorsze dla użytkownika: alarm na czystej naczepie czy przeoczony dodatek?
5. Czy użytkownik ma sam wskazać wzorzec dla każdego obrazu, czy system ma go dobierać z zebranych wzorców?
6. Co użytkownik robi po alarmie: zatwierdza/odrzuca miejsce, czy tylko czyta raport?

## Źródła
- Rapiscan — technologia (ATD/ACV, algorytmy): https://rapiscan-ase.com/resource-center/technology
- Przegląd analizy obrazów RTG cargo: https://openaccess.library.uitm.edu.my/Record/ndltd-bl.uk-oai-ethos.bl.uk-747225/Description
- EfficientAD (opóźnienie 2,2–4,5 ms na RTX A6000; PatchCore ~148 ms): https://arxiv.org/pdf/2303.14535
- PatchCore a pamięć karty (anomalib): https://github.com/openvinotoolkit/anomalib/discussions/1935
- Brak wyników o jawnym porównaniu ze wzorcem u Nuctech/Smiths — oznaczone jako założenie.

<!-- skill: przeplywy-pm -->
<!-- skill: competitor-analysis -->
