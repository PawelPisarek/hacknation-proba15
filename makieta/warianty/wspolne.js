// Makieta: udawane dane, bez backendu.
const TOWARY = ["drobnica na paletach","płyny w beczkach","materiały sypkie","maszyny","meble/AGD","pusta naczepa","nie wiem"];
const AUTA = {
  A: { nr: "WGM 4K21 (naczepa plandeka)", wzorzec: "Pusta naczepa — plandeka 13,6 m, wzorzec W-PL-014 z 12.11.2026",
       wszystkich: 7,
       miejsca: [
        {id:1, x:120, y:215, w:150, h:40, ocena:0.94, gdzie:"podwójna podłoga, przód"},
        {id:2, x:40,  y:70,  w:45,  h:150, ocena:0.88, gdzie:"ściana przednia"},
        {id:3, x:520, y:110, w:90,  h:70, ocena:0.71, gdzie:"w towarze, środek"},
        {id:4, x:780, y:245, w:120, h:22, ocena:0.58, gdzie:"rama, tył"},
        {id:5, x:330, y:42,  w:140, h:22, ocena:0.47, gdzie:"dach"} ] },
  B: { nr: "PO 77812 (naczepa plandeka)", wzorzec: "Pusta naczepa — plandeka 13,6 m, wzorzec W-PL-014 z 12.11.2026",
       wszystkich: 0, miejsca: [] }
};
function stan(){ const p=new URLSearchParams(location.search); return {auto:p.get("auto")||"A", towar:p.get("towar")}; }
function idz(o){ const s=Object.assign(stan(),o); const p=new URLSearchParams(); for(const k in s) if(s[k]!=null) p.set(k,s[k]); location.search=p.toString(); }
// obraz RTG jako SVG (ciemne = gęste); dodatki = miejsca z ramkami
function obraz(auto, {ramki=true, roznica=false, wybrane=null, wzorzec=false}={}){
  const a=AUTA[auto]; let s=`<svg viewBox="0 0 1000 300" class="rtg" xmlns="http://www.w3.org/2000/svg">
  <defs><filter id="sz"><feTurbulence baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 .18 0"/></filter></defs>
  <rect width="1000" height="300" fill="#e9ecef"/>
  <rect x="30" y="40" width="900" height="210" fill="none" stroke="#6c757d" stroke-width="6"/>
  <rect x="30" y="250" width="900" height="14" fill="#495057"/>
  <circle cx="700" cy="278" r="18" fill="#343a40"/><circle cx="760" cy="278" r="18" fill="#343a40"/><circle cx="820" cy="278" r="18" fill="#343a40"/>`;
  if(!wzorzec){ for(let i=0;i<8;i++) s+=`<rect x="${90+i*100}" y="120" width="80" height="128" fill="#adb5bd" opacity=".75"/>`; }
  if(!wzorzec) a.miejsca.forEach(m=>{ s+=`<rect x="${m.x+8}" y="${m.y+6}" width="${m.w-16}" height="${m.h-12}" fill="#495057" opacity=".55"/>`;});
  s+=`<rect width="1000" height="300" filter="url(#sz)"/>`;
  if(roznica && !wzorzec){ s+=`<rect x="90" y="120" width="780" height="128" fill="#fcc419" opacity=".18"/>`;
    a.miejsca.forEach(m=>{ s+=`<rect x="${m.x}" y="${m.y}" width="${m.w}" height="${m.h}" fill="#e03131" opacity=".35"/>`;}); }
  if(ramki && !wzorzec) a.miejsca.forEach(m=>{ const w=wybrane===m.id; s+=`<g class="ramka" data-id="${m.id}"><rect x="${m.x}" y="${m.y}" width="${m.w}" height="${m.h}" fill="none" stroke="${w?'#e03131':'#f08c00'}" stroke-width="${w?6:4}"/><text x="${m.x+4}" y="${m.y-6}" font-size="20" fill="#c92a2a" font-weight="700">${m.id} · ${Math.round(m.ocena*100)}%</text></g>`;});
  return s+"</svg>";
}
function wycinek(auto,m){ return obraz(auto,{wybrane:m.id}).replace('viewBox="0 0 1000 300"',`viewBox="${m.x-40} ${m.y-40} ${m.w+80} ${m.h+80}"`); }
function dalsze(a){ const n=a.wszystkich-a.miejsca.length; return n>0?`<span class="dalsze">+${n} dalszych miejsc</span>`:""; }
function brak(a){ return `<div class="brak"><b>Brak zaznaczeń</b><br>System nie znalazł miejsc różnych od wzorca.<br><small>Użyty wzorzec: ${a.wzorzec}</small></div>`; }
// ekran 1 (wspólny): wybór zgłoszonego towaru przed analizą
function wyborTowaru(nazwaWariantu){
  const {auto}=stan();
  document.body.innerHTML=`<header><b>Kontrola RTG</b> · ${nazwaWariantu}</header><main class="wybor">
   <h2>Auto ${AUTA[auto].nr}</h2><p>Wczytano obraz automatycznie. Zanim system zacznie analizę, wybierz zgłoszony towar:</p>
   <div class="towary">${TOWARY.map(t=>`<button onclick="idz({towar:'${t}'})">${t}</button>`).join("")}</div>
   <p><small>„nie wiem” — system zaznacza także ładunek.</small></p>
   <p class="pokaz">Pokaz: <a href="?auto=A">auto z dodatkiem</a> · <a href="?auto=B">auto czyste</a></p></main>`;
}
function naglowek(nazwa){ const {auto,towar}=stan(); return `<header><b>Kontrola RTG</b> · ${nazwa} · Auto ${AUTA[auto].nr} · towar: <i>${towar}</i> <a href="?auto=${auto}">zmień</a> · <a href="?auto=${auto==='A'?'B':'A'}">następne auto</a></header>`; }
function decyzja(t){ alert(`Decyzja zapisana w raporcie: „${t}” (makieta — dane udawane)`); }
