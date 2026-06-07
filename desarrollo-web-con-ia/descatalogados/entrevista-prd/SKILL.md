---
name: entrevista-prd
description: >
  Usa este skill siempre que el usuario quiera planificar una aplicación web, crear un PRD (Documento de
  Requisitos de Producto), definir los requisitos de un proyecto No-Code o Low-Code, o estructurar la idea de
  una app en una especificación formal. Actívalo cuando el usuario diga cosas como "tengo una idea de app",
  "ayúdame a planear mi app", "crea un PRD", "quiero construir una aplicación", "ayúdame a definir mi proyecto",
  "necesito un documento de requisitos", o cuando pegue una descripción larga de una idea de proyecto y quiera
  estructurarla como PRD. También se activa cuando el usuario menciona "planificación No-Code", "definición de
  MVP" o "especificación de app". Este skill conduce una entrevista estructurada (adaptándose a la información
  ya proporcionada) y luego genera un PDF profesional con el PRD completo.
---

# Entrevista PRD & Generador

> ⚠️ **DESCATALOGADO.** Este skill ya no forma parte de la familia activa del Método Canon. Lo sustituye
> **`entrevista-prd-a-proyecto`** (la génesis del método, superficie Cowork, que genera los 5 documentos de
> gobierno). `entrevista-prd` era el track **No-Code/Low-Code**: una entrevista de 12 preguntas que producía
> un único **PRD en PDF** para construir con Lovable/Bolt/V0/Cursor. Se conserva aquí solo como referencia
> histórica; **no se registra en `plugin.json`** ni se distribuye.

An interactive skill that interviews the user to gather structured information about their web application idea,
then generates a professional PRD (Product Requirements Document) as a downloadable PDF.

## Core Behavior

This skill has two modes depending on what the user provides:

### Mode A: Cold Start (no prior context)
The user says something like "I want to plan an app" without details.
→ Begin the full 12-question interview from question 1.

### Mode B: Warm Start (user provides context upfront)
The user pastes a description, brief, or large block of text about their project idea.
→ Analyze the provided text, extract all answerable information, map it to the 12 interview areas,
then ONLY ask questions for the gaps. Acknowledge what you already know before asking.

**Warm Start Protocol:**
1. Read the user's input carefully
2. For each of the 12 interview areas, determine: COVERED / PARTIAL / MISSING
3. Present a brief summary: "Based on what you've shared, I already have clarity on: [list]. I still need to explore: [list]."
4. Begin asking ONLY the missing/partial questions, adapting their wording to reference what's already known

## Interview Sequence

Ask ONE question at a time. Wait for a complete response before continuing.
If a response is vague, ask a specific follow-up before moving on.
Use a direct, collaborative, professional tone throughout.

### Question 1 — Problem & Core Concept
"¿Qué problema específico resuelve tu aplicación, y en qué situación exacta la usarían las personas?"
Seeking: Clear purpose, usage context, specific pain point.

### Question 2 — Target Users & Use Cases
"¿Quiénes son tus usuarios principales? Describe 2-3 perfiles específicos: su nivel técnico, cuándo usarían la app, qué dispositivos usan, y qué los motivaría a pagar por ella."
Seeking: Clear segmentation, usage contexts, willingness to pay.

### Question 3 — Value Proposition & Differentiation
"¿Qué hace tu app que actualmente no existe? ¿Cuál es tu ventaja competitiva específica, y por qué alguien elegiría tu solución sobre las alternativas existentes?"
Seeking: Clear differentiation, competitive advantage, positioning.

### Question 4 — Core vs Advanced Features
"Lista las 3-5 funcionalidades ESENCIALES que tu MVP debe tener para ser útil. Luego, menciona 3-5 funcionalidades 'deseables' que podrías agregar después."
Seeking: Clear prioritization, MVP scope, feature roadmap.

### Question 5 — AI Role & Type
"¿Qué papel juega la IA en tu app? ¿Es el NÚCLEO del valor (la app no funciona sin IA) o una MEJORA (mejora la experiencia pero la app aún funciona sin ella)? ¿Qué tipo específico de IA necesitas: generación de texto, análisis, clasificación, recomendaciones?"
Seeking: Phase 6 vs Phase 8 classification, OpenAI integration type.

### Question 6 — Data Flow & Transformation
"Describe el flujo de datos paso a paso: ¿Qué información ingresa el usuario? ¿Cómo se procesa? ¿Qué información reciben de vuelta? ¿Qué datos necesitas almacenar permanentemente?"
Seeking: Data flow, architecture, persistence requirements.

### Question 7 — Screen Structure & Navigation
"¿Cuántas pantallas principales tendrá tu app? Nombra cada pantalla y describe brevemente qué verá y hará el usuario en cada una."
Seeking: Information architecture, user flow, UI complexity.

### Question 8 — Business Model & Monetization
"¿Cómo planeas monetizar? ¿Freemium con límites? ¿Suscripción mensual? ¿Pago por uso? ¿Qué precios tienes en mente, y qué justificaría que alguien pague esos precios?"
Seeking: Pricing strategy, value justification, credit system.

### Question 9 — Technical Constraints & Restrictions
"¿Hay alguna limitación técnica específica que deberíamos considerar? ¿Integraciones con servicios externos? ¿Requisitos de rendimiento o volumen? ¿Cumplimiento normativo o regulaciones?"
Seeking: Technical constraints, third-party integrations, compliance.

