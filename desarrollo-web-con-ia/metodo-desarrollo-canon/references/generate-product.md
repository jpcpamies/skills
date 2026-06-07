# Generar PRODUCT.md

> Escribe `PRODUCT.md` en el formato que espera Impeccable (lo lee TODOS sus comandos; es OBLIGATORIO para Impeccable).
> Al existir este archivo + DESIGN.md, el proyecto se salta `/impeccable teach`.
> Colócalo en la raíz del proyecto o en `/docs/` (Impeccable resuelve por fallback).

## Estructura (secciones canónicas de Impeccable)

```markdown
# Product

## Register
brand   <!-- o "product" — según D1 -->

## Users
[Quién usa el producto. Específico: no "usuarios" sino "fundadores en solitario evaluando una herramienta
en el móvil entre reuniones". Sale de Validate V3 + PRD P2.]

## Product Purpose
[Qué resuelve y cómo se mide el éxito. Sale de Validate V1 + PRD P1/P3.]

## Brand Personality
[Las 3 palabras concretas de D2, desarrolladas en 2-3 frases de tono. Ej: "Expert, decisive, editorial".
Tono direct / specific / rooted in craft, sin hedging.]
Three-word personality: **[palabra1, palabra2, palabra3]**.

## Anti-references
[Lista nombrada de qué evitar — D4 + eje Design de V6. Marcas/estéticas/lenguaje concretos.]

## Design Principles
[3-5 principios rectores derivados del North Star y la personalidad. Ej: "Practice what you preach",
"Show don't tell", "Editorial over marketing", "Purposeful restraint".]

## Accessibility & Inclusion
[Baseline de D9: WCAG 2.1 AA, contraste verificado, focus visible, prefers-reduced-motion, HTML semántico.]
```

Reglas: el `Register` es obligatorio (Impeccable lo usa para ajustar defaults). Personalidad con palabras reales,
nunca "moderno y limpio". Anti-references siempre nombradas, no adjetivos.

Tras escribir PRODUCT.md, continúa con `generate-design.md`.
