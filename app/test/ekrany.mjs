// Test przeglądarkowy ekranów MVP: A1–A11 (docs/pm/06), KA17, KA18, P42, P44, tryb awaryjny.
//   BASE=https://hacknation.ksefbot.pl/ WLASNY=/tmp/skrzyniowa.bmp DUZY=/tmp/duzy50.bmp ZRZUTY=docs/zrzuty \
//   node app/test/ekrany.mjs        (playwright-core + chromium; NODE_PATH do playwright-core)
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright-core");
import fs from "node:fs";
import os from "node:os";

const BASE = process.env.BASE || "http://localhost:3000/";
const ZR = process.env.ZRZUTY || "";
const exe = process.env.CHROMIUM || `${os.homedir()}/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome`;
const wyniki = [];
const ok = (nazwa, warunek, opis = "") => { wyniki.push([nazwa, !!warunek, opis]); console.log(warunek ? "OK  " : "BŁĄD", nazwa, opis); };
const przegl = await chromium.launch({ executablePath: exe, args: ["--no-sandbox"] });
const kontekst = await przegl.newContext({ viewport: { width: 1500, height: 950 } });
const s = await kontekst.newPage();
const zadania = [];
s.on("request", (r) => zadania.push(r.url()));
const zrzut = async (n) => { if (ZR) await s.screenshot({ path: `${ZR}/mvp-${n}.png`, fullPage: true }); };
const poz = () => s.$$eval(".poz", (e) => e.map((x) => ({ t: x.querySelector(".g span").textContent, kl: x.className, dop: !!x.querySelector(".dopisek"), cala: x.textContent })));
const tekst = () => s.textContent("#app");
const auto = async (k) => { await s.goto(BASE); await s.click(`text=Auto ${k}`); await s.locator(".karta", { hasText: `Auto ${k}` }).locator("button").click(); await s.waitForSelector(".towar"); };

// --- A1 + KA4: E1 → E2 → decyzje → E4, czas
await s.goto(BASE);
ok("A1 E1: auto A, auto B, wczytaj własne zdjęcie", (await tekst()).includes("Auto A") && (await tekst()).includes("Auto B") && (await s.$("text=Wczytaj własne zdjęcie")));
await zrzut("E1");
const t0 = Date.now();
await auto("A");
const towary = await s.$$eval(".towar button", (b) => b.map((x) => x.textContent));
ok("A1 linia towaru: 6 grup + nie wiem", JSON.stringify(towary) === JSON.stringify(["drobnica na paletach", "płyny w beczkach", "materiały sypkie", "maszyny", "meble/AGD", "pusta naczepa", "nie wiem (zaznaczamy wszystko)"]), towary.length + "");
ok("A1 bez wyboru = nie wiem", (await s.getAttribute(".towar button.akt", "onclick")).includes("nie_wiem"));
const awaryjny = (await tekst()).includes("Tryb awaryjny");
ok("MVP: wynik z usługi na karcie (nie tryb awaryjny)", !awaryjny || process.env.AWARYJNY === "1", awaryjny ? "awaryjny" : "usługa");
await zrzut("E2-A");

// --- A2: dwa obrazy, wzorzec, klik podświetla na obu
const nazwaWz = await s.textContent(".obrazy small");
ok("A2 identyfikator wzorca", /W-[a-z]+/.test(nazwaWz), nazwaWz.trim());
await s.click(".poz:nth-child(4)");
const grube = await s.$$eval("svg rect[stroke-width='4']", (r) => r.length);
ok("A2 klik w pozycję: miejsce na obu obrazach", grube === 2, `ramki pogrubione: ${grube}`);
ok("A2 różnica podświetlona (podgląd z karty)", (await s.$$eval("svg image", (i) => i.map((x) => x.getAttribute("href")))).some((h) => /podglad|zapis\/A\.png/.test(h)));

