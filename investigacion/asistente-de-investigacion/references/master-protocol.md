# Protocolo Maestro de Investigación Híbrido con IA — V4.1

Metodología Integral: Gobernanza, Seguridad y Operativa Avanzada.

## Tabla de Contenidos
1. [Propósito y Alcance](#1-propósito-y-alcance)
2. [Arquitectura de Seguridad](#2-arquitectura-de-seguridad)
3. [Roles y Responsabilidades](#3-roles-y-responsabilidades)
4. [Fase 1: Descubrimiento](#4-fase-1-descubrimiento)
5. [Fase 2: Adquisición](#5-fase-2-adquisición)
6. [Fase 3: Análisis en NotebookLM](#6-fase-3-análisis)
7. [Fase 4: Generación de Assets](#7-fase-4-generación-matriz-de-audiencias)
8. [Control de Calidad](#8-control-de-calidad)
9. [Anexos de Auditoría](#9-anexos)

---

## 1. Propósito y Alcance

Marco obligatorio para investigación científica asistida por IA.

**Objetivos Críticos**:
- Eliminar la Alucinación: trazabilidad absoluta a fuentes primarias (DOI).
- Estandarizar la Calidad: todo entregable (técnico, divulgativo, docente) con mismos
  criterios de rigor.
- Auditoría Continua: rastro documental forense de cada decisión con asistencia de IA.

## 2. Arquitectura de Seguridad

### Principio de "Silos de Seguridad"

Dos entornos estancos para evitar contaminación:

- **Entorno de Descubrimiento** (Abierto pero Filtrado): Consensus accede a 200M papers
  con filtros Q1 y Scholar Agent.
- **Entorno de Análisis** (Cerrado y Blindado): NotebookLM como RAG cerrado. Solo
  "conoce" documentos subidos manualmente.

### Mitigación de Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Fuentes Inventadas | Consensus solo devuelve papers indexados con DOI verificado |
| Sesgo de Confirmación | Definición PICO previa obligatoria |
| Simplificación Excesiva | Prompts de Rol específicos por audiencia (Matriz de Audiencias) |

## 3. Roles y Responsabilidades

- **Investigador Principal**: ejecuta búsqueda PICO, valida abstracts, descarga PDFs,
  opera NotebookLM. Responsable final de la veracidad del contenido.
- **Revisor de Gobernanza**: audita que el protocolo se ha seguido (registro DOIs,
  Checkpoints de validación).
- **Asistente IA**: copiloto técnico. Genera prompts en inglés, guía el proceso. Sin
  autoridad sobre el contenido final.

## 4. Fase 1: Descubrimiento y Curación (Consensus)

### 4.1 Definición de la Pregunta (PICO)

Documentar obligatoriamente: Población, Intervención, Comparación, Outcome.

### 4.2 Ejecución de Búsquedas

Usar prompt en inglés generado por el Asistente.

**Configuración de interfaz obligatoria**:
- Scope: "All over 200M papers"
- Mode: "PRO" (✨) o "DEEP"

**Filtros de calidad obligatorios**:
- Study Type: Systematic Review | Meta-Analysis | RCT
- Journals: "Rigorous Journals" (Q1 - Top 25% SJR)
- Year: 2020-Present

### 4.3 Checkpoint Humano 1 (Selección)

Revisar "Study Snapshot" de cada candidato.
- Criterio de Inclusión: Relevancia directa + DOI verificable + N > 50
- Entregable: Lista de 15-20 papers seleccionados.

## 5. Fase 2: Adquisición y Custodia

### 5.1 Obtención de Fuentes Primarias
Descargar PDF completo (Full Text) desde repositorios legítimos. Prohibido usar resúmenes
de terceros.

### 5.2 Normalización de Archivos
Renombrar: `AÑO_AUTOR_TEMA_CLAVE.pdf`
Ejemplo: `2023_Smith_Intervention_Safety.pdf`

## 6. Fase 3: Análisis en NotebookLM (RAG Cerrado)

### 6.1 Ingesta Segura
1. Crear cuaderno nuevo: "PROYECTO [TEMA]".
2. Subir PDFs de la Fase 2.
3. **MANDATO DE SEGURIDAD CRÍTICO**: No activar "Web Sources" ni "Discover".
   Sistema en aislamiento (Air Gap).

### 6.2 System Prompt para NotebookLM

```
Actúa como un Investigador Senior. Tu única fuente de verdad son los documentos
proporcionados en este cuaderno. Tienes prohibido usar conocimiento externo.

REGLAS OPERATIVAS:
1. Grounding Absoluto: Si el dato no está en los PDFs, responde 'No hay evidencia en las fuentes'.
2. Trazabilidad: Cada afirmación debe llevar su cita [1] clickeable.
3. Idioma: Responde en Español profesional.
```

## 7. Fase 4: Generación de Assets (Matriz de Audiencias)

Seleccionar la VÍA correspondiente y ejecutar el prompt específico.

### VÍA A: Dirección y Gestión (Técnico)

Para: Protocolos, Guías, Justificación Económica.

**Prompt — Algoritmo de Decisión**:
```
Basado EXCLUSIVAMENTE en las fuentes subidas, genera la especificación técnica para un
diagrama de flujo del proceso. Define nodos de decisión (Sí/No) y acciones.
Cita la fuente (Guía/Estudio) de cada paso. Señala discrepancias entre fuentes si existen.
```

**Audio Overview — Debate Técnico**:
- Configuración: Focus on Evidence.
- Prompt: "Genera un debate técnico entre dos especialistas sénior analizando los
  hallazgos principales y sus implicaciones. Cita los estudios relevantes. Tono
  académico y crítico."

### VÍA B: Público General / Usuarios Finales (Divulgativo)

Para: Trípticos, Hojas informativas, Material de difusión.

**Prompt — Contenido Divulgativo**:
```
Actúa como experto en Comunicación. Redacta el contenido para un tríptico (6 caras).
Nivel: Lectura fácil (6º grado).
Frecuencias Naturales: Usa '1 de cada 10' en vez de porcentajes.
Estructura Visual: Describe qué icono debe acompañar a cada texto.
Disclaimer: Incluye nota legal de no sustitución de consulta profesional.
```

**Audio Overview — Guía para el Público**:
- Configuración: Education.
- Prompt: "Genera una conversación amable y empática para personas no especializadas.
  Desmitifica conceptos complejos con analogías sencillas. Tono cálido y tranquilizador."

### VÍA C: Docencia y Formación (Académico)

Para: Formación interna, Cursos, Seminarios.

**Prompt — Plan de Clase**:
```
Actúa como Profesor Universitario. Genera esquema de clase (45 min).
Objetivos: 3 conceptos clave.
Caso Práctico: Genera un caso ficticio basado en la evidencia para resolver.
Takeaways: Resumen de puntos de actuación clave.
```

**Audio Overview — Resumen de Estudio**:
- Configuración: Study Summary.
- Prompt: "Genera un resumen dinámico tipo 'repaso de examen'. Pregunta-Respuesta
  rápido para fijar conceptos clave."

## 8. Control de Calidad y Gobernanza

### 8.1 Checkpoint Humano 2 (Validación Click-Through)

El Investigador debe auditar el entregable final haciendo clic en al menos 3 citas
críticas por página para verificar que el texto fuente coincide con la síntesis.

**Tasa de Error Tolerable**: 0%. Si una cita es incorrecta, se regenera el documento.

### 8.2 Declaración de Metodología

Todo documento final debe incluir:
> "Generado con asistencia de IA bajo Metodología de Investigación v4.1.
> Revisado por [Nombre Investigador]."

## 9. Anexos de Auditoría

### Anexo A: Plantilla de Registro de Búsqueda
- Fecha:
- Investigador:
- Pregunta PICO:
- Términos de Búsqueda (Inglés):
- Filtros Aplicados: [ ] Systematic Review [ ] Q1 Journals [ ] Year > 2020

### Anexo B: Plantilla de Decisión de Inclusión (Checkpoint 1)

| Paper (Título/Autor) | ¿DOI Verificable? | Decisión (INCLUIR/EXCLUIR) | Justificación |
|-----------------------|-------------------|---------------------------|---------------|
| Paper 1 | [ ] | | |
| Paper 2 | [ ] | | |

### Anexo C: Checklist de Aprobación Final (Checkpoint 2)

- [ ] Registro de auditoría completo
- [ ] Todas las fuentes tienen DOI verificable
- [ ] Validación humana "Click-Through" realizada (Citas correctas)
- [ ] Metodología declarada en documento final
- [ ] Sin uso de "Discover Sources" (RAG Cerrado)
