# Esquema del `registry.json`

El `registry.json` es el corazón del sistema y la única fuente de verdad. El
`unified.md` y el `status.md` se regeneran desde él en cada ejecución.

## Estructura

```json
{
  "source": {
    "type": "channel | playlist",
    "name": "Nombre legible",
    "slug": "nombre-slug",
    "url": "https://...",
    "id": "UCxxxxx | PLxxxxx",
    "first_harvest": "ISO8601",
    "last_harvest": "ISO8601",
    "last_incremental_check": "ISO8601"
  },
  "stats": {
    "total_videos": 0,
    "downloaded": 0,
    "failed_retriable": 0,
    "failed_permanent": 0,
    "no_transcript_available": 0,
    "pending": 0
  },
  "videos": {
    "<video_id>": {
      "title": "...",
      "url": "...",
      "published_at": "ISO8601",
      "duration_seconds": 0,
      "status": "downloaded | pending | failed_retriable | failed_permanent | no_transcript",
      "attempts": 0,
      "last_attempt": "ISO8601",
      "last_error": "string o null",
      "transcript_filename": "titulo-slug.txt",
      "language_detected": "es"
    }
  }
}
```

## Estados de un vídeo

| Estado | Significado | ¿Reintentable? |
|---|---|---|
| `pending` | Aún no intentado | — |
| `downloaded` | Éxito, archivo `.txt` creado | No (ya está) |
| `failed_retriable` | Error transitorio (rate limit, timeout, 5xx) | Sí, en próxima sesión |
| `failed_permanent` | Vídeo eliminado, privado, geobloqueo absoluto, cuenta terminada | No |
| `no_transcript` | Sin subtítulos manuales ni automáticos | No |

## Reglas de persistencia

- **Escritura atómica**: escribir a `registry.json.tmp` y renombrar (rename
  atómico POSIX). Nunca dejar el archivo en estado intermedio corrupto.
- **Escritura tras cada vídeo**: actualizar inmediatamente después de cada
  descarga (éxito o fallo). Si se corta la luz al vídeo 847 de 1500, no se
  pierde nada.
- **Backup rotativo**: cada 100 vídeos procesados, copiar a
  `registry.json.backup`.
- **Idempotencia**: cualquier vídeo `downloaded` se salta automáticamente.
  Reejecutar el harvester N veces seguidas es seguro y rápido.
