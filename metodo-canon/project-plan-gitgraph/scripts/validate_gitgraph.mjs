// Valida que un diagrama Mermaid gitGraph compila (y avisa si falta el bloque de color).
// Uso:  node validate_gitgraph.mjs <archivo.mermaid>
// Para la validación completa instala el parser real UNA VEZ en la carpeta de este skill
// (no en el repo del usuario; aquí hay un .gitignore para node_modules):  npm i @mermaid-js/parser
// Exit code 0 = OK | 1 = NO COMPILA | 2 = error de uso.
import fs from 'fs';

const file = process.argv[2];
if (!file) { console.error('uso: node validate_gitgraph.mjs <archivo.mermaid>'); process.exit(2); }
let text;
try { text = fs.readFileSync(file, 'utf8'); }
catch (e) { console.error('no se pudo leer:', file); process.exit(2); }

const problems = [];
const warns = [];

// 1) bloque de código (la causa nº1 de "Lexer error on line 1")
if (/^﻿?\s*```/.test(text)) {
  problems.push('El archivo empieza con ``` (valla de código). Quita las líneas de triple comilla: rompen mermaid.live con "Lexer error on line 1, column 1".');
}

// 2) bloque de color obligatorio en este skill (estado por color: git0..gitN)
const hasInit = /%%\{\s*init\s*:/.test(text);
const hasGit0 = /['"]git0['"]\s*:/.test(text);
if (!hasInit || !hasGit0) {
  warns.push('Falta el bloque de color %%{init: {theme:base, themeVariables:{git0..gitN}}}%%. Este skill exige codificar el ESTADO POR COLOR (verde=cerrado, rojo=NEXT, naranja=por hacer, gris=descartado). El grafo compila igual, pero no cumple la convención.');
}

// 3) quitar front matter para los chequeos estructurales
const body = text.replace(/^﻿?---\r?\n[\s\S]*?\r?\n---\r?\n/, '');

// 4) heurísticas línea a línea
const lines = body.split(/\r?\n/);
let started = false;
const ids = [];
const branches = ['main'];
const checkouts = [];
const KW = ['gitGraph', 'commit', 'branch', 'checkout', 'merge', 'cherry-pick', 'accTitle', 'accDescr'];
lines.forEach((ln, idx) => {
  const t = ln.trim();
  if (t === '' || t.startsWith('%%')) return;
  if (/^gitGraph(\s|:|$)/.test(t)) { started = true; return; }
  if (!started) return;
  if (((t.match(/"/g) || []).length) % 2 !== 0) problems.push(`L${idx + 1}: comillas sin cerrar -> ${t}`);
  const first = t.split(/[\s:]+/)[0];
  if (!KW.includes(first)) problems.push(`L${idx + 1}: instrucción no reconocida "${first}" -> ${t}`);
  if (first === 'commit') {
    const m = t.match(/id:\s*"([^"]*)"/);
    if (m) {
      ids.push(m[1]);
      if (m[1].includes('`')) problems.push(`L${idx + 1}: el id contiene backtick`);
    }
    const tm = t.match(/type:\s*([A-Za-z]+)/);
    if (tm && !['HIGHLIGHT', 'REVERSE', 'NORMAL'].includes(tm[1])) problems.push(`L${idx + 1}: type inválido "${tm[1]}" (usa HIGHLIGHT | REVERSE | NORMAL)`);
  }
  if (first === 'branch') { const b = t.split(/\s+/)[1]; if (b) branches.push(b.replace(/"/g, '')); }
  if (first === 'checkout') { const b = t.split(/\s+/)[1]; if (b) checkouts.push({ b: b.replace(/"/g, ''), l: idx + 1 }); }
});
if (!started) problems.push('No se encontró la palabra clave "gitGraph".');
const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
if (dup.length) problems.push('ids de commit duplicados (Mermaid los exige únicos): ' + [...new Set(dup)].join(' | '));
checkouts.forEach(c => { if (!branches.includes(c.b)) problems.push(`L${c.l}: checkout a una rama no declarada "${c.b}"`); });

// 5) parser real de Mermaid (si está instalado)
let parser = 'no-ejecutado';
try {
  const mod = await import('@mermaid-js/parser');
  try {
    const r = await mod.parse('gitGraph', body);
    const errs = [...((r && r.lexerErrors) || []), ...((r && r.parserErrors) || [])];
    if (errs.length) { parser = 'ERROR'; errs.slice(0, 4).forEach(e => problems.push('parser: ' + (e.message || e))); }
    else parser = 'OK';
  } catch (e) {
    parser = 'ERROR';
    problems.push('parser: ' + ((e && e.message) || String(e)).split('\n').slice(0, 5).join(' | '));
  }
} catch (e) {
  parser = 'no-instalado';
  warns.push('Parser real no disponible. Validación completa: "npm i @mermaid-js/parser" en el sandbox. Por ahora solo heurísticas.');
}

console.log(`commits: ${ids.length} | ramas: ${[...new Set(branches)].join(',')} | HIGHLIGHT: ${(body.match(/type:\s*HIGHLIGHT/g) || []).length} | parser: ${parser}`);
warns.forEach(w => console.log('WARN:', w));
if (problems.length) {
  console.log('\nNO COMPILA:');
  problems.forEach(p => console.log('  - ' + p));
  process.exit(1);
}
console.log('\nOK: el gitGraph es válido.');
process.exit(0);