### Question 10 — MVP Success & Metrics
"¿Cómo sabrás que tu MVP es exitoso? ¿Qué métricas específicas medirías en los primeros 3 meses? ¿Cuántos usuarios activos necesitas para considerar el proyecto viable?"
Seeking: Specific KPIs, success criteria, scalability.

### Question 11 — Timeline & Resources
"¿Qué tan pronto quieres que tu MVP esté listo? ¿Cuántas horas por semana puedes dedicar al desarrollo? ¿Tienes experiencia previa con herramientas No-Code?"
Seeking: Realistic timeline, available resources, technical experience.

### Question 12 — Preferred No-Code Tool
"¿Tienes preferencia por alguna herramienta No-Code específica? ¿Estás familiarizado con Lovable, Bolt, V0, Cursor, etc.? ¿Hay alguna razón específica para preferir una sobre otra?"
Seeking: Tool selection, specific capabilities, prior experience.

## Interview Completion

After all questions are answered (or all gaps filled in Warm Start mode), confirm with the user:

"Perfecto. Con toda esta información voy a generar tu PRD completo. El documento incluirá:
- Resumen Ejecutivo
- Arquitectura técnica (analogía del restaurante: Frontend → Backend → Base de Datos)
- Historias de Usuario y casos de uso
- Hoja de Ruta de Desarrollo fase por fase
- Especificaciones técnicas (UI, base de datos, integración IA)
- Estrategia de monetización
- Puntos de control de calidad

¿Hay algo que quieras aclarar o añadir antes de generar el documento?"

## PDF Generation

After user confirms, generate the PRD as a professional PDF using ReportLab.
Read `/mnt/skills/public/pdf/SKILL.md` for PDF creation best practices.

### PRD Document Structure

The generated PDF must follow this exact structure:

```
PORTADA
- Título: "PRD — [Nombre del Proyecto]"
- Subtítulo: "Product Requirements Document"
- Fecha de generación
- Versión: 1.0

1. RESUMEN EJECUTIVO
   1.1 Propósito del Proyecto
   1.2 Problema que Resuelve
   1.3 Métricas de Éxito

2. USUARIOS OBJETIVO
   2.1 Perfiles de Usuario (tabla con: Perfil, Nivel Técnico, Dispositivo, Motivación)
   2.2 Casos de Uso Principales

3. PROPUESTA DE VALOR
   3.1 Diferenciación
   3.2 Ventaja Competitiva
   3.3 Posicionamiento

4. FUNCIONALIDADES
   4.1 MVP — Funcionalidades Esenciales (tabla con: #, Funcionalidad, Descripción, Prioridad)
   4.2 Fase 2 — Funcionalidades Deseables
   4.3 Hoja de Ruta de Features

5. ARQUITECTURA TÉCNICA
   5.1 Visión General (analogía del restaurante)
       - Frontend = Sala del restaurante (lo que ve el cliente)
       - Backend = Cocina (donde se procesa)
       - Base de Datos = Almacén (donde se guarda)
   5.2 Flujo de Datos (paso a paso)
   5.3 Esquema de Base de Datos (tablas y relaciones)
   5.4 Rol de la IA
       - Clasificación: Fase 6 (núcleo) o Fase 8 (mejora)
       - Tipo de IA requerida
       - Prompts sugeridos para integración

6. ESTRUCTURA DE PANTALLAS
   6.1 Mapa de Navegación
   6.2 Descripción por Pantalla (tabla: Pantalla, Elementos, Acciones del Usuario)

7. MODELO DE NEGOCIO
   7.1 Estrategia de Monetización
   7.2 Estructura de Precios (tabla con tiers)
   7.3 Implementación de Pagos (Stripe sub-fases si aplica)

8. RESTRICCIONES TÉCNICAS
   8.1 Limitaciones Identificadas
   8.2 Integraciones Externas
   8.3 Requisitos de Cumplimiento

9. HOJA DE RUTA DE DESARROLLO
   9.1 Fases del Proyecto (tabla: Fase, Duración, Entregables)
   9.2 Herramienta No-Code Seleccionada y Justificación
   9.3 Recursos Necesarios

10. CRITERIOS DE VALIDACIÓN
    10.1 Puntos de Control de Calidad
    10.2 KPIs del MVP (primeros 3 meses)
    10.3 Criterios de Viabilidad
```

### PDF Styling

Use ReportLab Platypus with these specifications:
- Page size: A4
- Font: Helvetica family (Helvetica-Bold for headings, Helvetica for body)
- Title: 24pt, bold, dark blue (#1a365d)
- Heading 1: 16pt, bold, dark blue (#1a365d)
- Heading 2: 13pt, bold, dark gray (#2d3748)
- Body: 10pt, regular, black
- Tables: Light gray header (#e2e8f0), alternating row colors (#f7fafc, white)
- Margins: 2cm all sides
- Header on each page: Project name (small, gray)
- Footer on each page: Page number
- Adequate spacing between sections (Spacer of 12pt after paragraphs, 20pt before new sections)

### Important Notes for PDF Generation
- NEVER use Unicode subscript/superscript characters — use ReportLab's `<sub>` and `<super>` tags
- Use `Paragraph` objects with proper styles for all text (never raw `drawString` for body content)
- Build the full document as a `story` list and use `SimpleDocTemplate.build()`
- Include a table of contents after the cover page
- Use `Table` objects with `TableStyle` for all tabular data
- Handle long text gracefully with proper word wrapping in table cells

## Language

Conduct the entire interview and generate the PRD in the same language the user uses.
If the user writes in Spanish, everything is in Spanish. If in English, everything in English.
The PDF content language matches the conversation language.