// --- A3 + KA9 + KA12 + P36 + P41: ≤ 5, licznik raz przy nagłówku, rozwinięcie
const nag = await s.textContent(".lista h3");
const wszystkie = Number((await s.evaluate(() => S.w.miejsca.length)));
ok("A3/KA12 nagłówek zwinięty „Zaznaczenia (5) i +N dalszych miejsc”", /^Zaznaczenia \(5\) i \+\d+ dalszych miejsc/.test(nag.trim()), nag.trim());
ok("P36 licznik +N tylko raz", (await s.$$("text=/dalszych miejsc/")).length === 1);
for (const [k] of [["drobnica"], ["plyny"], ["sypkie"], ["maszyny"], ["meble"], ["pusta"], ["nie_wiem"]]) {
  await s.click(`.towar button[onclick*="'${k}'"]`);
  const n = (await poz()).length;
  ok(`A3 ≤ 5 pozycji (${k})`, n <= 5, `${n}`);
}
await s.click(".dalsze");
const nag2 = await s.textContent(".lista h3");
ok("P41/KA17 po rozwinięciu „Zaznaczenia (N)” pełna liczba", nag2.trim().startsWith(`Zaznaczenia (${wszystkie})`), nag2.trim());
const p = await poz();
ok("P35 rozwinięte: wszystkie miejsca na liście", p.length === wszystkie, `${p.length}/${wszystkie}`);
await zrzut("E2-A-rozwiniete");
await s.click(".dalsze");

// --- A9 + KA10: dopisek przy podłodze
const pp = await poz();
await s.click(".dalsze");
const pr = await poz();
ok("A9 dopisek przy pozycji w podłodze", pr.filter((x) => x.t.includes("podłoga")).every((x) => x.dop) && pr.some((x) => x.dop), pr.filter((x) => x.dop).map((x) => x.t).join("; "));
ok("A9 brak dopisku poza podłogą", pr.filter((x) => !x.t.includes("podłoga")).every((x) => !x.dop));
await s.click(".dalsze");

// --- P42: zablokowany raport z komunikatem i „rozwiń”
const brak = await s.textContent(".brakuje");
ok("P42/KA14 raport wyszarzony z „Brakuje decyzji: N, w tym M w dalszych miejscach”", /Brakuje decyzji: \d+, w tym \d+ w dalszych miejscach/.test(brak) && (await s.isDisabled("text=Raport z auta →")), brak.trim());
ok("P42 przycisk „rozwiń” przy komunikacie", !!(await s.$(".brakuje .dalsze")));

// --- KA18: kolory
const kolKontrola = await s.$eval(".poz .kontrola", (b) => getComputedStyle(b).backgroundColor);
ok("KA18 „do kontroli” niebieski", kolKontrola === "rgb(28, 126, 214)", kolKontrola);
const oceny = await s.$$eval(".poz .ocena", (e) => e.map((x) => [parseInt(x.textContent), x.className]));
ok("P37/KA18 czerwień tylko ≥ 80%", oceny.every(([v, c]) => c.includes("wys") === v >= 80), JSON.stringify(oceny));

