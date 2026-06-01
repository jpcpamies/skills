# Generar PRD.md

> Escribe `PRD.md` en markdown plano (no PDF). Lo lee Claude Code para generar el `PROJECT_PLAN.md`.
> Usa las respuestas de los tres bloques. No inventes: si falta un dato, márcalo como `[TODO: ...]`.

## Estructura obligatoria

```
# PRD — [Nombre del Proyecto]
> Product Requirements Document · Canon Method · [fecha]

## 1. Resumen Ejecutivo
Problema núcleo, propuesta en 2-3 frases, veredicto de validación (painkiller).

## 2. Validación de Negocio
Founder-market fit, evidencia (si hubo), painkiller vs vitamin, diferenciación en 5 ejes.

## 3. Usuarios Objetivo
2-3 perfiles (ICP profundizado): demografía, psicografía, contexto de uso, dispositivos, willingness-to-pay.

## 4. Propuesta de Valor y Diferenciación
Qué no existe hoy, ventaja competitiva, posicionamiento.

## 5. Funcionalidades
MVP (3-5 esenciales) vs Avanzadas (deseables). Prioridad explícita.

## 6. Arquitectura Técnica
Stack elegido. Rol de la IA (NÚCLEO vs MEJORA) y tipo. Modelo de datos / flujo de datos.
Analogía del restaurante (Frontend = sala, Backend = cocina, BBDD = despensa) para claridad.

## 7. Estructura de Pantallas
Lista de pantallas con qué ve/hace el usuario en cada una.

## 8. Modelo de Negocio
Pricing, justificación, sistema de créditos/límites si aplica.

## 9. Restricciones Técnicas
Integraciones, rendimiento, cumplimiento, restricciones de coste.

## 10. Criterios de Validación (MVP)
KPIs concretos a 3 meses, umbral de viabilidad.

## 11. Hoja de Ruta
Encuadre realista por fases (alineado al FRAMEWORK_DEV Golden Order).

## 12. Metodología de Desarrollo (CAPA DE PROCESO — instrucciones para Claude Code)
[Ver bloque imperativo abajo — se copia tal cual, adaptando la URL]
```

## Bloque §12 — texto imperativo a incrustar (clave para la cascada)

Incluye este texto en el PRD (la URL del framework ya está cableada):

```markdown
## 12. Metodología de Desarrollo

Este proyecto sigue el **Canon Method**. Antes de escribir el `PROJECT_PLAN.md`, Claude Code DEBE:

1. **Traer el framework de construcción** a `/docs/FRAMEWORK_DEV.md` desde la última versión:
   `curl -fsSL https://raw.githubusercontent.com/jpcpamies/canon-framework/main/FRAMEWORK_DEV.md -o docs/FRAMEWORK_DEV.md` (o WebFetch). Si no hay red, usa la copia incluida.
2. **Generar `PROJECT_PLAN.md`** siguiendo el Golden Order de `FRAMEWORK_DEV.md`, adaptado a este PRD, en subfases atómicas.

### Capa de calidad de diseño: Impeccable (Non-slop)
Este proyecto integra **Impeccable** (https://impeccable.style), motor de calidad de diseño determinista para Claude Code.

- **Fase 0 (Bootstrap) — instalar:** `npx impeccable skills install` (autodetecta Claude Code; siempre la última versión).
  Para actualizar: `npx impeccable skills update`. Verificar comandos con `npx impeccable skills help` o tecleando `/impeccable`.
- **NO ejecutar `/impeccable teach` (ni `init`):** este proyecto YA incluye `PRODUCT.md` y `DESIGN.md` generados por CANON.
  Colócalos donde Impeccable los resuelve (raíz o `/docs/`). Opcional: `/impeccable document` cuando haya código, para
  reconciliar el `DESIGN.md` con los tokens reales.
- **Comandos por fase:**
  - Feature nueva → `/impeccable shape` luego `/impeccable craft`.
  - Iteración visual en navegador → `/impeccable live`.
  - Antes de cerrar una feature visual → `/impeccable critique` + `/impeccable polish`.
  - Pasada técnica → `/impeccable audit` → `/impeccable harden`.
  - Refinamiento dimensional → `/impeccable typeset`, `/impeccable colorize`, `/impeccable layout`.
  - Pre-commit / CI → `npx impeccable detect src/` (determinista, sin LLM).
  - Pre-ship → `/impeccable optimize`, `/impeccable harden`, `/impeccable polish`.
- **El `DESIGN.md` es la fuente de verdad visual.** Solo los comandos System (`document`, `extract`) lo modifican, a propósito.

### Filosofía anti-slop (Non-slop)
Evita los tells de UI generada por IA. Los más críticos (ver https://impeccable.style/slop):
borde-acento lateral en tarjetas, paletas morado/cian, una sola fuente (Inter) para todo, tarjetas anidadas,
texto gris sobre fondo de color, texto con degradado, icono en cuadradito sobre cada heading, eyebrow+headline gigante,
easing con rebote, copy buzzword/em-dash. El `DESIGN.md` y el `CLAUDE.md §13` codifican las reglas concretas.
```

Tras escribir el PRD, continúa con `generate-product.md`.
