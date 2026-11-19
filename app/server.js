// Serwer MVP na ksefbot.pl: ekrany (public/) + przekazanie /api/* do usługi na karcie OMENa (OMEN_URL).
// Bez zależności (node:http). Port 3000. Plik do 120 MB, czas oczekiwania na usługę 150 s.
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const OMEN = (process.env.OMEN_URL || "").replace(/\/$/, ""); // adres usługi tylko w zmiennej Coolify (nie w repo)
const SHA = (process.env.SOURCE_COMMIT || process.env.COOLIFY_SOURCE_COMMIT || "").slice(0, 7) || "?";
const PUB = path.join(__dirname, "public");
const TYPY = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".json": "application/json", ".png": "image/png", ".css": "text/css" };
const MAX = 120e6;

function wyslij(res, kod, obj) {
  const b = Buffer.from(JSON.stringify(obj));
  res.writeHead(kod, { "Content-Type": "application/json; charset=utf-8", "Content-Length": b.length, "Cache-Control": "no-store" });
  res.end(b);
}

function doOmena(req, res, sciezka) {
  if (!OMEN) return wyslij(res, 502, { blad: "brak OMEN_URL — usługa na karcie nieustawiona", awaryjny: true });
  const n = Number(req.headers["content-length"] || 0);
  if (n > MAX) return wyslij(res, 413, { blad: "plik większy niż 120 MB" });
  const u = new URL(OMEN + sciezka);
  const p = http.request(u, { method: req.method, headers: { "Content-Type": req.headers["content-type"] || "application/octet-stream", ...(n ? { "Content-Length": n } : {}) }, timeout: 150000 }, (r) => {
    res.writeHead(r.statusCode, { "Content-Type": r.headers["content-type"] || "application/octet-stream", "Cache-Control": r.statusCode === 200 && /^\/(podglad|wzorzec)\//.test(sciezka) ? "private, max-age=3600" : "no-store" });
    r.pipe(res);
  });
  p.on("timeout", () => p.destroy(new Error("czas minął")));
  p.on("error", (e) => { if (!res.headersSent) wyslij(res, 502, { blad: "usługa na karcie OMENa nie odpowiada: " + e.message, awaryjny: true }); else res.end(); });
  req.pipe(p);
}

http.createServer((req, res) => {
  const u = new URL(req.url, "http://x");
  if (u.pathname === "/api/wersja") return wyslij(res, 200, { sha: SHA, omen: OMEN ? "ustawiony" : "brak" });
  if (u.pathname.startsWith("/api/")) return doOmena(req, res, u.pathname.slice(4) + u.search);
  let f = path.normalize(path.join(PUB, u.pathname === "/" ? "index.html" : u.pathname));
  if (!f.startsWith(PUB) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nie ma"); }
  res.writeHead(200, { "Content-Type": TYPY[path.extname(f)] || "application/octet-stream", "Cache-Control": f.endsWith(".html") ? "no-store" : "max-age=300" });
  fs.createReadStream(f).pipe(res);
}).listen(3000, () => console.log("MVP :3000, usługa", OMEN, "sha", SHA));
