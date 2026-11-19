# Drugie Spojrzenie (repo hacknation-proba15)

Narzędzie dla operatorów RTG na granicy: porównuje obraz naczepy ze wzorcem czystego pojazdu i zaznacza na obrazie miejsca, które mogą kryć przemyt. Decyzję o kontroli fizycznej nadal podejmuje człowiek.

**Dla kogo:** operatorzy RTG Służby Celno-Skarbowej (zadanie KAS „Automatyczna wyszukiwarka anomalii”). Treść zadania: [docs/zadanie.md](docs/zadanie.md).

**Linki:** makieta — [pawelpisarek.github.io/hacknation-proba15/makieta/](https://pawelpisarek.github.io/hacknation-proba15/makieta/) · wersja na ksefbot.pl — _(do uzupełnienia)_ · opis dla HackTribe: [docs/hacktribe.md](docs/hacktribe.md)

## Jak uruchomić

Wymagania: Python ≥ 3.10, `pip install -r requirements.txt`, PyTorch z CUDA (wykrywanie działa tylko na karcie graficznej).

```sh
# dane syntetyczne: biblioteka pustych wzorców + badane naczepy (pełny rozmiar: --skala 1 --bity 24, ~50 MB/obraz)
python -m rtg.generator --wyjscie dane/bib --wariant biblioteka --grupy 12 --skala 0.25
# wykrywanie: H1 różnica / H2 nauka; towar „nie wiem” albo zgłoszony
python -m rtg.wykryj --dane dane/bib --metoda roznica nauka --towar nie_wiem zgloszony --wyjscie wyniki/bib
# ocena wg zadania: FP (czyste), FN, FN@5, +N, dobór wzorca, czas, pamięć karty; --wymagaj = kod 1 przy niezaliczeniu
python -m rtg.ocena --dane dane/bib --wyniki wyniki/bib/nauka_zgloszony.json --bazowe wyniki/bib/nauka_nie_wiem.json --krzywa 1,1.5,2 --wymagaj
# podgląd ramek (PNG)
python -m rtg.raport --dane dane/bib --wyniki wyniki/bib/nauka_zgloszony.json --wyjscie wyniki/raport
```

Makieta: statyczna strona `makieta/index.html` (bez budowania, udawane dane), otwierana wprost w przeglądarce.

## Jak oceniamy

Skuteczność mierzymy na dwóch zbiorach, tak jak w zadaniu:
- **zbiór „czysty”** (naczepy bez dodatków) — aplikacja nie powinna zaznaczać nic; każdy alarm to **false positive (FP)**;
- **zbiór z „dodatkami”** (elementy niebędące konstrukcją pojazdu) — aplikacja powinna zaznaczyć ich miejsce; brak zaznaczenia to **false negative (FN)**.

Wyniki podamy po zmierzeniu — w tej wersji README nie ma żadnych liczb.

## Dane: sztuczny zbiór — dlaczego

Obrazów KAS nie mamy (dane są wydawane dopiero na stoisku). Dlatego budujemy własny sztuczny zbiór plików .bmp: naczepy „czyste” i z doklejonymi „dodatkami”. Pozwala to policzyć FP i FN na znanej prawdzie, ale nie zastępuje prawdziwych obrazów RTG.

## Użyte narzędzia

Narzędzia przygotowane przed hackathonem i użyte w projekcie. Znaczniki `<!-- skill: … -->` na końcu plików w `docs/` wskazują, którego skilla użyto.

| Narzędzie | Do czego | Gdzie w repo |
|---|---|---|
| **OpenMausBot** ([github.com/milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot), Apache-2.0) | Zespół 5 botów. Szef — rozdziela pracę i rozmawia z Pawłem; Projektant — pyta Artura i pisze spec; Analityk — materiały, ryzyka, recenzje; Programista — kod, makieta, wdrożenia; Prezenter — README i teksty. | całe repo (`docs/decyzje.md`, `docs/stan.md`) |
| **Claude** (Anthropic) | Modele, na których działają boty. | całe repo |
| **pm-skills** ([github.com/phuryn/pm-skills](https://github.com/phuryn/pm-skills), MIT): `competitor-analysis`, `brainstorm-ideas-new`, `identify-assumptions-new`, `prioritize-assumptions`, `strategy-red-team`, `create-prd`, `test-scenarios` | Analiza konkurencji, pomysły i założenia, atak na założenia, PRD, scenariusze testów. | `docs/pm/01`–`06`, `docs/spec.md` |
| **pm-skills** (Prezenter): `product-name`, `value-prop-statements` | Nazwa produktu, hasło i opis do formularza HackTribe. | `docs/hacktribe.md` |
| Skill zespołu `przeplywy-pm` | Kolejność kroków pracy produktowej i recenzji przejść. | `docs/pm/`, `docs/spec.md` |
| **NumPy** (`>=1.24`) | Obliczenia na obrazach, porównanie ze wzorcem. | `rtg/`, `requirements.txt` |
| **Pillow** (`>=10`) | Odczyt i zapis plików .bmp, rysowanie zaznaczeń. | `rtg/`, `requirements.txt` |
| **PyTorch** (CUDA) | Metoda „nauka” na karcie graficznej; instalowany osobno (patrz `bazowy.sh`). | `rtg/wykryj.py`, `bazowy.sh` |
| NumPy, Pillow, PyTorch (CUDA) | obliczenia na obrazach, odczyt .bmp, wykrywanie na karcie graficznej | `rtg/` |
| Makieta | czysty HTML/CSS/JS bez bibliotek, udawane dane | `makieta/index.html` |
