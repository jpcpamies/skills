# Estrategias para canales grandes (>200 vídeos)

Este documento describe las tácticas que Claude debe aplicar cuando un canal o playlist tiene un volumen alto de vídeos. El objetivo absoluto es **completitud**: obtener el 100% del contenido descargable, aunque eso requiera horas o días repartidos en varias sesiones. La velocidad es secundaria.

## Tabla de contenidos

1. Filosofía de fondo
2. Enumeración inicial robusta
3. Procesamiento por lotes (batching)
4. Backoff exponencial multinivel
5. Rotación de estrategias por vídeo fallido
6. Persistencia atómica e idempotencia
7. Cooldowns largos y sesiones nocturnas
8. Uso de cookies de navegador
9. Detección y respuesta a bloqueos persistentes
10. Sesiones distribuidas en días
11. Reanudación tras interrupción
12. Heurísticas de finalización

---

## 1. Filosofía de fondo

YouTube no quiere que descargues su contenido masivamente. Sus defensas incluyen rate limits, captchas, bloqueos por IP, y degradación silenciosa de respuestas (devolver listados truncados o vacíos). Cualquier estrategia agresiva (paralelismo, sin pausas) provoca bloqueos que hacen el trabajo más lento, no más rápido.

La estrategia ganadora es **lenta, paciente, persistente**. Como un cosechador: ir vídeo a vídeo, dormir cuando toca, levantarse y seguir.

Cuando el skill detecta un canal grande, debe comunicarle al usuario en lenguaje claro:

> "Este canal tiene N vídeos. Con descarga responsable, calculo X horas de trabajo. Si me bloquean, puede tardar más. Voy a procesar en lotes con pausas, y si pasa cualquier cosa, el progreso se guarda tras cada vídeo. Puedes apagar el ordenador y al reanudar continúo donde quedé."

---

## 2. Enumeración inicial robusta

El listado completo del canal/playlist es el cimiento. Si falla o queda incompleto, todo lo demás falla en cascada.

### Comando base

```bash
yt-dlp --flat-playlist --no-warnings \
       --print "%(id)s|%(title)s|%(upload_date)s|%(duration)s" \
       --sleep-requests 1 \
       <url_canal_o_playlist>
```

### Salvaguardas

1. **Guardar el listado inmediatamente** a un archivo `enumeration_raw.txt` en el directorio del canal antes de hacer nada más.
2. **Validación de cardinalidad**: si yt-dlp reporta menos de 10 vídeos en un canal que claramente tiene más (heurística: el usuario dijo que es un canal grande, o la página principal indica miles de subs), reintentar la enumeración 3 veces con esperas de 2-5 minutos entre intentos.
3. **Doble fuente para canales**: para canales, ejecutar la enumeración tanto en la URL `/videos` como en la URL `/streams` y `/shorts` si existen. Combinar resultados deduplicando por `video_id`.
4. **Paginación grande**: para canales de >1000 vídeos, añadir `--playlist-items 1:5000` en pasos sucesivos si la enumeración completa falla.

### Si la enumeración falla repetidamente

Marcar el harvest como "enumeración pendiente", esperar 30 minutos, reintentar. No empezar a descargar vídeos individuales hasta tener el listado completo, porque el registry necesita conocer el universo total para calcular `pending`.

---

## 3. Procesamiento por lotes (batching)

No descargar 1000 vídeos seguidos sin respirar. El skill procesa en lotes:

| Tamaño del canal | Lote | Pausa entre lotes |
|---|---|---|
| <200 vídeos | 50 | 5 min |
| 200-500 | 30 | 10 min |
| 500-1500 | 25 | 20 min |
| 1500-3000 | 20 | 30 min |
| >3000 | 15 | 45 min |

Entre vídeos del mismo lote: pausa aleatoria de 3-8 segundos (configurada vía `--sleep-interval` y `--max-sleep-interval`).

Tras completar un lote, escribir en `harvest.log`:
```
2026-05-08T10:45:00Z [INFO] Lote 3/25 completado (75/625 vídeos). Descansando 30min antes del siguiente lote.
```

---

## 4. Backoff exponencial multinivel

