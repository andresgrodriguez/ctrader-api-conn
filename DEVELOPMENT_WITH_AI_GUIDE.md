# Guía de Desarrollo con Agente IA

Este documento contiene instrucciones sobre cómo interactuar eficientemente con el agente IA durante el desarrollo del proyecto Cliente API cTrader.

## Principios Generales

1. **Enfoque Incremental:** Trabajar fase por fase, módulo por módulo.
2. **Contexto Limitado:** Proporcionar solo la información necesaria para la tarea actual.
3. **Memoria Externa:** Utilizar los archivos `DEVELOPMENT_PROGRESS.md` y git commits como memoria externa.
4. **Sesiones Enfocadas:** Cada sesión con el agente debe tener objetivos claros y limitados.

## Workflow para Cada Fase

### Paso 1: Preparación
- Actualizar `DEVELOPMENT_PROGRESS.md` con la fase actual y pendientes.
- Identificar archivos/documentos relevantes para la fase.

### Paso 2: Iniciar Sesión con el Agente
- Proporcionar contexto mínimo pero suficiente.
- Especificar claramente los objetivos de la sesión.

### Paso 3: Durante la Sesión
- Guiar al agente cuando se desvíe del objetivo.
- Proporcionar información adicional solo cuando sea necesario.

### Paso 4: Finalizar Sesión
- Solicitar al agente que actualice `DEVELOPMENT_PROGRESS.md`.
- Realizar commits según las recomendaciones.
- Documentar aprendizajes o problemas para futuras sesiones.

## Plantillas de Mensajes por Fase

### Fase 0: Configuración del Entorno

**Mensaje Inicial:**
```
Estamos comenzando el desarrollo del cliente API cTrader en Python. Para la Fase 0, necesitamos configurar la estructura inicial del proyecto según README.md y DEVELOPMENT_JOURNAL.md.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Por favor, ayúdame a:
1. Crear la estructura de directorios según README.md
2. Crear un archivo requirements.txt básico
3. Actualizar .env.example si es necesario
4. Verificar la configuración necesaria para el contenedor Docker
```

**Archivos a Proporcionar:**
- README.md (sección de estructura)
- DEVELOPMENT_PROGRESS.md

### Fase 1: Módulos Base - Configuración y Logging

**Mensaje Inicial:**
```
Continuamos con el desarrollo del cliente API cTrader. Hoy trabajaremos en la Fase 1: implementación de los módulos base utils/config.py y utils/logging_setup.py.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para estos módulos:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Secciones relevantes de PROJECT_SPECIFICATIONS.md y DEVELOPMENT_JOURNAL.md

### Fase 2.1: Cliente API - Autenticación

**Mensaje Inicial:**
```
Avanzamos con el cliente API cTrader. En esta sesión implementaremos client/auth.py para la autenticación con la API.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para auth.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

También necesitarás revisar los módulos utils ya implementados.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- utils/config.py, utils/logging_setup.py (ya implementados)
- Secciones relevantes de las especificaciones

### Fase 2.2: Cliente API - Cliente Core (Parte 1)

**Mensaje Inicial:**
```
Continuamos con el desarrollo del cliente API cTrader. En esta sesión, trabajaremos en la primera parte de client/core.py, enfocándonos en la estructura básica y los métodos de conexión.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para core.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

También necesitarás revisar client/auth.py y los módulos utils ya implementados.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- client/auth.py (ya implementado)
- Secciones relevantes de las especificaciones

### Fase 2.3: Cliente API - Cliente Core (Parte 2)

**Mensaje Inicial:**
```
Continuamos con el desarrollo del cliente API cTrader. En esta sesión, completaremos la implementación de client/core.py, enfocándonos en los métodos de envío/recepción de mensajes y manejos de errores.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para core.py (parte 2):
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

También necesitamos implementar los tests de integración básicos para el cliente.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- client/core.py (parcialmente implementado)
- Secciones relevantes de las especificaciones

### Fase 3.1: Comandos CLI - Main y Estructura Base

**Mensaje Inicial:**
```
Avanzamos a la fase de implementación de comandos. En esta sesión, crearemos main.py con la estructura CLI básica y la configuración de argparse.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para main.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

Necesitaremos preparar la estructura básica para todos los comandos que implementaremos en las siguientes sesiones.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones anteriores relevantes
- Secciones relevantes de las especificaciones

### Fase 3.2: Comandos CLI - Account Info

**Mensaje Inicial:**
```
Continuamos con la implementación de comandos. En esta sesión, desarrollaremos el comando account_info para obtener información de la cuenta de trading.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para commands/account_info.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

También implementaremos pruebas para este comando.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- main.py
- Secciones relevantes de las especificaciones

### Fase 3.3: Comandos CLI - List Symbols

**Mensaje Inicial:**
```
Continuamos con la implementación de comandos. En esta sesión, desarrollaremos el comando list_symbols para listar los símbolos disponibles en la cuenta.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para commands/list_symbols.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

También implementaremos pruebas para este comando.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones relevantes previas
- Secciones relevantes de las especificaciones

### Fase 3.4: Comandos CLI - Candles

**Mensaje Inicial:**
```
Continuamos con la implementación de comandos. En esta sesión, desarrollaremos el comando candles para obtener datos históricos de velas (trendbars).

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para commands/candles.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

Este comando es más complejo ya que incluye múltiples parámetros y cálculos. También implementaremos pruebas para este comando.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones relevantes previas
- Secciones relevantes de las especificaciones

