# Drugie Spojrzenie (repo hacknation-proba15)

Narzędzie dla operatorów RTG na granicy: porównuje obraz naczepy ze wzorcem czystego pojazdu i zaznacza na obrazie miejsca, które mogą kryć przemyt. Decyzję o kontroli fizycznej nadal podejmuje człowiek.

**Dla kogo:** operatorzy RTG Służby Celno-Skarbowej (zadanie KAS „Automatyczna wyszukiwarka anomalii”). Treść zadania: [docs/zadanie.md](docs/zadanie.md).

**Linki:** makieta — _(do uzupełnienia)_ · wersja na ksefbot.pl — _(do uzupełnienia)_ · opis dla HackTribe: [docs/hacktribe.md](docs/hacktribe.md)

## Jak uruchomić

_Komendy dopisze Programista (wymagania, instalacja, start, przykład na pliku .bmp)._

## Jak oceniamy

Skuteczność mierzymy na dwóch zbiorach, tak jak w zadaniu:
- **zbiór „czysty”** (naczepy bez dodatków) — aplikacja nie powinna zaznaczać nic; każdy alarm to **false positive (FP)**;
- **zbiór z „dodatkami”** (elementy niebędące konstrukcją pojazdu) — aplikacja powinna zaznaczyć ich miejsce; brak zaznaczenia to **false negative (FN)**.

Wyniki podamy po zmierzeniu — w tej wersji README nie ma żadnych liczb.

## Dane: sztuczny zbiór — dlaczego

Obrazów KAS nie mamy (dane są wydawane dopiero na stoisku). Dlatego budujemy własny sztuczny zbiór plików .bmp: naczepy „czyste” i z doklejonymi „dodatkami”. Pozwala to policzyć FP i FN na znanej prawdzie, ale nie zastępuje prawdziwych obrazów RTG.

## Użyte narzędzia

- **OpenMausBot** ([github.com/milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot), Apache-2.0) — zespół 5 botów: Szef, Projektant, Analityk, Programista, Prezenter; przygotowany przed hackathonem.
- **Claude** (Anthropic) — modele, na których działają boty.
- **pm-skills** ([github.com/phuryn/pm-skills](https://github.com/phuryn/pm-skills), MIT) — skille do pracy produktowej i tekstów.
- **Biblioteki w kodzie** — _lista do uzupełnienia z kodu Programisty_.
