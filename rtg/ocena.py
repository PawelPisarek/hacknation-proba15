"""Skrypt oceny wg rozdz. 6 zadania.

- obraz „czysty”: każda zaznaczona ramka = false positive (FP),
- obraz z „dodatkami”: dodatek nietrafiony żadną ramką = false negative (FN);
  ramki na obrazie z dodatkami, które nie trafiają w żaden dodatek, liczymy osobno (FP_dod).
Trafienie: część wspólna ≥ 30% pola dodatku albo ≥ 30% pola ramki (ramka w środku dużego
dodatku też trafia; ramka-na-pół-obrazu nie trafia, bo dodatek to < 30% jej pola).

  python -m rtg.ocena --dane dane/maly --wyniki wyniki/roznica.json [--json]
Wypisuje jedną linię: metoda FP=… FN=…/… FP_dod=… czas/obraz=… s
"""
import argparse
import json
import os
import statistics


def wspolne(a, b):
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return max(0, w) * max(0, h)


def trafia(ramka, prawda, prog=0.3):
    i = wspolne(ramka, prawda)
    return i >= prog * prawda[2] * prawda[3] or i >= prog * ramka[2] * ramka[3]


def ocen(meta, wyniki):
    fp = fn = fp_dod = n_dod = n_czyst = czyste_z_alarmem = 0
    czasy, brak = [], []
    rodzaje_fn = {}
    for o in meta["obrazy"]:
        if o["rola"] == "nauka":
            continue
        w = wyniki["obrazy"].get(o["plik"])
        if w is None:
            brak.append(o["plik"])
            continue
        czasy.append(w["czas_s"])
        r = [x[:4] for x in w["ramki"]]
        if o["rola"] == "czysty":
            n_czyst += 1
            fp += len(r)
            czyste_z_alarmem += bool(r)
        else:
            for d in o["dodatki"]:
                n_dod += 1
                if not any(trafia(x, d["ramka"]) for x in r):
                    fn += 1
                    rodzaje_fn[d["rodzaj"]] = rodzaje_fn.get(d["rodzaj"], 0) + 1
            fp_dod += sum(not any(trafia(x, d["ramka"]) for d in o["dodatki"]) for x in r)
    return {"metoda": wyniki.get("metoda", "?"), "FP": fp, "czyste": n_czyst, "czyste_z_alarmem": czyste_z_alarmem,
            "FN": fn, "dodatki": n_dod, "FP_dod": fp_dod, "FN_rodzaje": rodzaje_fn,
            "czas_sr_s": round(statistics.mean(czasy), 3) if czasy else None,
            "czas_max_s": round(max(czasy), 3) if czasy else None, "brak_wyniku": len(brak)}


def linia(w):
    return (f"{w['metoda']}: FP={w['FP']} (czyste z alarmem {w['czyste_z_alarmem']}/{w['czyste']}) "
            f"FN={w['FN']}/{w['dodatki']} FP_dod={w['FP_dod']} czas/obraz śr={w['czas_sr_s']} s max={w['czas_max_s']} s"
            + (f" BRAK WYNIKU={w['brak_wyniku']}" if w["brak_wyniku"] else "")
            + (f" FN wg rodzaju={w['FN_rodzaje']}" if w["FN_rodzaje"] else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dane", required=True)
    ap.add_argument("--wyniki", nargs="+", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    meta = json.load(open(os.path.join(a.dane, "etykiety.json")))
    for p in a.wyniki:
        w = ocen(meta, json.load(open(p)))
        print(json.dumps(w, ensure_ascii=False) if a.json else linia(w))


if __name__ == "__main__":
    main()
