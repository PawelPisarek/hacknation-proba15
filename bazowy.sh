#!/bin/sh
# Wynik bazowy: generuje zbiory (jeśli brak), liczy H1 (roznica) i H2 (nauka) na karcie, ocenia.
# Uruchamiać na OMENie przez orkiestrator (--klasa gpu-tlo). DANE=katalog na dane (domyślnie ~/dane/rtg).
set -e
DANE=${DANE:-$HOME/dane/rtg}
python -c "import torch,sys; print('torch', torch.__version__, 'cuda', torch.cuda.is_available()); sys.exit(0 if torch.cuda.is_available() else 3)" \
  || pip install -q torch --index-url https://download.pytorch.org/whl/cu121
pip install -q -r requirements.txt
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader || true
[ -f "$DANE/maly/etykiety.json" ] || python -m rtg.generator --wyjscie "$DANE/maly" --grupy 12 --skala 0.25
[ -f "$DANE/duzy/etykiety.json" ] || python -m rtg.generator --wyjscie "$DANE/duzy" --grupy 1 --nauka 4 --czyste 1 --z-dodatkami 2 --skala 1 --bity 24
[ -f "$DANE/pusta/etykiety.json" ] || python -m rtg.generator --wyjscie "$DANE/pusta" --grupy 12 --skala 0.25 --wariant pusta --ziarno 19
mkdir -p wyniki
python -m rtg.wykryj --dane "$DANE/maly" --metoda roznica nauka --wyjscie wyniki/maly
python -m rtg.wykryj --dane "$DANE/pusta" --metoda roznica nauka --wyjscie wyniki/pusta
python -m rtg.wykryj --dane "$DANE/duzy" --metoda roznica nauka --wyjscie wyniki/duzy
echo "=== WYNIK maly (12 grup, 1825x575) ==="
python -m rtg.ocena --dane "$DANE/maly" --wyniki wyniki/maly/roznica.json wyniki/maly/nauka.json
echo "=== WYNIK pusta (P19: wzorzec pusta naczepa, badane 2/3 z towarem zgloszonym) ==="
python -m rtg.ocena --dane "$DANE/pusta" --wyniki wyniki/pusta/roznica.json wyniki/pusta/nauka.json
echo "=== WYNIK duzy (7300x2300, ~50 MB) ==="
python -m rtg.ocena --dane "$DANE/duzy" --wyniki wyniki/duzy/roznica.json wyniki/duzy/nauka.json
python -m rtg.raport --dane "$DANE/maly" --wyniki wyniki/maly/roznica.json --wyjscie wyniki/raport --ile 4
python -m rtg.raport --dane "$DANE/maly" --wyniki wyniki/maly/nauka.json --wyjscie wyniki/raport --ile 4
python -m rtg.raport --dane "$DANE/pusta" --wyniki wyniki/pusta/nauka.json --wyjscie wyniki/raport_pusta --ile 4
