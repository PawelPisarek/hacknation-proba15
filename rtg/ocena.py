"""Skrypt oceny wg rozdz. 6 zadania (+ kryteria KA ze spec, braki z docs/pm/06 cz. C).

- obraz „czysty”: każda zaznaczona ramka = false positive (FP),
- obraz z „dodatkami”: dodatek nietrafiony żadną ramką = false negative (FN);
  ramki na obrazie z dodatkami, które nie trafiają w żaden dodatek, liczymy osobno (FP_dod).
Trafienie: część wspólna ≥ 30% pola dodatku albo ≥ 30% pola ramki.
Limit (KA2/KA9): na ekranie ≤ --limit ramek o najwyższej pewności + licznik „+N”; FN@limit i FN na pełnej liście.
Dobór wzorca (KA1): trafność = typ wzorca = typ badanego (typy z biblioteki); „niepewny” dla typu spoza biblioteki.
Wybór towaru (KA5): --bazowe <wynik „nie_wiem”> → ile dodatków trafionych bez wyboru zgasło po wyborze.
Trudny wariant (KA8): --latwy <wynik> --dane-latwy <katalog> → różnica FN w pp.
Krzywa (KA3): --krzywa 0.8,1,1.2 → FP/FN przy innym mnożniku progu (ramki filtrowane po pewności).
Werdykt: --wymagaj → kod wyjścia 1, gdy nie spełnia progów roboczych (FP=0, czas<60 s, FN@5−FN ≤ 5 pp,
dobór ≥ 90%, trudny FN +≤ 10 pp, 0 dodatków zgaszonych wyborem towaru).

  python -m rtg.ocena --dane dane/bib --wyniki wyniki/bib/nauka_zgloszony.json --bazowe wyniki/bib/nauka_nie_wiem.json
"""
import argparse
import json
import os
import statistics
import sys


def wspolne(a, b):
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return max(0, w) * max(0, h)


def trafia(ramka, prawda, prog=0.3):
    i = wspolne(ramka, prawda)
    return i >= prog * prawda[2] * prawda[3] or i >= prog * ramka[2] * ramka[3]


