---
name: conocimiento-youtube
description: Descarga masiva e incremental de transcripciones de canales y playlists de YouTube en su idioma original. Crea un archivo .txt por vídeo, un unified.md concatenado y un registry.json con el estado de cada vídeo. Soporta canales grandes con batching, backoff exponencial y reanudación tras interrupción. Usa este skill cuando el usuario pida descargar un canal de YouTube, cosechar transcripciones, obtener una base de conocimiento desde un canal o playlist, actualizar un canal previamente descargado, o cuando pegue una URL de canal o playlist de YouTube con intención de extraer su contenido textual.
---

# Conocimiento YouTube

Cosecha exhaustivamente las transcripciones de canales y playlists de YouTube
en el entorno Cowork.

**Principio rector — completitud sobre velocidad.** El objetivo es obtener el
100% del contenido descargable. Si un canal grande tarda horas o días
repartidos en varias sesiones, es aceptable. Nunca abandonar vídeos como
`failed_retriable` sin haber agotado todas las estrategias razonables.

## Modos de operación

Toda la lógica vive en `scripts/harvester.py`. Cuatro modos, invocables
conversacionalmente o desde Dispatch:

| Comando | Qué hace |
|---|---|
| `harvest <URL>` | Descarga inicial completa de un canal o playlist. |
| `harvest update <slug>` | Incremental: comprueba vídeos nuevos y reintenta `failed_retriable`. |
| `harvest status <slug>` | Muestra el `status.md` del canal/playlist. |
| `harvest retry <slug>` | Fuerza reintento de `failed_retriable` con estrategias más agresivas (auto-actualiza yt-dlp primero). |

Detección automática del tipo de URL:
- `/channel/`, `/@`, `/c/`, `/user/` → canal.
- `playlist?list=` o `&list=` → playlist.

## Estructura de salida

Dentro del directorio de trabajo de Cowork, bajo `canales/<slug>/` o
`playlists/<slug>/`:

```
transcripts/        ← un .txt por vídeo
unified.md          ← documento concatenado completo
registry.json       ← registro maestro (fuente de verdad)
logs/harvest.log    ← log cronológico (append-only)
logs/status.md      ← reporte legible regenerado cada ejecución
```

Las carpetas madre `canales/` y `playlists/` se crean automáticamente.

## Qué leer según la tarea (carga bajo demanda)

Este SKILL.md es el dispatcher. Carga la referencia que toque, no todas:

| Cuándo | Lee |
|---|---|
| Antes de procesar un canal/playlist de **>200 vídeos** (OBLIGATORIO) | `references/large-channel-strategies.md` |
| Para entender o manipular el `registry.json` y sus estados | `references/registry-schema.md` |
| Para el formato exacto de los `.txt`, `unified.md`, logs y `status.md` | `references/file-formats.md` |
| Para flags de yt-dlp, fallback, rotación de estrategias y manejo de dependencias | `references/download-engine.md` |

## Cómo procede Claude al activarse

1. Identificar la URL y el modo (inicial / update / status / retry).
2. Si es **modo inicial**:
   - Si el canal/playlist tiene >200 vídeos previstos, leer
     `references/large-channel-strategies.md` antes de empezar.
   - Si el usuario no especificó idioma, ofrecer detección automática o
     preguntar (`--lang`, por defecto `es,en`).
   - Avisar de la estimación de duración total (horas o días si aplica).
   - Confirmar antes de empezar si la estimación supera las 2 horas.
3. Lanzar `harvester.py` con los flags adecuados.
4. Mientras se ejecuta, vigilar el log e informar de hitos: lote completado,
   rate limit, cooldown.
5. Al terminar (o al pausar para cooldown), mostrar el `status.md` y explicar
   los próximos pasos.

Si un canal empieza a fallar masivamente con errores de extracción (no de
red), ejecutar `harvest retry <slug>`: actualiza yt-dlp antes de reintentar.

## Notas de uso

- Se ejecuta en local en Cowork, con acceso a la carpeta del proyecto.
- Invocable desde Dispatch (`harvest <URL>`, `harvest update <slug>`, etc.).
- Tolera interrupciones: al reanudar lee el registry y continúa donde quedó.
- Para canales enormes (5000+ vídeos) sugiere sesiones nocturnas y avisa al
  terminar cada una.
- Instalación y ejemplos de ejecución directa: ver `README.md`.
