# Estrategia Lingüística en Investigación con IA

Justificación del uso de Prompts en Inglés a través de Asistente Intermediario.

## El Problema: Sesgo del Idioma en la Ciencia

### Dominio del Inglés en Bases de Datos Q1

Más del 95% de la literatura científica de alto impacto (revistas Q1 como The Lancet,
NEJM, Nature, Science) se publica exclusivamente en inglés.

- **Búsqueda en Español**: los algoritmos priorizan coincidencias exactas o traducciones
  directas, limitando resultados a revistas regionales, ignorando el corpus de evidencia
  global reciente.
- **Búsqueda en Inglés**: acceso al 100% del corpus indexado en Semantic Scholar y
  PubMed, sin omitir meta-análisis publicados en cualquier parte del mundo.

### Precisión Semántica de los Motores de IA

Consensus usa "Vector Search" (búsqueda semántica). Los modelos de embedding están
entrenados predominantemente en corpus científicos en inglés.

- **Pérdida por Traducción**: búsquedas en español sufren traducción interna implícita
  que pierde matices técnicos de las sub-especialidades.
- **Precisión Nativa**: buscar directamente en inglés alinea la consulta con el lenguaje
  nativo de la base de datos.

## La Solución: El Asistente como Puente

Arquitectura de "Intermediario Inteligente":

### Flujo de Idiomas

| Fase | Acción | Idioma | Quién |
|------|--------|--------|-------|
| 1. Intención | Explicar qué necesitamos | ESPAÑOL | Investigador → Asistente |
| 2. Traducción | Generar consulta técnica optimizada | INGLÉS | Asistente (automático) |
| 3. Búsqueda | Interrogar base de datos mundial | INGLÉS | Asistente → Consensus |
| 4. Análisis | Leer y sintetizar evidencia | ESPAÑOL | NotebookLM → Investigador |

### Rol del Asistente

Actúa como Ingeniero de Prompts en tiempo real:

1. **Input**: El investigador habla en español natural.
   - Ejemplo: "Quiero ver qué evidencia hay sobre la eficacia de esta intervención en
     población pediátrica."
2. **Procesamiento**: Analiza la petición, identifica los términos técnicos correctos
   (MeSH u otros tesauros del dominio) y estructura la consulta.
3. **Output**: Prompt Maestro en inglés técnico.
   - Ejemplo: `Efficacy of [intervention] in pediatric population AND systematic review`

### Ventajas Operativas

- **Cero Fricción**: el investigador piensa y trabaja en su idioma materno.
- **Máxima Calidad**: la búsqueda se ejecuta con la precisión del inglés técnico.
- **Lectura en Español**: NotebookLM lee los papers en inglés y genera la síntesis en
  español perfecto.

## Conclusión

La estrategia "Input Español → Prompt Inglés → Output Español" es el estándar de oro
para equipos no angloparlantes que desean competir al máximo nivel científico.