### Fase 4.1: Comandos P2 - Positions

**Mensaje Inicial:**
```
Avanzamos a los comandos de prioridad P2. En esta sesión, implementaremos el comando positions para listar las posiciones abiertas.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para commands/positions.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

También implementaremos pruebas para este comando.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones relevantes previas
- Secciones relevantes de las especificaciones

### Fase 4.2: Comandos P2 - History

**Mensaje Inicial:**
```
Continuamos con los comandos de prioridad P2. En esta sesión, implementaremos el comando history para obtener el historial de transacciones.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para commands/history.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

También implementaremos pruebas para este comando.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones relevantes previas
- Secciones relevantes de las especificaciones

### Fase 5.1: Comandos P3 - Ticks

**Mensaje Inicial:**
```
Avanzamos a los comandos de prioridad P3. En esta sesión, implementaremos el comando ticks para obtener datos históricos de ticks.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Especificaciones para commands/ticks.py:
[Copiar sección relevante de PROJECT_SPECIFICATIONS.md]

Guía de implementación:
[Copiar sección relevante de DEVELOPMENT_JOURNAL.md]

Este comando maneja grandes volúmenes de datos, por lo que necesitaremos optimizar su implementación. También implementaremos pruebas para este comando.
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones relevantes previas
- Secciones relevantes de las especificaciones

### Fase 6.1: Integración - Revisión y Correcciones

**Mensaje Inicial:**
```
Comenzamos la fase final de integración. En esta sesión, revisaremos todos los componentes, corregiremos problemas de integración y aseguraremos un manejo de errores consistente.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Por favor, ayúdame a:
1. Revisar las integraciones entre módulos
2. Verificar el formato de salida según las especificaciones
3. Mejorar el manejo de errores en todos los componentes
4. Corregir cualquier problema identificado
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones de todos los componentes
- Especificaciones de formatos de salida

### Fase 6.2: Integración - Pruebas End-to-End y Documentación Final

**Mensaje Inicial:**
```
Estamos en la fase final del proyecto. En esta sesión, completaremos las pruebas de integración, verificaremos la funcionalidad end-to-end y finalizaremos la documentación.

El estado actual se encuentra en DEVELOPMENT_PROGRESS.md.

Por favor, ayúdame a:
1. Completar los tests de integración pendientes
2. Verificar que todos los comandos funcionan correctamente end-to-end
3. Revisar y actualizar la documentación final
4. Preparar la versión 1.0.0 del cliente API cTrader
```

**Archivos a Proporcionar:**
- DEVELOPMENT_PROGRESS.md
- Implementaciones de todos los componentes
- README.md para actualizaciones finales

## Estrategia de Git

### Cuándo Hacer Commits (Obligatorios)
1. **Después de cada componente funcional completado**
2. **Al final de cada sesión de trabajo con el agente**
3. **Después de implementar tests para un componente**
4. **Después de correcciones significativas**

### Estructura de Commits
- **Formato:** `[Fase X.Y] Implementa <componente> - <descripción breve>`
- **Ejemplos:** 
  - `[Fase 1.1] Implementa utils/config.py - Carga de configuración desde env`
  - `[Fase 2.3] Implementa tests de integración para client/core.py`
  - `[Fase 3.4] Corrige manejo de errores en commands/candles.py`

## Preguntas Frecuentes para el Agente

### 1. Pérdida de Contexto
Si el agente parece "perder la pista" o el contexto, usa:
```
Vamos a retomar el foco. Estamos trabajando en la Fase X, específicamente en [componente actual]. 
El objetivo es [objetivo específico de la tarea].
```

### 2. Implementaciones Incompletas
Si una implementación queda incompleta:
```
Necesitamos completar la implementación de [componente]. 
Los aspectos pendientes son:
- [aspecto 1]
- [aspecto 2]
```

### 3. Correcciones
Si necesitas corregir algo:
```
Hay un problema con la implementación de [componente]. 
El problema específico es [descripción del problema].
Necesitamos corregirlo implementando [solución sugerida].
```

### 4. Solicitud de Explicación
Si necesitas que el agente explique algún aspecto de la implementación:
```
Por favor, explica el funcionamiento de [aspecto específico] en [componente].
Específicamente, necesito entender [punto concreto].
```

### 5. Revisión de Código
Si necesitas una revisión del código implementado:
```
Por favor, revisa la implementación de [componente] con enfoque en:
- Manejo de errores
- Eficiencia
- Adherencia a las especificaciones
- Estilo de código
```

## Ejemplos de Desarrollo Efectivo

### Ejemplo: Sesión Exitosa para utils/config.py
```
Mensaje inicial claro → Agente implementa config.py → Revisión → Solicitud de cambios menores → Implementación final → Commit
```

### Ejemplo: Manejo de Problemática
```
Agente implementa código con error → Identificar problema específico → Solicitar corrección concreta → Implementación corregida → Verificar → Commit
```

### Ejemplo: Recuperación de Contexto
```
Agente pierde contexto → "Vamos a retomar el foco..." → Revisar DEVELOPMENT_PROGRESS.md → Proporcionar información específica → Continuar implementación → Commit
```

---

Recuerda: El éxito del desarrollo con IA depende de mantener sesiones enfocadas, proporcionar contexto adecuado, y utilizar herramientas externas como DEVELOPMENT_PROGRESS.md y los commits de Git para la "memoria" del proyecto. 