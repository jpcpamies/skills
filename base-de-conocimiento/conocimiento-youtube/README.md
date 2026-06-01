# Conocimiento YouTube

Skill para Cowork que cosecha exhaustivamente las transcripciones de canales y playlists de YouTube. Diseñado para **completitud sobre velocidad**: si un canal grande tarda horas o días repartidos en varias sesiones, lo asume y persiste el progreso.

## Qué hace

- Descarga TODAS las transcripciones de un canal o playlist en su idioma original.
- Guarda cada transcripción como `.txt` individual nombrado con el título del vídeo.
- Mantiene un `unified.md` concatenado con todo el contenido cronológicamente.
- Lleva un `registry.json` con estado granular de cada vídeo.
- Modo incremental cada 3 días para detectar vídeos nuevos.
- Estrategias avanzadas para canales grandes: batching, backoff exponencial, rotación de estrategias por vídeo, cooldowns nocturnos, sesiones distribuidas en días.

## Estructura de salida

```
canales/
└── nombre-canal-slug/
    ├── transcripts/
    │   ├── titulo-video-1.txt
    │   └── titulo-video-2.txt
    ├── unified.md
    ├── registry.json
    └── logs/
        ├── harvest.log
        └── status.md

playlists/
└── nombre-playlist-slug/
    └── (misma estructura)
```

## Instalación

```bash
pip install -r requirements.txt
```

Requisitos del sistema:
- Python 3.9+
- `yt-dlp` instalado y accesible vía PATH (se instala por pip).

## Uso

### Descarga inicial de un canal
```bash
python scripts/harvester.py harvest https://www.youtube.com/@nombredelcanal --lang es,en
```

### Descarga inicial de una playlist
```bash
python scripts/harvester.py harvest "https://www.youtube.com/playlist?list=PLxxx" --lang es
```

### Modo incremental (comprobar vídeos nuevos)
```bash
python scripts/harvester.py update nombredelcanal
```

### Ver estado actual
```bash
python scripts/harvester.py status nombredelcanal
```

### Forzar reintento de los failed_retriable
```bash
python scripts/harvester.py retry nombredelcanal
```

### Con cookies del navegador (para canales con restricciones)
```bash
python scripts/harvester.py harvest https://www.youtube.com/@canal --cookies-from-browser chrome
```

## Idiomas

El parámetro `--lang` admite una lista separada por comas en orden de preferencia:
- `--lang es` → solo español.
- `--lang es,en` → español primero, inglés como fallback.
- `--lang es,en,ca` → español, inglés, catalán.

Por defecto: `es,en`.

## Estados de un vídeo

| Estado | Significado | ¿Reintentable? |
|---|---|---|
| `pending` | Aún no procesado | — |
| `downloaded` | Descargado con éxito | No (ya está) |
| `failed_retriable` | Error transitorio (429, timeout, 5xx) | Sí, en próxima sesión |
| `failed_permanent` | Vídeo eliminado, privado, terminado | No |
| `no_transcript` | Sin subtítulos disponibles | No |

## Estrategias para canales grandes

Ver `references/large-channel-strategies.md` para el detalle completo. Resumen:

- **Lotes adaptativos** según tamaño del canal (15-50 vídeos/lote, pausas de 5-45min entre lotes).
- **Backoff exponencial** dentro de la sesión: 30s → 2min → 5min → ... → 4h.
- **Rotación de estrategias por vídeo**: yt-dlp estándar → con cookies → con player_client=android → youtube-transcript-api.
- **Persistencia atómica** del registry tras cada vídeo.
- **Cooldown nocturno** automático si se detectan 3 señales de bloqueo consecutivas.
- **Reanudación tras interrupción**: cierra el portátil, ábrelo mañana, ejecuta `update <slug>` y continúa donde quedó.

## Programación con Dispatch

Para automatizar updates incrementales cada 3 días, configurar Dispatch para ejecutar:

```bash
cd /ruta/a/tu/proyecto/cowork
python scripts/harvester.py update <slug>
```

## Notas de uso responsable

- Respeta los rate limits de YouTube. El skill ya está configurado para hacerlo.
- Las cookies del navegador vinculan la actividad a tu cuenta. Úsalas solo si es necesario.
- Los vídeos sin subtítulos manuales ni automáticos no se pueden descargar — esto es una limitación de YouTube, no del skill.