// --- A6: odrzucenie z powodem (anuluj nie zapisuje)
const kolejnosc0 = (await poz()).map((x) => x.t);
await s.click(".poz:nth-child(4) >> text=odrzuć");
const powody = await s.$$eval(".okno button", (b) => b.map((x) => x.textContent));
ok("A6 cztery powody", ["element konstrukcji", "zwykły ładunek", "zakłócenie obrazu", "inne"].every((x) => powody.includes(x)), powody.join(", "));
await zrzut("E3");
await s.click(".okno >> text=anuluj");
ok("A6 bez powodu nie zapisuje", !(await tekst()).includes("odrzucone:"));
await s.click(".poz:nth-child(4) >> text=odrzuć");
await s.click(".okno >> text=element konstrukcji");
ok("A6 odrzucone z powodem", (await tekst()).includes("✖ odrzucone: element konstrukcji"));
// KA18: czytelność odrzuconej pozycji — kontrast tekstu ≥ 7:1
const kontrast = await s.$eval(".poz.odr", (e) => {
  const rgb = (c) => c.match(/\d+/g).slice(0, 3).map(Number);
  const L = (c) => { const [r, g, b] = rgb(c).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const t = getComputedStyle(e.querySelector(".dec")).color, tl = getComputedStyle(e).color, bg = getComputedStyle(e).backgroundColor;
  const k = (a, b) => { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  return [k(t, bg), k(tl, bg)];
});
ok("KA18 kontrast odrzuconej pozycji ≥ 7:1 (napis decyzji i tekst)", kontrast.every((k) => k >= 7), kontrast.map((k) => k.toFixed(1)).join(" / "));
// P32: kolor konturu i cofnij
ok("P32 kontur odrzuconego szary", (await s.$$eval("svg rect", (r) => r.map((x) => x.getAttribute("stroke")))).includes("#868e96"));
await s.click(".poz.odr >> text=cofnij decyzję");
ok("P32/KA15 cofnij decyzję przywraca pozycję", !(await tekst()).includes("✖ odrzucone"));
await s.click(".poz:nth-child(4) >> text=odrzuć");
await s.click(".okno >> text=element konstrukcji");

// --- A7: do kontroli nie zmienia listy
await s.click(".poz:nth-child(3) >> text=do kontroli");
ok("A7 do kontroli: oznaczenie, lista i kolejność bez zmian", (await tekst()).includes("✔ do kontroli") && JSON.stringify((await poz()).map((x) => x.t)) === JSON.stringify(kolejnosc0));
ok("P32 kontur zatwierdzonego zielony", (await s.$$eval("svg rect", (r) => r.map((x) => x.getAttribute("stroke")))).includes("#2f9e44"));

// --- P44 B / KA17: zmiana towaru zachowuje decyzje przy miejscach, które zostają
const decPrzed = await s.evaluate(() => ({ ...S.dec }));
await s.click(`.towar button[onclick*="'maszyny'"]`);
const po = await s.evaluate(() => ({ dec: { ...S.dec }, wid: widoczne().map((x) => x.id), zg: zgaszone().map((x) => x.gdzie) }));
const zostaly = Object.keys(decPrzed).filter((id) => po.wid.includes(Number(id)));
ok("P44 decyzje przy miejscach, które zostały, zachowane", zostaly.every((id) => JSON.stringify(po.dec[id]) === JSON.stringify(decPrzed[id])), `zostały ${zostaly.length}/${Object.keys(decPrzed).length}`);
ok("P44 decyzje przy wygaszonych odpadają", Object.keys(po.dec).every((id) => po.wid.includes(Number(id))));
ok("P40/KA17 wygaszanie bez dachu, podłogi i ściany przedniej", po.zg.length > 0 && po.zg.every((g) => !/^(dach|podłoga|ściana przednia)/.test(g)), `wygaszone ${po.zg.length}: ${[...new Set(po.zg)].join("; ")}`);
const wyg = await s.textContent(".wygaszone");
ok("P29/KA13 „wygaszone: N”", /wygaszone: [1-9]/.test(wyg), wyg.split("(")[0].trim());
await zrzut("E2-A-maszyny");
await s.click(`.towar button[onclick*="'pusta'"]`);
ok("P34 pusta naczepa nic nie wygasza", (await s.textContent(".wygaszone")).trim() === "wygaszone: 0");
await s.click(`.towar button[onclick*="'maszyny'"]`);

// --- decyzje przy wszystkich → E4 (A8, KA14, P38)
for (;;) { const b = await s.$(".poz:not(.zat):not(.odr) .kontrola"); if (!b) { const r = await s.$(".brakuje .dalsze"); if (r) { await r.click(); continue; } break; } await b.click(); }
await s.click("text=Raport z auta →");
const czas = (Date.now() - t0) / 1000;
const e4 = await tekst();
ok("A1/KA4 ścieżka do raportu ≤ 2 min", czas <= 120, `${czas.toFixed(1)} s (automat)`);
ok("A8 raport: kontrola, wzorzec, ocena, decyzje z powodem", ["Kontrola", "Wzorzec", "%", "odrzucone — element konstrukcji", "do kontroli"].every((x) => e4.includes(x)));
ok("P38 wiersz „Wygaszone wyborem ładunku”", /Wygaszone wyborem ładunku\s*\d+/.test(e4));
ok("P41 raport: nagłówek z pełną liczbą, bez „dalszych miejsc”", /Zaznaczenia \(\d+\) i decyzje/.test(e4) && !e4.includes("dalszych miejsc"));
await zrzut("E4-A");

// --- A11: odrzucenie nie uczy — ta sama lista po ponownej analizie
const lista1 = await s.evaluate(() => S.w.miejsca.map((x) => x.gdzie + x.ocena).join("|"));
await auto("A");
const lista2 = await s.evaluate(() => S.w.miejsca.map((x) => x.gdzie + x.ocena).join("|"));
ok("A11 po odrzuceniu ta sama lista i kolejność", lista1 === lista2);
ok("Zmiana auta: decyzje od zera", (await s.evaluate(() => Object.keys(S.dec).length)) === 0);

// --- A4: auto B
await auto("B");
const b2 = await tekst();
ok("A4 auto B: „Brak zaznaczeń” + użyty wzorzec, bez „+N”", b2.includes("Brak zaznaczeń") && b2.includes("Użyty wzorzec") && !b2.includes("dalszych miejsc"));
ok("A5 przy dobrym wzorcu brak paska niepewny", !(await s.$(".niepewny")));
await zrzut("E2-B");
await s.click("text=Raport z auta →");
const b4 = await tekst();
ok("A8 raport auta B: brak zaznaczeń + wzorzec", b4.includes("brak zaznaczeń") && /W-[a-z]+/.test(b4));
await zrzut("E4-B");

// --- A5 + KA11: własne zdjęcie (typ spoza biblioteki) → wzorzec niepewny, nazwa pliku w E4
if (process.env.WLASNY) {
  await s.goto(BASE);
  await s.setInputFiles("#plik", process.env.WLASNY);
  await s.waitForSelector(".towar", { timeout: 150000 });
  const nazwa = process.env.WLASNY.split("/").pop();
  ok("A5/KA11 własny plik: pasek „wzorzec niepewny”", !!(await s.$(".niepewny")));
  ok("KA11 własny plik: ≤ 5 + licznik", (await poz()).length <= 5);
  await zrzut("E2-wlasne");
  await s.evaluate(() => { for (const x of widoczne()) S.dec[x.id] = { k: false, powod: "inne" }; rysuj(); });
  await s.click("text=Raport z auta →");
  const w4 = await tekst();
  ok("A5/KA11 raport: „wzorzec niepewny” i nazwa pliku w polu Kontrola", w4.includes("wzorzec niepewny") && w4.includes("plik " + nazwa));
  await zrzut("E4-wlasne");
}
if (process.env.DUZY) { // pre-mortem: plik ~50 MB przez publiczny adres
  await s.goto(BASE);
  const t1 = Date.now();
  await s.setInputFiles("#plik", process.env.DUZY);
  await s.waitForSelector(".towar, .awaria", { timeout: 200000 });
  const mb = (fs.statSync(process.env.DUZY).size / 1e6).toFixed(1);
  ok(`Plik ${mb} MB przez ${BASE}: wynik z karty`, !!(await s.$(".towar")), `${((Date.now() - t1) / 1000).toFixed(1)} s, czas karty ${await s.evaluate(() => S.w && S.w.czas_s)} s`);
}

// --- A10: żadnych żądań poza własny adres
const obce = zadania.filter((u) => !u.startsWith(BASE) && !u.startsWith("data:") && !u.startsWith("blob:"));
ok("A10 bez żądań do chmury (tylko własny adres)", obce.length === 0, obce.slice(0, 3).join(" "));
ok("A10 język ekranu polski", (await s.getAttribute("html", "lang")) === "pl");

// --- tryb awaryjny: usługa nie odpowiada → zapisany wynik aut pokazu
await s.route("**/api/analiza**", (r) => r.fulfill({ status: 502, contentType: "application/json", body: '{"blad":"test","awaryjny":true}' }));
await auto("A");
ok("Tryb awaryjny: zapisany wynik z karty, oznaczony", (await tekst()).includes("Tryb awaryjny") && (await poz()).length > 0);
await s.unroute("**/api/analiza**");

const zle = wyniki.filter((w) => !w[1]);
console.log(`\nWYNIK: ${wyniki.length - zle.length}/${wyniki.length} zaliczonych${zle.length ? " — niezaliczone: " + zle.map((w) => w[0]).join("; ") : ""}`);
await przegl.close();
process.exit(zle.length ? 1 : 0);