Cuando un vídeo falla por motivo retriable (429, timeout, 5xx), aplicar escalera de espera **dentro del mismo intento de harvest**:

| Fallo nº | Espera antes del reintento |
|---|---|
| 1 | 30 segundos |
| 2 | 2 minutos |
| 3 | 5 minutos |
| 4 | 15 minutos |
| 5 | 30 minutos |
| 6 | 1 hora |
| 7 | 2 horas |
| 8 | 4 horas |

Tras el 8º fallo consecutivo del mismo vídeo en una sesión, marcarlo como `failed_retriable` (no como permanente) y seguir con el siguiente. En sesiones futuras se reintentará desde cero.

**Detección del tipo de error**:
- 429 (Too Many Requests) → backoff inmediato.
- "Sign in to confirm you're not a bot" → backoff largo + activar cookies si están disponibles.
- "Video unavailable" sin más → comprobar contexto: si el siguiente vídeo también falla, es problema general (esperar); si es solo este, es `failed_permanent`.

---

## 5. Rotación de estrategias por vídeo fallido

Cuando un vídeo falla con yt-dlp estándar, **no rendirse**. Probar alternativas en orden:

### Estrategia A — yt-dlp con flags base
```
yt-dlp --write-auto-subs --write-subs --sub-lang <idioma> \
       --skip-download --convert-subs srt
```

### Estrategia B — yt-dlp con cookies del navegador
```
yt-dlp --cookies-from-browser chrome \
       --write-auto-subs --write-subs --sub-lang <idioma> \
       --skip-download --convert-subs srt
```

(Requiere que el usuario haya iniciado sesión en YouTube en Chrome y haya activado el flag `--enable-cookies` al lanzar el harvester.)

### Estrategia C — yt-dlp con extractor-args
```
yt-dlp --extractor-args "youtube:player_client=android,web" \
       --write-auto-subs --write-subs --sub-lang <idioma> \
       --skip-download --convert-subs srt
```

Cambiar el cliente de extracción a "android" a veces evita bloqueos que afectan al cliente "web".

### Estrategia D — youtube-transcript-api (Python)
Usar la librería `youtube-transcript-api` directamente:
```python
from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_principal, 'en'])
```

### Estrategia E — yt-dlp con proxy / VPN (si está configurado)
```
yt-dlp --proxy <proxy_url> ...
```

Solo si el usuario lo ha configurado explícitamente.

### Orden de aplicación
Por cada vídeo fallido, probar A → B → C → D → E secuencialmente, con pausa de 1-3 minutos entre estrategias. Solo después de fallar las cinco se marca `failed_retriable`.

---

## 6. Persistencia atómica e idempotencia

El `registry.json` es la fuente de verdad. Reglas:

- **Escritura atómica**: escribir a `registry.json.tmp` y renombrar a `registry.json` (rename atómico en POSIX). Nunca dejar el archivo en estado intermedio corrupto.
- **Escritura tras cada vídeo**: actualizar el registry inmediatamente después de cada descarga (éxito o fallo). Coste: ~5ms. Beneficio: si se corta la luz al vídeo 847 de 1500, no se pierde nada.
- **Backup rotativo**: cada 100 vídeos procesados, copiar `registry.json` a `registry.json.backup`. Si la escritura principal se corrompe, queda el backup.
- **Idempotencia**: cualquier vídeo en estado `downloaded` se salta automáticamente. Reejecutar el harvester 100 veces seguidas debe ser seguro y rápido (solo procesa lo pendiente).

---

## 7. Cooldowns largos y sesiones nocturnas

Si en una sesión se detectan **3 errores 429 consecutivos** o **un mensaje "Sign in to confirm you're not a bot"**, el skill activa "modo cooldown nocturno":

1. Pausar el harvest.
2. Escribir en log: "Rate limit persistente detectado. Recomiendo pausar 6-12h. Reanudar mañana o esta noche."
3. Mostrar al usuario el `status.md` actualizado.
4. Salir limpiamente.

El usuario puede entonces:
- Esperar y reanudar manualmente con `harvest update <nombre>`.
- Programar Dispatch para reanudar a las 3am.

---

## 8. Uso de cookies de navegador

Para canales con vídeos que requieren login (age-gated, miembros) o cuando los rate limits son agresivos, las cookies del navegador ayudan.

