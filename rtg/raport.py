"""Raport graficzny: obraz z ramkami wykrytymi (czerwone) i prawdą (zielone), zmniejszony do PNG.

  python -m rtg.raport --dane dane/maly --wyniki wyniki/nauka.json --wyjscie wyniki/raport --ile 6
"""
import argparse
import json
import os

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dane", required=True)
    ap.add_argument("--wyniki", required=True)
    ap.add_argument("--wyjscie", required=True)
    ap.add_argument("--ile", type=int, default=6)
    ap.add_argument("--szer", type=int, default=1400)
    a = ap.parse_args()
    meta = json.load(open(os.path.join(a.dane, "etykiety.json")))
    wyn = json.load(open(a.wyniki))
    os.makedirs(a.wyjscie, exist_ok=True)
    n = 0
    for o in meta["obrazy"]:
        if o["rola"] == "nauka" or o["plik"] not in wyn["obrazy"] or n >= a.ile:
            continue
        im = Image.open(os.path.join(a.dane, "obrazy", o["plik"])).convert("RGB")
        s = a.szer / im.width
        im = im.resize((a.szer, int(im.height * s)))
        d = ImageDraw.Draw(im)
        for x in o["dodatki"]:
            X, Y, W, H = [v * s for v in x["ramka"]]
            d.rectangle([X - 2, Y - 2, X + W + 2, Y + H + 2], outline=(0, 200, 0), width=2)
        for x in wyn["obrazy"][o["plik"]]["ramki"]:
            X, Y, W, H = [v * s for v in x[:4]]
            d.rectangle([X, Y, X + W, Y + H], outline=(230, 0, 0), width=2)
        im.save(os.path.join(a.wyjscie, o["plik"].replace(".bmp", f"_{wyn['metoda']}.png")))
        n += 1
    print("raport:", n, "obrazów ->", a.wyjscie)


if __name__ == "__main__":
    main()
