# 01 — Analiza konkurencji i podejść (/competitive-analysis)

**Data**: 2026-11-19 (sobota, start próby 15); poprawione po recenzjach R1–R2 (Analityk), R3 bez braków
**Produkt**: wyszukiwarka anomalii na obrazach RTG naczep/ciężarówek (KAS) — porównanie badanego obrazu .bmp ze wzorcem, zaznaczenie różnic. Działa lokalnie (bez chmury), wynik z usługi na karcie OMENa (GTX 1050 4 GB).
**Perspektywa porównania** (decyzja Szefa 11:22): funkcje i sposób porównania obrazów, nie cena ani rynek — to narzędzie dla KAS, nie produkt na rynek; konkurentów szukamy sami poza wymienionymi w zadaniu.
**Źródła**: `docs/zadanie.md`, `docs/decyzje.md`, `docs/materialy.md` §6, wyszukiwanie w sieci 19.11 (linki na dole). Czego nie dało się potwierdzić — oznaczone „niezweryfikowane” lub „założenie”.

## Przegląd rynku
Operatorzy RTG oceniają obrazy ręcznie; dostawcy sprzętu dokładają moduły AI dwóch rodzajów: wykrywanie zagrożeń (ATD, znane przedmioty, np. broń, papierosy) oraz weryfikacja zawartości względem zgłoszenia/manifestu (ACV). KAS ma już detektor papierosów, który słabo radzi sobie z małymi skrytkami w konstrukcji pojazdu — tu potrzebne jest porównanie ze wzorcem i wykrywanie „czegoś, czego nie powinno być”, a nie szukanie znanego przedmiotu.

Porównanie obrazu cargo/pojazdu z obrazami wcześniejszymi lub referencyjnymi **jest znane** (prior art, `docs/materialy.md` §6): projekt UE ACXIS (baza referencyjna cargo, rejestracja obrazów i obraz różnicowy), patenty USPTO 10302807, 10768338, 11287391 (porównanie z wcześniejszymi obrazami pojazdu, różnica piksel po pikselu, skrytki poza kontenerem), UCL/Jaccard i in. (autoenkoder uczony na pustych kontenerach) i OSTI (podobieństwo głębokie obrazów pojazdów). Jawnego opisu takiego modułu u Nuctech/Multicontrol nie znalazłem — czy go mają, jest **niezweryfikowane**. Sama idea „porównaj ze wzorcem” nie jest więc nowością; wyróżnia nas wykonanie (sekcja „Okazje do wyróżnienia”).

