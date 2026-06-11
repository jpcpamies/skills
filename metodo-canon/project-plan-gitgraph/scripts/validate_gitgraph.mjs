// Valida que un diagrama Mermaid gitGraph compila (y avisa si falta el bloque de color).
// Uso:  node validate_gitgraph.mjs <archivo.mermaid>
//
// NO ENSUCIA LA CARPETA DEL SKILL. El parser real (@mermaid-js/parser) se instala en un
// directorio TEMPORAL del SO (os.tmpdir()/mermaid-gitgraph-validator), nunca aquí. Así la
// carpeta del skill queda siempre limpia y "botón derecho > Comprimir" produce un .zip
// válido para subir a la superficie (sin node_modules ni paths con caracteres inválidos).
//
// Exit code 0 = OK | 1 = NO COMPILA | 2 = error de uso.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

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

// 5) parser real de Mermaid — instalado en un dir TEMPORAL del SO, NO en la carpeta del skill.
async function loadParser() {
  const scratch = path.join(os.tmpdir(), 'mermaid-gitgraph-validator');
  const pkgDir = path.join(scratch, 'node_modules', '@mermaid-js', 'parser');
  const pkgJson = path.join(pkgDir, 'package.json');
  if (!fs.existsSync(pkgJson)) {
    fs.mkdirSync(scratch, { recursive: true });
    // Instala en el scratch temporal (cwd = scratch), nunca en la carpeta del skill.
    execSync('npm i @mermaid-js/parser --no-audit --no-fund --silent', { cwd: scratch, stdio: 'ignore' });
  }
  const meta = JSON.parse(fs.readFileSync(pkgJson, 'utf8'));
  const dot = (meta.exports && meta.exports['.']) || {};
  const entry = dot.import || dot.default || meta.module || meta.main;
  if (!entry) throw new Error('no se pudo resolver el entry de @mermaid-js/parser');
  return import(pathToFileURL(path.join(pkgDir, entry)).href);
}

let parser = 'no-ejecutado';
try {
  const mod = await loadParser();
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
  parser = 'no-disponible';
  warns.push('Parser real no disponible (sin red o sin npm). Se instala solo en ' + path.join(os.tmpdir(), 'mermaid-gitgraph-validator') + ' la primera vez. Por ahora solo heurísticas.');
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
