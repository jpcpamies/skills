---
name: master-prompt-craft
description: >
  Generador de Master Prompts en formato C.R.A.F.T. (Contexto, Rol, Acción, Formato, Target).
  Use this skill whenever the user wants to create a master prompt, a prompt profesional,
  a prompt en formato C.R.A.F.T., or any high-quality detailed prompt for ChatGPT or any LLM.
  Trigger when the user says things like "quiero crear un master prompt", "crea un prompt",
  "necesito un prompt profesional", "hazme un prompt CRAFT", "genera un prompt detallado",
  "create a master prompt", "I need a professional prompt", "build me a CRAFT prompt",
  or any variation requesting prompt engineering or prompt creation.
  This skill conducts a brief interview to understand the topic, then generates
  a complete prompt in C.R.A.F.T. format.
---

# MasterPrompt — Generador de Prompts en Formato C.R.A.F.T.

Skill interactivo que entrevista al usuario y genera prompts excepcionales en formato C.R.A.F.T. (Contexto, Rol, Acción, Formato, Target).

## Paso 1: Recoger el tema

Al invocar el skill, preguntar:

> **¡Perfecto! Vamos a crear un Master Prompt en formato C.R.A.F.T.** 🎯
>
> Necesito que me cuentes:
> 1. **¿Cuál es el tema o idea principal?** (Ej: "guía de nutrición", "plan de marketing", "asistente Python"...)
> 2. **¿Para qué modelo será?** (ChatGPT, Claude, Gemini, universal...)
> 3. **¿Algún detalle extra?** (público, formato, tono, restricciones...)

Si el usuario ya proporcionó el tema en su mensaje, NO preguntar de nuevo. Extraer la info y solo preguntar lo que falte, o generar directamente si hay contexto suficiente.

## Paso 2: Generar el prompt C.R.A.F.T.

### Estructura obligatoria — 5 secciones:

**C — Contexto:** Situación, propósito, conocimientos requeridos y "por qué" de la solicitud. Detallado para que el modelo entienda completamente la tarea.

**R — Rol:** Experto líder mundial en el sector. +20 años de experiencia. Habilidades específicas, estilo de comunicación y especialización. Aspiracional: el mejor profesional imaginable.

**A — Acción:** Lista numerada de 5-10 pasos secuenciales, claros, concretos y ejecutables. Llevan lógicamente del inicio al resultado final. Si aplica, incluir instrucción para pedir info al usuario.

**F — Formato:** Tipo exacto de estructura (texto plano, markdown, tabla, lista, código, ensayo...). Encabezados, viñetas, ejemplos. Longitud si es relevante.

**T — Target (Público objetivo):** Quién consume el contenido. Edad, profesión, nivel de conocimiento, idioma, nivel de lectura, tono, contexto cultural.

### Reglas de calidad

1. **Exhaustividad** — Sin ambigüedades en ninguna sección
2. **Especificidad** — Términos concretos, no generalidades vagas
3. **Coherencia** — Las 5 secciones alineadas entre sí
4. **Adaptabilidad** — Usar `[PERSONALIZAR: ...]` para datos que el usuario no proporcionó
5. **Idioma** — Mismo idioma del usuario (español por defecto)
6. **Rol de élite** — Siempre experto de nivel mundial

## Entrega

1. Mostrar el prompt completo en el chat con markdown limpio
2. Generar archivo `.md` descargable en `/mnt/user-data/outputs/` con nombre descriptivo (ej: `MasterPrompt-CRAFT-nutricion-deportiva.md`)

## Ejemplo de referencia

```
**CONTEXTO:**
Tu tarea es crear una guía detallada para ayudar a las personas a establecer, seguir y alcanzar objetivos mensuales. El propósito es desglosar metas grandes en pasos manejables alineados con la visión anual. Enfoque en consistencia, superar obstáculos y celebrar avances, usando técnicas SMART.

**ROL:**
Eres un coach experto en productividad con más de dos décadas de experiencia ayudando a optimizar tiempo, definir metas claras y lograr éxito sostenido. Alto nivel en formación de hábitos, estrategias motivacionales y planificación práctica. Estilo claro, motivador y práctico.

**ACCIÓN:**
1. Introducción atractiva sobre por qué los objetivos mensuales son clave.
2. Guía paso a paso para desglosar metas anuales en objetivos mensuales.
3. Estrategias para identificar prioridades mensuales.
4. Técnicas para mantener enfoque, seguimiento y ajuste de planes.
5. Ejemplos en áreas comunes (salud, carrera, finanzas, desarrollo personal).
6. Obstáculos comunes y cómo superarlos.
7. Conclusión motivadora con reflexión y mejora continua.

**FORMATO:**
Texto plano con encabezados y subencabezados claros. Listas numeradas/viñetas para pasos prácticos. Ejemplos concretos o casos de estudio.

**PÚBLICO OBJETIVO:**
Profesionales y emprendedores 25-55 años. Buscan estrategias prácticas para productividad y metas. Valoran estructura y claridad. Lenguaje sencillo y accesible.
```

## Notas
- Respirar, avanzar paso a paso, revisar coherencia antes de entregar
- Sugerir refinar temas demasiado amplios
- Ofrecer siempre iterar y mejorar el prompt generado
