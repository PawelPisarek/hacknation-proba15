"""Sonda H7 (KA7): szczyt pamięci karty dla szkieletów PatchCore (wide_resnet50_2, warstwy 2–3)
i EfficientAD (PDN-S nauczyciel+uczeń + autoenkoder) na obrazie w rozdzielczości roboczej.
Wagi losowe (pamięć nie zależy od wag; bez pobierania). Tylko karta.

  python -m rtg.sonda_pamiec --szer 1800 --wys 576
"""
import argparse
import time

import torch
import torch.nn as nn


def pdn_s(out=384):
    return nn.Sequential(nn.Conv2d(3, 128, 4, padding=3), nn.ReLU(), nn.AvgPool2d(2, 2, padding=1),
                         nn.Conv2d(128, 256, 4, padding=3), nn.ReLU(), nn.AvgPool2d(2, 2, padding=1),
                         nn.Conv2d(256, 256, 3, padding=1), nn.ReLU(), nn.Conv2d(256, out, 4))


def ae():
    enc = nn.Sequential(*[m for c in [(3, 32), (32, 32), (32, 64), (64, 64), (64, 64)]
                          for m in (nn.Conv2d(c[0], c[1], 4, 2, 1), nn.ReLU())], nn.Conv2d(64, 64, 8))
    return enc


def pomiar(nazwa, f, x, n=3):
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    try:
        with torch.no_grad():
            f(x)
            torch.cuda.synchronize()
            t0 = time.time()
            for _ in range(n):
                f(x)
            torch.cuda.synchronize()
        print(f"{nazwa}: szczyt karty {round(torch.cuda.max_memory_allocated() / 1e6)} MB, "
              f"{round((time.time() - t0) / n, 3)} s/obraz, wejście {tuple(x.shape)}")
    except torch.OutOfMemoryError:
        print(f"{nazwa}: BRAK PAMIĘCI KARTY przy wejściu {tuple(x.shape)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--szer", type=int, default=1800)
    ap.add_argument("--wys", type=int, default=576)
    a = ap.parse_args()
    dev = torch.device("cuda")
    print("karta:", torch.cuda.get_device_name(0), round(torch.cuda.get_device_properties(0).total_memory / 1e6), "MB")
    for dt in (torch.float32, torch.float16):
        x = torch.randn(1, 3, a.wys, a.szer, device=dev, dtype=dt)
        try:
            import torchvision
            m = torchvision.models.wide_resnet50_2(weights=None).to(dev, dt).eval()

            def patchcore(x):
                y = m.maxpool(m.relu(m.bn1(m.conv1(x))))
                l2 = m.layer2(m.layer1(y))
                l3 = m.layer3(l2)
                return torch.cat([l2, nn.functional.interpolate(l3, size=l2.shape[-2:])], 1)
            pomiar(f"PatchCore wide_resnet50_2 L2+L3 {dt}", patchcore, x)
            del m
        except ImportError:
            print("PatchCore: brak torchvision — nie mierzone")
        t, s, e = pdn_s().to(dev, dt).eval(), pdn_s(768).to(dev, dt).eval(), ae().to(dev, dt).eval()
        pomiar(f"EfficientAD PDN-S (nauczyciel+uczeń+AE) {dt}", lambda x: (t(x), s(x), e(x)), x)
        del t, s, e


if __name__ == "__main__":
    main()
