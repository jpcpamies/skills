# Metodología de Operación: Asistente de Investigación con IA

Guía de uso para equipos de investigación.

## Principios de Interacción

El Asistente es un copiloto de seguridad, no un chat cualquiera. Es un auditor programado.

- **Háblale en Español**: expresarse con naturalidad, usar jerga técnica del sector.
- **Sigue el Orden**: el Asistente no permite saltar pasos (especialmente configuración
  de interfaz). Esto es por seguridad.
- **Copia y Pega**: la función principal en Fase 1 es generar "códigos" (prompts) para
  que el usuario los use en otras herramientas.

## Flujo de Trabajo Paso a Paso

### Paso 1: Activación y Definición (En el Asistente)

Abrir chat y escribir objetivo en español.

Ejemplo: *"Hola, necesitamos revisar la evidencia sobre [tema] porque creemos que
hay que actualizar el protocolo actual."*

El asistente actúa como auditor: pide definir estructura PICO para asegurar búsqueda
no sesgada. El usuario responde en español.

### Paso 2: Obtención del Prompt Maestro

El asistente genera un bloque de texto en INGLÉS TÉCNICO.

Reglas para el usuario:
1. NO traducir el texto.
2. Copiar el texto en inglés tal cual.
3. ESPERAR instrucciones de configuración antes de buscar.

### Paso 3: Ejecución en Consensus

Configuración visual antes de dar Enter:

1. Abrir Consensus.app.
2. Pegar texto en inglés en barra de búsqueda.
3. **VERIFICACIÓN VISUAL (CRÍTICO)**:
   - SCOPE (Izquierda): "All over 200M papers"
   - MODE (Derecha): "PRO" (✨) o "DEEP"
4. Pulsar ENTER.
5. FILTROS: Systematic Review + Rigorous Journals + Year > 2020.
6. Seleccionar papers basándose en Q1 y rigor.

### Paso 4: Retorno al Español (NotebookLM)

Con PDFs descargados y subidos a NotebookLM:
1. Volver al asistente: "Ya tengo los PDFs subidos."
2. El asistente da instrucciones para NotebookLM (generar contenido en español).
3. NotebookLM traduce y sintetiza la evidencia inglesa al español automáticamente.

## Ventajas para el Equipo

- **Menor Esfuerzo Cognitivo**: no necesitas dominar la terminología técnica en inglés,
  el asistente lo hace por ti.
- **Mayor Rigor**: se usa el mismo lenguaje que los investigadores de referencia mundial,
  garantizando que se recuperan los mismos papers de alta calidad.
- **Resultado Nativo**: el documento final estará en perfecto castellano.
