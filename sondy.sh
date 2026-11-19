#!/bin/sh
# Sondy 1–3 z docs/pm/05-zalozenia-atak.md — jeden przebieg na karcie OMENa (--klasa gpu-tlo).
# Hipotezy: S1 H1a dobór=typ ≥90%, H1b „niepewny” dla typu spoza, H3a FP=0 na czystych pustych;
# S2 H3b FP=0 na załadowanych z wyborem, H5a wybór obniża FP, H5b wybór nie gasi dodatków, H2 FN@5−FN ≤5 pp;
# S3 H8 trudny FN +≤10 pp i FP=0, H6 50 MB < 60 s, H7 PatchCore/EfficientAD ≤ 4 GB.
set -e
DANE=${DANE:-$HOME/dane/rtg}
pip install -q -r requirements.txt
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader || true
G="--wariant biblioteka --grupy 36 --czyste 1 --z-dodatkami 2 --skala 0.25 --ziarno 21"
[ -f "$DANE/bib/etykiety.json" ] || python -m rtg.generator --wyjscie "$DANE/bib" $G
[ -f "$DANE/bib_trudny/etykiety.json" ] || python -m rtg.generator --wyjscie "$DANE/bib_trudny" $G --trudny
[ -f "$DANE/bib_duzy/etykiety.json" ] || python -m rtg.generator --wyjscie "$DANE/bib_duzy" --wariant biblioteka \
  --grupy 3 --biblioteka 3 --nauka-towaru 1 --czyste 1 --z-dodatkami 1 --skala 1 --bity 24 --ziarno 22
W=wyniki/sondy; mkdir -p $W
python -m rtg.wykryj --dane "$DANE/bib" --metoda roznica nauka --towar nie_wiem zgloszony --zapas 1.0 --wyjscie $W/bib
python -m rtg.wykryj --dane "$DANE/bib_trudny" --metoda roznica nauka --towar nie_wiem zgloszony --zapas 1.0 --wyjscie $W/bib_trudny
python -m rtg.wykryj --dane "$DANE/bib_duzy" --metoda roznica nauka --towar nie_wiem zgloszony --zapas 1.0 --wyjscie $W/bib_duzy
for M in roznica nauka; do
  echo "=== SONDA 1 ($M, bez wyboru towaru): dobór wzorca, niepewny, FP na czystych pustych — punkt pracy zapas 1.1 ==="
  python -m rtg.ocena --dane "$DANE/bib" --wyniki $W/bib/${M}_nie_wiem.json --mnoznik 1.1 --krzywa 1,1.1,1.25,1.5,2,3 --wymagaj || true
  echo "=== SONDA 2 ($M, z wyborem towaru): FP załadowane, zgaszone dodatki, FN@5 ==="
  python -m rtg.ocena --dane "$DANE/bib" --wyniki $W/bib/${M}_zgloszony.json --bazowe $W/bib/${M}_nie_wiem.json --mnoznik 1.1 --krzywa 1,1.1,1.25,1.5,2,3 --wymagaj || true
  echo "=== SONDA 3 ($M, trudny vs łatwy, z wyborem towaru i bez) ==="
  for T in zgloszony nie_wiem; do
  python -m rtg.ocena --dane "$DANE/bib_trudny" --wyniki $W/bib_trudny/${M}_$T.json --latwy $W/bib/${M}_$T.json --dane-latwy "$DANE/bib" --mnoznik 1.1 --wymagaj || true
  done
  echo "=== SONDA 3 ($M, pełne 50 MB): czas, pamięć ==="
  python -m rtg.ocena --dane "$DANE/bib_duzy" --wyniki $W/bib_duzy/${M}_zgloszony.json $W/bib_duzy/${M}_nie_wiem.json --mnoznik 1.1
done
echo "=== SONDA 3: pamięć karty PatchCore / EfficientAD (H7) ==="
python -c "import torchvision" 2>/dev/null || pip install -q torchvision --index-url https://download.pytorch.org/whl/cu126 || true
python -m rtg.sonda_pamiec --szer 1824 --wys 576 || true
python -m rtg.sonda_pamiec --szer 7300 --wys 2300 || true
python -m rtg.raport --dane "$DANE/bib" --wyniki $W/bib/nauka_zgloszony.json --wyjscie $W/raport --ile 8
