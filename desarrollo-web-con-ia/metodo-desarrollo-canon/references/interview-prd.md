# Bloque 2 — PRD (Arquitectura especificada)

> Las 12 preguntas del PRD. Una a la vez, con 2-3 sugerencias tailored derivadas de lo ya respondido en Validate.
> En warm start, marca CUBIERTO/PARCIAL/FALTA y pregunta solo los huecos. NO repreguntes lo que ya salió en Validate
> (usuarios, problema, diferenciación): refiérelo y profundiza.
> Cierra con confirmación antes del bloque de Diseño.

Nota de stack: una de las preguntas decide el stack técnico. El stack por defecto del usuario es React 18 (Vite) +
TypeScript strict + Tailwind + shadcn/ui en frontend; backend/DB suele ser Convex (o Express/Supabase, o Hono/Turso);
auth con Clerk; routing Wouter. NO uses herramientas no-code (Lovable/Bolt/V0): el pipeline es Claude Code local.

## P1 — Problema y concepto núcleo
"¿Qué problema específico resuelve tu aplicación, y en qué situación exacta la usarían?"
(Si Validate lo cubrió, confirma y afina.) → `PRD` Resumen Ejecutivo.

## P2 — Usuarios objetivo y casos de uso
"¿Quiénes son tus usuarios principales? 2-3 perfiles: nivel técnico, cuándo la usan, qué dispositivos, qué los motiva a pagar."
(Profundiza el ICP de Validate.) → `PRD` Usuarios Objetivo · refuerza `PRODUCT` Users.

## P3 — Propuesta de valor y diferenciación
"¿Qué hace tu app que hoy no existe? ¿Cuál es tu ventaja competitiva y por qué te elegirían frente a alternativas?"
→ `PRD` Propuesta de Valor.

## P4 — Core vs features avanzadas
"Lista las 3-5 funcionalidades ESENCIALES del MVP. Luego 3-5 'deseables' para después."
→ `PRD` Funcionalidades (MVP scope + roadmap).

## P5 — Rol y tipo de IA
"¿Qué papel juega la IA? ¿Es el NÚCLEO del valor (sin IA no funciona) o una MEJORA? ¿Qué tipo: generación, análisis, clasificación, recomendación?"
→ `PRD` Arquitectura Técnica (clasificación IA-núcleo vs IA-mejora, tipo de integración).

## P6 — Flujo de datos y transformación
"Flujo paso a paso: ¿qué introduce el usuario, cómo se procesa, qué recibe de vuelta, qué datos hay que almacenar de forma permanente?"
→ `PRD` Arquitectura Técnica + modelo de datos.

## P7 — Estructura de pantallas y navegación
"¿Cuántas pantallas principales? Nombra cada una y qué ve/hace el usuario en ella."
→ `PRD` Estructura de Pantallas. (También informa el conteo de pantallas para el bloque de Diseño.)

## P8 — Modelo de negocio y monetización
"¿Cómo monetizas? ¿Freemium, suscripción, pago por uso? ¿Qué precios y qué los justifica?"
(Apóyate en la evidencia de willingness-to-pay de Validate.) → `PRD` Modelo de Negocio.

## P9 — Restricciones técnicas e integraciones externas
"¿Limitaciones técnicas? ¿Qué **integraciones externas** necesita (pagos, auth, email, SMS, storage, IA, analítica…)? ¿Rendimiento/volumen? ¿Cumplimiento normativo? ¿Restricciones de coste (p. ej. free tier)?"
Por cada integración nombrada, anótala explícitamente: alimentará el **bootstrap de integraciones** (§14 del `CLAUDE.md` → `references/integration-bootstrap.md`), que en Claude Code buscará el tooling oficial del servicio antes de codear.
→ `PRD` Restricciones Técnicas + lista de integraciones + alimenta restricciones operativas del `CLAUDE.md`.

## P10 — Éxito del MVP y métricas
"¿Cómo sabrás que el MVP funciona? Métricas concretas a 3 meses, usuarios activos para considerarlo viable."
→ `PRD` Criterios de Validación.

## P11 — Timeline y recursos
"¿Para cuándo el MVP? ¿Horas/semana disponibles? ¿Experiencia previa?"
→ `PRD` Hoja de Ruta (encuadre realista).

## P12 — Stack técnico
"¿Stack preferido? Por defecto: React+Vite+TS+Tailwind+shadcn; backend Convex (o Express+Supabase / Hono+Turso); auth Clerk; routing Wouter. ¿Mantenemos el default o ajustamos?"
→ `PRD` Arquitectura Técnica + **define §1-§3 del `CLAUDE.md`** (stack, estructura, comandos).

## Cierre del bloque
Resume lo capturado y confirma: "Con esto tengo el PRD. Ahora pasamos al bloque de Diseño, donde definiremos el
sistema visual (te pediré referencias visuales). ¿Listo?"
