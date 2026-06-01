# Motor de descarga

## Dependencias y su fragilidad

El skill depende de dos herramientas externas, declaradas en
`requirements.txt`:

- `yt-dlp` (motor primario)
- `youtube-transcript-api` (fallback)

**`yt-dlp` se rompe con frecuencia** cuando YouTube cambia su frontend. Por
eso:

- `harvester.py` verifica ambas dependencias al arrancar y aborta con un
  mensaje claro si falta alguna (`pip install -r requirements.txt`).
- El modo `retry` **auto-actualiza `yt-dlp`** (`pip install -U yt-dlp`) como
  primer paso, antes de reintentar nada. La causa nº1 de un canal "atascado"
  en `failed_retriable` es un `yt-dlp` obsoleto.
- Si un `harvest` o `update` empieza a fallar masivamente con errores de
  extracción (no de red), la primera acción recomendada es ejecutar
  `harvest retry <slug>` para forzar la actualización de `yt-dlp`.

## Comando primario (yt-dlp)

```
yt-dlp --write-auto-subs --write-subs --sub-lang <idioma_o_all> \
       --skip-download --convert-subs srt \
       --sleep-requests 2 --sleep-interval 3 --max-sleep-interval 8 \
       --retries 5 --fragment-retries 5 \
       <url_video>
```

El `.srt` resultante se procesa para extraer texto plano (eliminar
timestamps, números de fragmento, líneas vacías excesivas).

## Fallback

`youtube-transcript-api` cuando yt-dlp no consigue subtítulos.

## Rotación de estrategias por vídeo fallido

Por cada vídeo que falla, probar en orden con pausa entre intentos:

1. **A** — yt-dlp estándar.
2. **B** — yt-dlp con cookies del navegador (`--cookies-from-browser`), solo
   si el usuario lo activó.
3. **C** — yt-dlp con `--extractor-args "youtube:player_client=android,web"`.
4. **D** — `youtube-transcript-api`.

Solo después de agotar todas se marca `failed_retriable`. El detalle completo
(backoff, cooldowns, sesiones multi-día) está en
`large-channel-strategies.md`.

## Enumeración

```bash
yt-dlp --flat-playlist --no-warnings \
       --print "%(id)s|%(title)s|%(upload_date)s|%(duration)s" \
       --sleep-requests 1 \
       <url_canal_o_playlist>
```

El listado se persiste a disco (`enumeration_raw.json`) **antes** de empezar a
descargar nada. Para canales grandes, ver `large-channel-strategies.md`.
