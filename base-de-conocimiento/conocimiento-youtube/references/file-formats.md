# Formato de los archivos de salida

## Archivos `.txt` individuales

- **Nombre**: título del vídeo slugificado (sin caracteres especiales,
  espacios → guiones, máximo 120 caracteres). Si dos vídeos comparten título
  exacto, sufijo con los últimos 6 caracteres del `video_id`.
- **Contenido**: transcripción íntegra en idioma original, en texto corrido
  limpio. Sin timestamps, sin marcas tipo `[Music]` o `[Applause]`, sin
  etiquetas técnicas residuales.

## `unified.md`

Concatenación cronológica (más antiguo → más nuevo), formato estricto:

```
[Título del vídeo]


[Transcripción completa]


[Siguiente título]


[Siguiente transcripción]
```

Título, dos saltos de línea, transcripción, dos saltos de línea, siguiente
vídeo. **Se regenera desde cero** cada ejecución (no acumula append) para
mantener consistencia con el estado real del registry.

## `logs/harvest.log` (append-only)

Una línea por evento:

```
2026-05-08T10:00:00Z [INFO] Inicio harvest canal: @ejemplo
2026-05-08T10:00:05Z [INFO] Detectados 1247 vídeos en el canal
2026-05-08T10:00:30Z [OK] Descargado: "Título del vídeo" (id: abc123)
2026-05-08T10:01:15Z [WARN] Rate limit detectado, pausa 5min
2026-05-08T10:06:20Z [FAIL_PERM] Vídeo abc456: vídeo privado
2026-05-08T10:45:00Z [INFO] Lote 3/25 completado. Descansando 30min antes del siguiente lote.
```

## `logs/status.md` (regenerado cada ejecución)

Reporte legible en Markdown con:

- Fuente (canal o playlist), nombre, URL.
- Total de vídeos detectados.
- Descargados con éxito (con %).
- Pendientes de reintentar.
- Fallos permanentes.
- Sin transcripción disponible.
- Última ejecución y duración.
- Próxima comprobación incremental prevista.
- Estimación de tiempo restante para completitud (basada en velocidad media
  de las últimas 50 descargas).

Cuando el usuario pida "muéstrame el log de X" o "estado del canal X", el
skill enseña este `status.md`.