def pp(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def trafione(meta, wyniki, mnoznik=1.0):
    """Zbiór (plik, nr dodatku) trafionych na pełnej liście."""
    out = set()
    for o in meta["obrazy"]:
        w = wyniki["obrazy"].get(o["plik"])
        if o["rola"] != "dodatki" or w is None:
            continue
        r = [x[:4] for x in w["ramki"] if x[4] >= mnoznik - 1e-9]
        for i, d in enumerate(o["dodatki"]):
            if any(trafia(x, d["ramka"]) for x in r):
                out.add((o["plik"], i))
    return out


def ocen(meta, wyniki, limit=5, mnoznik=1.0):
    """mnoznik: ramka zostaje, gdy pewność (= punktacja / próg) ≥ mnoznik (krzywa progu)."""
    fp = fp5 = fn = fn5 = fp_dod = n_dod = n_czyst = czyste_z_alarmem = plus_n = obrazy_plus = 0
    czasy, brak, rodzaje_fn, fp_zal = [], [], {}, {}
    dob_ok = dob_n = niep_bib = niep_spoza = n_spoza = 0
    for o in meta["obrazy"]:
        if o["rola"] not in ("czysty", "dodatki"):
            continue
        w = wyniki["obrazy"].get(o["plik"])
        if w is None:
            brak.append(o["plik"])
            continue
        czasy.append(w["czas_s"])
        wszystkie = sorted([x for x in w["ramki"] if x[4] >= mnoznik - 1e-9], key=lambda x: -x[4])
        r, r5 = [x[:4] for x in wszystkie], [x[:4] for x in wszystkie[:limit]]
        if len(r) > limit:
            plus_n += len(r) - limit
            obrazy_plus += 1
        if "wzorzec_typ" in w:
            if o.get("w_bibliotece", True):
                dob_n += 1
                dob_ok += w["wzorzec_typ"] == o["typ"]
                niep_bib += bool(w["niepewny"])
            else:
                n_spoza += 1
                niep_spoza += bool(w["niepewny"])
        if o["rola"] == "czysty":
            n_czyst += 1
            fp += len(r)
            fp5 += len(r5)
            czyste_z_alarmem += bool(r)
            t = o.get("towar_zgloszony", "pusta") != "pusta"
            fp_zal[t] = fp_zal.get(t, 0) + len(r)
        else:
            for d in o["dodatki"]:
                n_dod += 1
                if not any(trafia(x, d["ramka"]) for x in r):
                    fn += 1
                    rodzaje_fn[d["rodzaj"]] = rodzaje_fn.get(d["rodzaj"], 0) + 1
                if not any(trafia(x, d["ramka"]) for x in r5):
                    fn5 += 1
            fp_dod += sum(not any(trafia(x, d["ramka"]) for d in o["dodatki"]) for x in r)
    w = {"metoda": wyniki.get("metoda", "?"), "towar": wyniki.get("towar", "nie_wiem"), "mnoznik_progu": mnoznik,
         "FP": fp, "FP@limit": fp5, "czyste": n_czyst, "czyste_z_alarmem": czyste_z_alarmem,
         "FP_pusta": fp_zal.get(False, 0), "FP_zaladowana": fp_zal.get(True, 0),
         "FN": fn, "FN@limit": fn5, "dodatki": n_dod, "FN_pp": pp(fn, n_dod), "FN@limit_pp": pp(fn5, n_dod),
         "limit": limit, "plus_N_suma": plus_n, "obrazy_z_plus_N": obrazy_plus,
         "FP_dod": fp_dod, "FN_rodzaje": rodzaje_fn,
         "czas_sr_s": round(statistics.mean(czasy), 3) if czasy else None,
         "czas_max_s": round(max(czasy), 3) if czasy else None,
         "pamiec_karty_max_MB": wyniki.get("pamiec_karty_max_MB"), "brak_wyniku": len(brak)}
    if dob_n or n_spoza:
        w.update({"dobor_trafny_pct": pp(dob_ok, dob_n), "dobor_n": dob_n,
                  "niepewny_w_bibliotece_pct": pp(niep_bib, dob_n),
                  "niepewny_spoza_pct": pp(niep_spoza, n_spoza), "spoza_n": n_spoza})
    return w


def linia(w):
    s = (f"{w['metoda']}/{w['towar']}: FP={w['FP']} [pusta {w['FP_pusta']} / załadowana {w['FP_zaladowana']}] "
         f"(czyste z alarmem {w['czyste_z_alarmem']}/{w['czyste']}) FN={w['FN']}/{w['dodatki']} ({w['FN_pp']}%) "
         f"FN@{w['limit']}={w['FN@limit']} ({w['FN@limit_pp']}%) +N={w['plus_N_suma']} na {w['obrazy_z_plus_N']} obr. "
         f"FP_dod={w['FP_dod']} czas/obraz śr={w['czas_sr_s']} s max={w['czas_max_s']} s karta={w['pamiec_karty_max_MB']} MB")
    if "dobor_trafny_pct" in w:
        s += (f" dobór={w['dobor_trafny_pct']}% (n={w['dobor_n']}) niepewny: spoza={w['niepewny_spoza_pct']}% "
              f"(n={w['spoza_n']}) w bibl.={w['niepewny_w_bibliotece_pct']}%")
    if "zgaszone" in w:
        s += f" zgaszone wyborem={w['zgaszone']}/{w['trafione_bez_wyboru']} {w['zgaszone_rodzaje']}"
    if "FN_latwy_pp" in w:
        s += f" trudny−łatwy FN={w['FN_roznica_pp']} pp (łatwy {w['FN_latwy_pp']}%)"
    if w["brak_wyniku"]:
        s += f" BRAK WYNIKU={w['brak_wyniku']}"
    if w["FN_rodzaje"]:
        s += f" FN wg rodzaju={w['FN_rodzaje']}"
    return s


def werdykt(w):
    nie = []
    if w["FP_pusta"] > 0:
        nie.append(f"FP na czystych pustych={w['FP_pusta']} (>0)")
    if w["towar"] == "zgloszony" and w["FP_zaladowana"] > 0:
        nie.append(f"FP na załadowanych z wyborem={w['FP_zaladowana']} (>0)")
    if w["czas_max_s"] is not None and w["czas_max_s"] >= 60:
        nie.append(f"czas max={w['czas_max_s']} s (≥60)")
    if w["FN@limit_pp"] - w["FN_pp"] > 5:
        nie.append(f"FN@5−FN={round(w['FN@limit_pp'] - w['FN_pp'], 1)} pp (>5)")
    if "dobor_trafny_pct" in w and w["dobor_n"] and w["dobor_trafny_pct"] < 90:
        nie.append(f"dobór={w['dobor_trafny_pct']}% (<90)")
    if "FN_roznica_pp" in w and w["FN_roznica_pp"] > 10:
        nie.append(f"trudny FN +{w['FN_roznica_pp']} pp (>10)")
    if w.get("zgaszone", 0) > 0:
        nie.append(f"wybór towaru zgasił {w['zgaszone']} dodatków (Z5)")
    return nie


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dane", required=True)
    ap.add_argument("--wyniki", nargs="+", required=True)
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--mnoznik", type=float, default=1.0, help="punkt pracy: mnożnik progu z przebiegu (krzywa: patrz --krzywa)")
    ap.add_argument("--bazowe", help="wynik bez wyboru towaru (nie_wiem) do policzenia zgaszonych dodatków")
    ap.add_argument("--latwy", help="wynik na łatwym wariancie (ta sama metoda i tryb) do porównania FN")
    ap.add_argument("--dane-latwy")
    ap.add_argument("--krzywa", help="mnożniki progu, np. 0.8,1,1.2,1.5")
    ap.add_argument("--wymagaj", action="store_true", help="kod wyjścia 1, gdy nie spełnia progów roboczych")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    meta = json.load(open(os.path.join(a.dane, "etykiety.json")))
    zle = 0
    for p in a.wyniki:
        wyn = json.load(open(p))
        w = ocen(meta, wyn, a.limit, a.mnoznik)
        if a.bazowe:
            baz = trafione(meta, json.load(open(a.bazowe)))
            teraz = trafione(meta, wyn)
            zg = baz - teraz
            rodz = {}
            for (plik, i) in zg:
                o = next(x for x in meta["obrazy"] if x["plik"] == plik)
                k = f"{o['dodatki'][i]['rodzaj']}@{o['towar_zgloszony']}"
                rodz[k] = rodz.get(k, 0) + 1
            w.update({"zgaszone": len(zg), "trafione_bez_wyboru": len(baz), "zgaszone_rodzaje": rodz})
        if a.latwy:
            ml = json.load(open(os.path.join(a.dane_latwy, "etykiety.json")))
            wl = ocen(ml, json.load(open(a.latwy)), a.limit, a.mnoznik)
            w.update({"FN_latwy_pp": wl["FN_pp"], "FN_roznica_pp": round(w["FN_pp"] - wl["FN_pp"], 1),
                      "FP_latwy": wl["FP"]})
        print(json.dumps(w, ensure_ascii=False) if a.json else linia(w))
        if a.krzywa:
            z0 = wyn.get("parametry", {}).get("zapas", 1.0)
            print(f"  krzywa zapas progu (bazowy {z0}) → FP (pusta/załad.) / FN / FN@5:")
            for m in [float(x) for x in a.krzywa.split(",")]:
                k = ocen(meta, wyn, a.limit, m)
                print(f"  {round(m * z0, 3):>5}: FP={k['FP']} ({k['FP_pusta']}/{k['FP_zaladowana']}) FN={k['FN']}/{k['dodatki']} "
                      f"({k['FN_pp']}%) FN@{a.limit}={k['FN@limit']} ({k['FN@limit_pp']}%)")
        if a.wymagaj:
            nie = werdykt(w)
            print("  WERDYKT:", "zaliczone" if not nie else "niezaliczone — " + "; ".join(nie))
            zle += bool(nie)
    sys.exit(1 if (a.wymagaj and zle) else 0)


if __name__ == "__main__":
    main()