**Activación**: el usuario lanza el harvester con `--cookies-from-browser chrome` (o firefox, brave, etc.).

**Riesgos a comunicar**:
- Las cookies expiran y pueden requerir re-login.
- YouTube puede vincular la actividad a la cuenta del usuario.
- Si se hace muy agresivo, la cuenta puede recibir un aviso.

**Recomendación por defecto**: NO usar cookies salvo que un canal lo requiera o los rate limits sean insalvables sin ellas.

---

## 9. Detección y respuesta a bloqueos persistentes

Patrones que indican bloqueo serio (no solo rate limit puntual):

| Patrón | Respuesta |
|---|---|
| Mismos errores en 5+ vídeos consecutivos | Pausa de 1h + cambio de estrategia |
| Mensaje literal "Sign in to confirm you're not a bot" | Cooldown nocturno (6-12h) |
| Listados de canal devuelven vacíos | Pausa de 30min + reintento de enumeración |
| Tiempos de respuesta súbitamente >30s | Posible throttling: pausa 15min |
| Errores DNS o de red | Comprobar conectividad antes de marcar fallos |

---

## 10. Sesiones distribuidas en días

Para canales muy grandes (3000+ vídeos), una sola sesión es inviable. El skill divide explícitamente:

### Plan de sesión multi-día

Al detectar un canal de >3000 vídeos, el skill propone al usuario:

> "Este canal tiene N vídeos. Recomiendo dividir en sesiones de 4-6 horas con descansos de 12-18h entre sesiones. Plan estimado: M sesiones repartidas en D días. ¿Quieres que lo planifique?"

Si el usuario acepta, el skill:

1. Establece un objetivo de vídeos por sesión (ej. 500/sesión).
2. Tras alcanzar el objetivo, hace cooldown forzado y avisa.
3. La siguiente sesión se reanuda con `harvest update <nombre>` (manualmente o vía Dispatch).

### Programación con Dispatch

Si el usuario quiere automatizarlo:
- Crear comando Dispatch para reanudar cada noche a las 2am.
- El skill detecta automáticamente que es continuación y procesa el siguiente lote.

---

## 11. Reanudación tras interrupción

Cualquier ejecución del harvester debe empezar leyendo el `registry.json` existente:

1. Si no existe → primera ejecución, crear de cero.
2. Si existe → leer estado y continuar:
   - Vídeos en `pending` → procesar.
   - Vídeos en `failed_retriable` → reintentar (resetear `attempts` a 0 si la última ejecución fue hace >24h).
   - Vídeos en `downloaded` → omitir.
   - Vídeos en `failed_permanent` o `no_transcript` → omitir.

3. Tras procesar todos los pendientes, regenerar `unified.md` y actualizar `status.md`.

**Reanudación correcta**: el usuario debe poder cerrar el portátil a mitad del harvest, abrirlo al día siguiente, lanzar `harvest update <nombre>` y ver que continúa exactamente donde quedó, sin redescargar nada ya hecho.

---

## 12. Heurísticas de finalización

¿Cuándo se considera "completo" un harvest?

### Definición de completitud
Un harvest está completo cuando:
- `pending == 0` Y
- `failed_retriable == 0` (tras 3 sesiones de reintentos espaciados al menos 24h).

Mientras queden `failed_retriable`, el skill seguirá reintentándolos en cada ejecución.

### Cuándo desistir
Solo desistir y marcar `failed_permanent` cuando:
- El vídeo ha sido reintentado en al menos **5 sesiones distintas** separadas por al menos 24h cada una, fallando con todas las estrategias A-E.
- O el error es claramente permanente: "Video unavailable" estable, "This video has been removed", cuenta cancelada, etc.

### Reporte de completitud
Cuando el harvest queda completo, el `status.md` muestra prominentemente:

```
✅ HARVEST COMPLETO
Canal: @ejemplo
Total de vídeos detectados: 1247
Descargados con éxito: 1198 (96.1%)
Sin transcripción disponible: 47 (3.8%)
Fallos permanentes: 2 (0.1%)

Próxima comprobación incremental: 2026-05-11
```

Y se notifica al usuario explícitamente.
