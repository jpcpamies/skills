---
name: transcripcion-depurada
description: Depurador universal de transcripciones de voz a texto (Wispr Flow, Whisper, y cualquier STT). Usa este skill siempre que el usuario suba un archivo .txt con una transcripción automática y quiera depurarla, corregirla o limpiarla. También cuando mencione "transcripción", "Wispr", "whisper", "speech to text", "STT", "depurar transcripción", "limpiar transcripción", "corregir transcripción", "transcripción con errores", "identifica los hablantes", "separar hablantes", "diarización", o cualquier variación sobre limpiar, corregir o estructurar texto transcrito automáticamente. Se activa tanto si el texto tiene un solo hablante como si tiene varios. También se activa si el usuario pega texto transcrito directamente en el chat sin subir archivo.
---

# Transcripción Depurada — Depurador Universal de Transcripciones

## Qué hace este skill

Toma una transcripción automática (generada por Wispr Flow, Whisper, o cualquier motor STT) y la transforma en un documento limpio, estructurado y fiel al contenido original. Corrige errores de transcripción usando el contexto global, identifica hablantes si hay más de uno, y entrega el texto depurado listo para usar.

## Por qué importa el contexto global

Los motores STT transcriben en streaming, sin contexto. Eso produce errores predecibles: nombres propios deformados, términos técnicos mal capturados, palabras en otros idiomas distorsionadas, y fronteras de frase incorrectas. La clave para corregir bien es leer TODO el texto antes de tocar nada. El contexto global permite deducir la forma correcta de nombres y términos que aparecen mal escritos de distintas formas a lo largo del texto.

## Flujo de trabajo

### Paso 1: Obtener el texto

- Si el usuario sube un archivo .txt, leerlo desde `/mnt/user-data/uploads/`
- Si el usuario pega texto directamente en el chat, trabajar con ese texto
- Si el archivo tiene otra extensión (.md, .doc), leerlo igualmente e informar al usuario

### Paso 2: Lectura completa y análisis contextual

Antes de hacer ninguna corrección:

1. Leer el texto completo de principio a fin
2. Identificar el tema general y el dominio (tecnología, medicina, agricultura, negocios, etc.)
3. Detectar cuántos hablantes hay. Pistas típicas: cambios de registro, respuestas a preguntas implícitas, turnos de conversación, cambios de tono
4. Compilar una lista de nombres propios, términos técnicos y palabras en otros idiomas que aparecen, incluyendo sus variantes erróneas
5. Deducir la forma correcta de cada nombre/término usando frecuencia, contexto y coherencia

### Paso 3: Corrección

Aplicar las siguientes correcciones manteniendo siempre el contenido y sentido original:

**Nombres propios y términos técnicos:**
- Corregir a la forma estándar deducida del contexto
- Si aparece "Supaveis" en un texto sobre desarrollo web, corregir a "Supabase"
- Si aparece "Clode" o "Claud", corregir a "Claude"
- Si no hay certeza suficiente, marcar como `[¿término?]` para revisión humana

**Errores de transcripción comunes:**
- Homofonías mal resueltas (hay/ahí/ay, haber/a ver, echo/hecho)
- Palabras en otros idiomas mal capturadas (términos en inglés, catalán, etc., restaurar forma original)
- Cifras y datos: verificar coherencia interna

**Limpieza de oralidad:**
- Eliminar muletillas excesivas (eh, mm, o sea repetido, bueno bueno bueno)
- Eliminar falsos arranques ("lo que... lo que quiero decir es...")
- Eliminar repeticiones involuntarias
- CONSERVAR el tono natural y la personalidad de cada hablante. Esto no es una reescritura formal, es una limpieza

**Estructura:**
- Agrupar el contenido en partes temáticas numeradas con un título descriptivo cada una
- Dentro de cada parte, separar por turnos de palabra si hay varios hablantes
- Añadir párrafos donde haya cambio de tema

### Paso 4: Formato de salida

Encabezar siempre el documento con una cabecera de metadatos:

```
# [Título descriptivo de la sesión o tema principal]

**Fecha:** YYYY-MM-DD
**Hablantes:** [nombres detectados, o número si no se identifican]
**Tema:** [descripción breve del contenido]
```

Después, el cuerpo en partes temáticas numeradas con títulos descriptivos.

**Un solo hablante:**

```
## Parte 1. [Título descriptivo del bloque]

Texto depurado organizado en párrafos naturales según los cambios de tema.

## Parte 2. [Título descriptivo del bloque]

Siguiente bloque temático.
```

**Varios hablantes:**

```
## Parte 1. [Título descriptivo del bloque]

**[Nombre Hablante 1]**
Texto depurado del turno de palabra.

**[Nombre Hablante 2]**
Texto depurado del siguiente turno.

## Parte 2. [Título descriptivo del bloque]

**[Nombre Hablante 1]**
Siguiente intervención.
```

Para los nombres de hablantes: si se pueden deducir del contexto (se presentan, se nombran entre sí), usar sus nombres reales. Si no, usar "Hablante 1", "Hablante 2", etc.

No usar em dashes ni formateo excesivo. Mantener el formato limpio y directo.

### Paso 5: Notas del editor

Al final de la transcripción depurada, incluir siempre una sección:

```
---
## Notas del editor

**Hablantes detectados:** [número y nombres si se identificaron]

**Correcciones principales:**
- "Supaveis" a "Supabase" (aparece 12 veces)
- "Clode" a "Claude" (aparece 8 veces)
- "eneight" a "n8n" (aparece 3 veces)

**Términos con duda:**
- [¿Bergeron?] posible apellido, contexto insuficiente para confirmar

**Idioma principal:** Español (con términos técnicos en inglés)
**Duración estimada:** ~X minutos (basado en extensión del texto)
```

## Reglas fundamentales

- **NO resumas.** NO parafrasees. Mantén TODO el contenido semántico original, solo depurado.
- **NO censures.** Si el hablante dice una palabra malsonante o una expresión coloquial fuerte, mantenla. Es una transcripción, no una editorial.
- **NO añadas contenido.** No inventes lo que no está en el original.
- **Marca las dudas** con `[¿término?]` en vez de adivinar. Es mejor que el humano revise un término dudoso a que aparezca uno incorrecto sin señalar.
- **Conserva la voz.** Cada persona tiene su forma de hablar. La limpieza elimina ruido, no personalidad.

## Entrega

- Si el texto es corto (menos de 2000 palabras depuradas): entregar directamente en el chat
- Si el texto es largo (más de 2000 palabras depuradas): crear un archivo .md en `/mnt/user-data/outputs/` y presentarlo al usuario con `present_files`
- Nombrar el archivo con formato: `transcripcion_depurada_YYYY-MM-DD.md` (usando la fecha actual)
