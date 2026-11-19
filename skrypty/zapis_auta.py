"""Zapis wyniku jednego auta pokazu (JSON + podglądy) i test podłogi auta A po każdym towarze."""
import json
import os
import sys
import time
import urllib.request

from PIL import Image

a, z = sys.argv[1], sys.argv[2]
P = os.environ.get("P", "8772")
d = json.load(open(f"{z}/{a}.json"))
d["zapisano"] = "karta OMENa, " + time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
json.dump(d, open(f"{z}/{a}.json", "w"), ensure_ascii=False)
urllib.request.urlretrieve(f"http://localhost:{P}" + d["podglad"], f"{z}/{a}.png")
urllib.request.urlretrieve(f"http://localhost:{P}" + d["wzorzec_png"], f"{z}/wz_{d['typ']}.png")
au = json.load(open(os.path.expanduser("~/dane/rtg/bib/auta_pokazu.json")))[a]
im = Image.open(os.path.expanduser("~/dane/rtg/bib/obrazy/") + au["plik"]).convert("L")
im.thumbnail((700, 300))
im.save(f"{z}/{a}_e1.png")
print(a, "zapisano", len(d["miejsca"]), "miejsc", d["wzorzec"], d["czas_s"], "s")
if a == "A":
    def pole(q, p):
        ix = max(0, min(q["x"] + q["w"], p[0] + p[2]) - max(q["x"], p[0]))
        iy = max(0, min(q["y"] + q["h"], p[1] + p[3]) - max(q["y"], p[1]))
        return ix * iy / max(1, min(q["w"] * q["h"], p[2] * p[3]))
    print("prawda A:", au["prawda"])
    pod = [x["ramka"] for x in au["prawda"] if x["rodzaj"] == "podwojna_podloga"]
    for t in ["drobnica", "plyny", "sypkie", "maszyny", "meble", "pusta", "nie_wiem"]:
        v = [q for q in d["miejsca"] if t not in q["gasi"]]
        traf = [q["id"] for q in v if q["podloga"] and any(pole(q, p) >= 0.3 for p in pod)]
        print(f"TEST PODŁOGI towar={t}: widoczne {len(v)}, wygaszone {len(d['miejsca']) - len(v)}, "
              f"trafiona podłoga z dopiskiem {traf} ->", "OK" if traf else "BŁĄD")