## Konkurenci bezpośredni (ten sam użytkownik: operator RTG / służba celna)
| Konkurent | Pozycjonowanie | Mocna strona | Słaba strona |
|---|---|---|---|
| Nuctech — platforma inspekcji z AI | dostawca urządzeń KAS; głęboka sieć; wg jednego artykułu branżowego uczona też na danych symulowanych (niezweryfikowane; https://www.asadria.com/?p=25109) | jest już w urządzeniu | zamknięty; czy porównuje ze wzorcem — niezweryfikowane |
| Multicontrol — oprogramowanie urządzeń | drugi dostawca KAS | jak wyżej | jak wyżej; dane nieznane |
| Rapiscan (Insight) | kształt, tekstura, intensywność + głębokie wykrywanie przedmiotów; zgodność z manifestem (rapiscan-ase.com, patent US11099294: https://patentimages.storage.googleapis.com/ca/a9/48/5be1c9eb5bec46/US11099294.pdf) | dojrzały; certyfikacja — niezweryfikowane | porównuje ze zgłoszeniem, nie z pustym wzorcem pojazdu (wg znalezionych źródeł); model licencji/chmura — niezweryfikowane |
| Smiths Detection | algorytmy wykrywania materiałów wybuchowych w bagażu (artykuł branżowy: https://www.asadria.com/?p=25109) | renoma | czy dotyczy pojazdów — niezweryfikowane |
| Obecny detektor papierosów KAS | wykrywanie jednego rodzaju towaru | działa w produkcji | słaby przy małych ilościach w konstrukcji pojazdu (z zadania §1) |

## Konkurenci pośredni — podejścia do porównania obrazów (uruchamialne na GTX 1050 4 GB — do zmierzenia)
| Podejście | Jak działa | Plusy | Minusy / ryzyko |
|---|---|---|---|
| A. Różnica pikseli po dopasowaniu (rejestracja + różnica / SSIM) — **prior art: ACXIS, patenty 10302807 / 10768338 / 11287391** | wyrównuje wzorzec i badany obraz, odejmuje, progowanie, ramki | proste, szybkie, wyjaśnialne, bez uczenia | wrażliwe na przesunięcie, skalę, szum, inne ułożenie naczepy → fałszywe alarmy |
| B. PatchCore / pamięć fragmentów „czystych” (anomalib; metoda z wiedzy autora, arXiv 2106.08265 — niezweryfikowane w tej sesji) | uczy się na czystych obrazach, szuka fragmentów nietypowych | uczenie ok. 8 min w benchmarku przemysłowym (arXiv 2403.15463, inne dane niż nasze); mapa ciepła | pamięć rośnie z liczbą obrazów; przykład w dokumentacji anomalib redukuje do 10% fragmentów (nie pomiar); mieści się w 4 GB — niezweryfikowane; obrazy 50 MB trzeba ciąć na kafle |
| C. EfficientAD (mała sieć „uczeń–nauczyciel”) | wykrywanie anomalii w milisekundach | 2,2–4,5 ms/obraz w publikacji **na RTX A6000, nie na GTX 1050** (arXiv 2303.14535) | dłuższe uczenie (ok. 5,5 h w benchmarku arXiv 2403.15463); czas na GTX 1050 — niezweryfikowane, do zmierzenia |
| D. Autoenkoder / rekonstrukcja (prior art: Jaccard i in., UCL, arXiv 1609.02805 — na pustych kontenerach) | uczy się odtwarzać „czysty” obraz, różnica = anomalia | prosty, mały | rozmyta rekonstrukcja → fałszywe alarmy na krawędziach |
| E. Para obrazów w jednej sieci (zmiany wzorzec ↔ badany; OSTI: podobieństwo głębokie obrazów pojazdów) | sieć dostaje oba obrazy, zwraca maskę zmian | najlepiej pasuje do „wzorzec vs badany” | potrzebuje obrazów z oznaczonymi dodatkami, a zadanie §5 każe uczyć na prawidłowych — **działa tylko na naszym zbiorze sztucznym (z maskami) i nie przenosi się na dane KAS**; poza zakresem albo eksperyment |
| F. Nadzorowane wykrywanie obiektów (YOLO itp.) | szuka znanych „dodatków” | szybkie na znanych typach | nie wykryje nieznanych skrytek; jak obecny detektor KAS |

## Macierz funkcji
| Zdolność | Nasz produkt (cel) | Dostawcy sprzętu | Różnica pikseli (A) | PatchCore (B) | EfficientAD (C) |
|---|---|---|---|---|---|
| Porównanie ze wzorcem | tak | ? (niezweryfikowane) | tak | pośrednio (uczy się „normy”) | pośrednio |
| Zaznaczenie miejsca na obrazie | tak | ? (niezweryfikowane) | tak | tak (mapa ciepła) | tak |
| Bez chmury | tak | ? (niezweryfikowane) | tak | tak | tak |
| Duże pliki ~50 MB, partie | tak (kafle) | ? (niezweryfikowane) | tak | tak (kafle) | tak (kafle) |
| Zero zaznaczeń na czystych (zadanie §6: każde zaznaczenie = alarm FP) | cel — ustalone z zadania §6 (zero na czystych); limit 5 na auto to P8 | nieznane | słabo | dobrze wg publikacji, niezweryfikowane na RTG | jak B |
| Wykryje nieznany dodatek | tak | tylko znane | tak | tak | tak |
| Dobór wzorca z biblioteki (P6, P11; P19: A) | tak, z ostrzeżeniem „wzorzec niepewny” | ? | nie (wzorzec dany z góry; ACXIS ma bazę referencyjną) | pośrednio (norma z wielu czystych) | pośrednio |
| Ocena pewności zaznaczeń, najpewniejsze pierwsze, limit 5 na auto (P8) | tak | ? | nie (A = surowa różnica, bez rankingu) | tak (wynik nietypowości) | tak (wynik nietypowości) |
| Decyzja operatora „do kontroli”/odrzuć z powodem, zapisana w raporcie (P7, P9, P10) | tak | ? | nie | nie | nie |
| Wynik przypisany do miejsca i przedmiotu kontroli (§9 zadania; pole identyfikujące kontrolę w raporcie z auta) | tak (pole w raporcie, P10) | ? | nie (do dopisania) | nie (do dopisania) | nie (do dopisania) |
| Skalowalność na większe zbiory (kafle, partie, równoległość) | cel (§3, §7) | ? | dobra (prosta) | średnia (pamięć rośnie z liczbą obrazów) | dobra (mały model; niezweryfikowane na GTX 1050) |

## Fałszywe alarmy a małe skrytki (P5, P8)
Zadanie §6 liczy każde zaznaczenie na czystym obrazie jako alarm fałszywy, a małe skrytki (≈0,1% pikseli wg Jaccard i in.) wymagają czułości. Rozstrzyga to Artur (P5, 11:21): przeoczony dodatek jest gorszy, zbędny alarm = minuta więcej przy aucie, zaznaczeń na auto „kilka” — górna granica 5 (P8). Ten plik nie ustala progu: cel zero zaznaczeń na czystych w teście, 5 to limit na auto; kompromis czułość ↔ FP raportujemy krzywą, próg ustalają ludzie.

## Wzorzec (P19, odpowiedź Artura 11:26)
A — wzorzec to obraz pustej naczepy tego samego typu. Operator przed analizą wybiera z listy rodzaj zgłoszonego towaru (plus „pusta naczepa”), by zgodny ładunek nie dostawał ramek; bez wyboru zaznaczamy wszystko (P5). „Wzorzec niepewny” operator widzi, gdy w bibliotece nie ma naczepy tego typu i system bierze najbliższą podobną (P11).

## Okazje do wyróżnienia (po uwzględnieniu prior art)
1. **Automatyczny dobór wzorca z biblioteki** (P6, P11) — operator zwykle nie ma czystego zdjęcia tej samej naczepy; baza referencyjna z ACXIS to bliski odpowiednik, nasza działa lokalnie dla KAS i ostrzega „wzorzec niepewny”.
2. **Ocena pewności i do 5 zaznaczeń na auto** (P8) — operator widzi najpewniejsze pierwsze.
3. **Decyzja operatora z powodem zapisana w raporcie z auta** (P7, P10).
4. **Wszystko lokalnie** i partie/kafle dla plików ~50 MB, < 1 min na obraz (zadanie §7).

## Zagrożenia
1. **Dostawcy dodadzą porównanie ze wzorcem we własnym oprogramowaniu** (założenie, bez źródła) — nasza wartość: dobór wzorca i niezależność od dostawcy (Nuctech i Multicontrol).
2. **Różne ułożenie i długość naczep** — dopasowanie wzorca może zawieść; ryzyko fałszywych alarmów.
3. **Dane sztuczne ≠ rzeczywiste RTG** — wynik na własnym zbiorze nie dowodzi skuteczności na danych KAS (mówimy to na pokazie).

## Rekomendacje
- **Postawić na**: porównanie ze wzorcem (A) jako baza + ocena nietypowości (B lub C) jako filtr fałszywych alarmów + dobór wzorca.
- **Dorównać w**: czytelnym raporcie z zaznaczonymi miejscami.
- **Pominąć**: pełne wykrywanie znanych przedmiotów (F), podejście E na danych KAS. **Integracja z urządzeniami dostawców i repozytorium RTG** (§9) nie jest w zakresie MVP, ale raport ma pole identyfikujące kontrolę (miejsce, przedmiot), żeby integracja była możliwa.
- Na karcie 4 GB: kafle i małe modele; mieszczenie się B/C — do zmierzenia przez Programistę.

## Czego nie wiem o produkcie (pytania do Artura — moment (a))
Rozstrzyga zadanie (nie pytamy): praca bez internetu, dane sztuczne, działanie bez człowieka, format .bmp, język ekranu, perspektywa porównania (decyzja Szefa).
1. Użytkownik — P2: operator przy stanowisku, kilka minut na auto.
2. Problem — P3: podwójna podłoga, ściana przy kabinie.
3. Zysk — P4: mniej przeoczonych skrytek.
4. Cena błędu — P5: przeoczony dodatek gorszy; zaznaczeń kilka.
5. Wzorzec — P6, P11: system dobiera sam z biblioteki.
6. Po alarmie — P7: zatwierdza/odrzuca z powodem.

## Źródła
- Rapiscan — technologia: https://rapiscan-ase.com/resource-center/technology
- Przegląd analizy obrazów RTG cargo (ATD/ACV): https://openaccess.library.uitm.edu.my/Record/ndltd-bl.uk-oai-ethos.bl.uk-747225/Description
- ACXIS (prior art): https://openaccessgovernment.org/automated-comparison-x-ray-images-cargo-scanning-acxis/25162
- Jaccard i in., autoenkoder na pustych kontenerach: https://arxiv.org/pdf/1609.02805
- OSTI, podobieństwo głębokie obrazów pojazdów: https://www.osti.gov/servlets/purl/1877523
- Patenty: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10302807 (też 10768338, 11287391)
- EfficientAD (RTX A6000): https://arxiv.org/pdf/2303.14535
- Benchmark uczenia PatchCore / EfficientAD: https://arxiv.org/pdf/2403.15463
- PatchCore a pamięć karty: https://github.com/openvinotoolkit/anomalib/discussions/1935
- Nuctech (dane symulowane) i Smiths (bagaż): https://www.asadria.com/?p=25109
- Niezweryfikowane: porównanie ze wzorcem u Nuctech/Multicontrol/Smiths; certyfikacja i licencje Rapiscan; PatchCore/EfficientAD na GTX 1050 4 GB.

<!-- skill: przeplywy-pm -->
<!-- skill: competitor-analysis -->
