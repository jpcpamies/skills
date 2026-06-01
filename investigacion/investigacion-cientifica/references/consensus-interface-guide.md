# Guía Técnica de Interfaz Consensus — V2.1

Adaptada a Scholar Agent & Deep Search Scaling.

## Tabla de Contenidos
1. [Barra de Búsqueda](#1-barra-de-búsqueda)
2. [Filtros Post-Búsqueda](#2-filtros-post-búsqueda)
3. [Funcionalidades Avanzadas](#3-funcionalidades-avanzadas)
4. [Glosario de Interfaz](#4-glosario)

---

## 1. Barra de Búsqueda (Configuración Previa al Enter)

### A. Search Scope (Alcance)

**Opción**: "All over 200M papers".

No usar "Medical Mode" aunque exista. La opción "All" combinada con keywords específicos
del área de investigación garantiza capturar estudios transversales o multidisciplinares
indexados en otras categorías. El filtro semántico del prompt es suficiente para eliminar ruido.

**Estrategia "Embudo Ancho"**: buscar en "All" para capturar todo, filtrar por calidad después.

### B. Search Mode (Modo de Inferencia)

**Opción**: "PRO Mode" (✨) o "DEEP Search".

- **Quick** (NO usar): solo coincidencia de palabras clave (BM25), insuficiente para
  preguntas de investigación complejas.
- **PRO**: activa el Scholar Agent. Usa LLMs avanzados para leer abstracts recuperados
  y generar una "Synthesized Answer" validada. Analiza los Top 20 papers.
- **DEEP Search** (escalado): amplia la ventana de análisis a 50 documentos. Activar
  cuando la síntesis de 20 papers arroja resultados contradictorios ("Mixed Results") o
  insuficientes. Tiempo de cómputo: 2-5 min.

**Protocolo de escalado**: si PRO da resultados mixtos, escalar a DEEP.

## 2. Filtros Post-Búsqueda (Barra Lateral)

### A. Study Type
- **Primario**: Systematic Review, Meta-Analysis.
- **Fallback**: si no hay resultados, añadir RCT (Randomized Controlled Trial).
- **Razón**: cúspide de la pirámide de evidencia (Evidencia Secundaria) antes de bajar.

### B. Journal Quality Indicators
- **Selección**: "Rigorous Journals".
- Usa métricas SJR (Scimago Journal Rank) para identificar revistas Q1/Q2.
- Es el "Firewall" contra revistas depredadoras y ciencia de baja calidad.

### C. Year
- **Rango**: Min 2020 — Max Presente.
- **Razón**: evidencia vigente y actualizada.

## 3. Funcionalidades Avanzadas (Scholar Agent)

Si se activa modo "DEEP", Consensus ejecuta múltiples sub-búsquedas autónomas.

**Instrucción al usuario**: "Si usas DEEP search, espera a que la barra de progreso
termine completamente antes de seleccionar los papers."

## 4. Glosario

| Término | Definición |
|---------|-----------|
| **Consensus Meter** | Indicador visual Sí/No/Posiblemente. Útil para preguntas binarias. |
| **Study Snapshot** | Resumen estructurado (Población, N, Métodos) en la tarjeta del paper. |
| **Scholar Agent** | Motor de IA que ejecuta lectura y síntesis en modos Pro/Deep. |
| **SJR** | Scimago Journal Rank. Métrica de calidad de revistas científicas. |
| **Q1/Q2** | Cuartiles superiores de calidad de revistas según SJR. |
