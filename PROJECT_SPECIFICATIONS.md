# Especificaciones Detalladas: Cliente API cTrader

## 1. Introducción y Objetivo

**1.1. Propósito:**
Este documento define las especificaciones técnicas y funcionales para un cliente Python diseñado para interactuar con la API Open de cTrader. El cliente permitirá la recuperación de datos financieros y de cuenta, operando principalmente como una herramienta CLI dentro de un contenedor Docker (`ctrader-api-conn`).

**1.2. Alcance:**
*   Autenticación segura con la API de cTrader usando credenciales proporcionadas (RF-001).
*   Conexión estable a los endpoints de la API (Demo/Live) (RF-002).
*   Implementación de comandos CLI para:
    *   Obtener información de la cuenta (RF-003).
    *   Listar símbolos disponibles (RF-004).
    *   Obtener datos históricos de velas (trendbars) (RF-005).
    *   Obtener datos históricos de ticks (RF-006).
    *   Listar posiciones abiertas (RF-007).
    *   Listar historial de transacciones (deals) (RF-008).
*   Manejo de la comunicación asíncrona con la API (basada en Twisted) (RNF-006).
*   Procesamiento básico y visualización de los datos obtenidos en la consola (RF-014).
*   Configuración flexible mediante variables de entorno y argumentos CLI (RNF-004).
*   Registro (logging) detallado de operaciones y errores (RF-012).
*   Diseño modular y mantenible (RNF-007).

**1.3. Exclusiones:**
*   Gestión de la infraestructura Docker (se asume contenedor preexistente).
*   Interfaz Gráfica de Usuario (GUI).
*   Lógica de trading algorítmico (enfoque en obtención de datos).
*   Almacenamiento persistente avanzado (más allá de archivos de log y salidas simples en `/app/data`).
*   Suscripción y manejo de flujos de datos en tiempo real (ej. `ProtoOASpotEvent` continuo). El enfoque inicial es en solicitudes de datos históricos o de estado actual.

## 1.bis. Glosario de Términos cTrader

*   **ctidTraderAccountId:** Identificador único numérico de una cuenta de trading en cTrader.
*   **symbolId:** Identificador único numérico para un instrumento financiero (ej. EURUSD, XAUUSD) dentro de un broker específico.
*   **Trendbar / Vela:** Representación de la variación del precio en un período de tiempo, con precios de Apertura, Máximo, Mínimo y Cierre (OHLC) y Volumen.
*   **Tick:** Cambio individual en el precio (Bid o Ask).
*   **Deal:** Una transacción ejecutada que afecta el balance de la cuenta (ej. abrir/cerrar posición, comisión, depósito).
*   **Position:** Una exposición abierta en el mercado para un símbolo específico (puede consistir en uno o más deals).
*   **Proto Message:** Formato de serialización de datos (Protocol Buffers) usado por la API Open de cTrader para las solicitudes (`...Req`) y respuestas (`...Res`).
*   **PayloadType:** Campo en los mensajes Proto que identifica el tipo de mensaje específico (ej. `PROTO_OA_GET_TRENDBARS_RES`).
*   **Client ID / Client Secret:** Credenciales de aplicación necesarias para la autenticación inicial (`ProtoOAApplicationAuthReq`).
*   **Access Token:** Token temporal obtenido tras la autenticación de la aplicación, necesario para autorizar operaciones en una cuenta (`ProtoOAAccountAuthReq`).
*   **Enum:** Tipo de dato enumerado usado en los mensajes Proto (ej. `ProtoOATrendbarPeriod`, `ProtoOAQuoteType`).
*   **Timestamp:** Marca de tiempo en milisegundos desde la época Unix (1 Enero 1970 UTC), usada frecuentemente en la API.

## 2. Requisitos

**2.1. Requisitos Funcionales (RF) - Priorizados:**

*   **P0 (Crítico):**
    *   **RF-001 (Autenticación):** El cliente debe autenticarse con la API usando `Client ID`, `Client Secret` (para obtener `Access Token`) y `Account ID` (`ctidTraderAccountId`) para autorizar la cuenta. Las credenciales se leerán de variables de entorno.
    *   **RF-002 (Conexión):** Debe establecer y mantener una conexión TCP/TLS con el host y puerto API especificados (configurable Demo/Live vía variable de entorno `CTRADER_API_HOST` o argumento `--host`).
    *   **RF-009 (Manejo Respuestas):** Debe decodificar correctamente los mensajes Protobuf recibidos de la API.
    *   **RF-010 (Manejo Errores API):** Debe detectar, registrar y reportar al usuario errores específicos devueltos por la API (ej. `errorCode` en respuestas).
    *   **RF-011 (Manejo Errores Conexión):** Debe gestionar desconexiones inesperadas (loggear, detener limpiamente).
    *   **RF-012 (Logging):** Debe registrar eventos críticos (conexión, autenticación, errores) en archivos dentro de `/app/data/logs` con niveles configurables.
    *   **RF-013 (Interfaz CLI Básica):** Debe usar `argparse` para gestionar comandos básicos (al menos `help` y uno funcional) y opciones globales (`--host`, `--log-level`).
*   **P1 (Alto):**
    *   **RF-003 (Info Cuenta):** Comando `account_info` (usando `ProtoOATraderReq`/`ProtoOATraderRes`).
    *   **RF-004 (Listar Símbolos):** Comando `list_symbols` (usando `ProtoOASymbolsListReq`/`ProtoOASymbolsListRes`).
    *   **RF-005 (Obtener Velas):** Comando `candles` (usando `ProtoOAGetTrendbarsReq`/`ProtoOAGetTrendbarsRes`). Incluir parámetros `symbolId`, `period`, y rango temporal.
*   **P2 (Medio):**
    *   **RF-007 (Listar Posiciones):** Comando `positions` (usando `ProtoOAGetPositionListReq`/`ProtoOAGetPositionListRes`).
    *   **RF-008 (Listar Historial):** Comando `history` (usando `ProtoOAGetDealListReq`/`ProtoOAGetDealListRes`). Incluir parámetros de rango temporal.
*   **P3 (Bajo):**
    *   **RF-006 (Obtener Ticks):** Comando `ticks` (usando `ProtoOAGetTickDataReq`/`ProtoOAGetTickDataRes`). Incluir parámetros `symbolId`, `type`, y rango temporal.
    *   **RF-014 (Salida de Datos a Archivo):** Opción para guardar la salida en archivos (`--output-file` o similar).

**2.2. Requisitos No Funcionales (RNF):**
*   **RNF-001 (Lenguaje):** Python >= 3.8.
*   **RNF-002 (Librería API):** Uso obligatorio de `ctrader-open-api` (`OpenApiPy`).
*   **RNF-003 (Entorno Ejecución):** Contenedor Docker `ctrader-api-conn`.
*   **RNF-004 (Seguridad Credenciales):** Las credenciales (`Client ID`, `Secret`, `Account ID`, `Access Token`) NUNCA deben estar hardcodeadas. Se gestionarán exclusivamente vía variables de entorno (leídas desde `.env` por Docker Compose o pasadas directamente).
*   **RNF-005 (Calidad Código):** Código limpio, bien comentado (docstrings), modular (siguiendo la estructura definida), siguiendo PEP 8.
*   **RNF-006 (Asincronía):** Uso correcto del framework Twisted para operaciones asíncronas.
*   **RNF-007 (Mantenibilidad):** Código organizado para facilitar futuras extensiones o modificaciones.
*   **RNF-008 (Rendimiento):** Si bien no es el foco principal, evitar operaciones bloqueantes innecesarias y ser consciente del uso de recursos al solicitar grandes volúmenes de datos.
*   **RNF-009 (Dependencias):** Gestionadas a través de `requirements.txt`, utilizado en la construcción de la imagen Docker.

**2.3. Requisitos del Entorno (Contenedor `ctrader-api-conn`):**
*   **RE-001:** SO Linux base (ej. `python:3.10-slim`).
*   **RE-002:** Python >= 3.8 instalado.
*   **RE-003:** Librerías listadas en `requirements.txt` instaladas (incluyendo `ctrader-open-api`, `Twisted`, `protobuf`, `pyOpenSSL`, `service_identity`, `python-dotenv`, `pandas` (opcional pero recomendado para datos)).
*   **RE-004:** Variables de entorno requeridas (`CTRADER_CLIENT_ID`, `CTRADER_CLIENT_SECRET`, `CTRADER_ACCOUNT_ID`) configuradas.
*   **RE-005:** Variables de entorno opcionales (`CTRADER_API_HOST`, `CTRADER_API_PORT`, `LOG_LEVEL`, `OUTPUT_DIR`, `ACCESS_TOKEN`) disponibles.
*   **RE-006:** Acceso a Internet para conectar a `*.ctraderapi.com` en el puerto `CTRADER_API_PORT` (def. 5035).
*   **RE-007:** Volumen mapeado para `/app/data` para persistencia de logs y salidas.
*   **RE-008:** Volumen mapeado para `/app/src` para desarrollo iterativo.

## 3. Arquitectura y Tecnologías

*   **Lenguaje:** Python 3
*   **Framework Asíncrono:** Twisted
*   **Librería API cTrader:** `ctrader-open-api` (OpenApiPy)
*   **Comunicación API:** Protocol Buffers sobre TCP/TLS
*   **Interfaz de Usuario:** Command Line Interface (CLI) usando `argparse`
*   **Entorno de Ejecución:** Contenedor Docker (`ctrader-api-conn`)
*   **Gestión de Configuración:** `python-dotenv` para variables de entorno + `argparse` para overrides CLI.
*   **Logging:** Módulo `logging` de Python.
*   **Estructura del Proyecto:** Ver sección correspondiente en `README.md`.
*   **(Recomendado) Manipulación de Datos:** `pandas` (especialmente para velas y ticks).

## 4. Funcionalidades Detalladas y Formatos de Salida

*(Se detallan los mensajes Proto clave y el formato **exacto** de salida esperado para cada comando)*

*   **4.1. Módulo `client` (`src/client/`):**
    *   `auth.py`: Lógica para `ProtoOAApplicationAuthReq` -> `ProtoOAApplicationAuthRes` y `ProtoOAAccountAuthReq` -> `ProtoOAAccountAuthRes`. Maneja obtención y almacenamiento temporal del `accessToken`.
    *   `core.py`: Clase `CTraderClient`. Gestiona `Client` de OpenApiPy, callbacks (`_on_connect`, `_on_disconnect`, `_on_message`), envío de mensajes con manejo de `Deferreds` y `clientMsgId`.

*   **4.2. Módulo `commands` (`src/commands/`):**

    *   **`account_info.py` (RF-003):**
        *   **Mensajes:** `ProtoOATraderReq` (input: `ctidTraderAccountId`), `ProtoOATraderRes` (output: contiene `ProtoOATrader`).
        *   **Salida Consola (Formato Exacto):**
            ```text
            --- Account Info (ID: {ctidTraderAccountId}) ---
            Broker Name: {brokerName}
            Account Type: {accountType} ({leverageInCents / 100}:1)
            Balance: {balance / 100.0:.2f} {depositAsset.name}
            Equity: {equity / 100.0:.2f} {depositAsset.name}
            Margin Used: {marginUsed / 100.0:.2f} {depositAsset.name}
            Free Margin: {freeMargin / 100.0:.2f} {depositAsset.name}
            Margin Level: {marginLevel:.2f} %
            Total Positions: {totalPositionsCount}
            ```
            *(Nota: `balance`, `equity`, etc. vienen en centavos; `depositAsset.name` es la moneda)*

    *   **`list_symbols.py` (RF-004):**
        *   **Mensajes:** `ProtoOASymbolsListReq` (input: `ctidTraderAccountId`), `ProtoOASymbolsListRes` (output: lista de `ProtoOALightSymbol` y `ProtoOASymbolCategory`).
        *   **Salida Consola (Formato Exacto):** (Tabla formateada, usar tabulate o similar)
            ```text
            --- Available Symbols (Account: {ctidTraderAccountId}) ---
              ID  Symbol Name         Category Name        Enabled
            ----  ------------------  -------------------  -------
            {id}  {symbolName:<18}  {categoryName:<19}  {enabled}
            ... (más símbolos)
            ```

    *   **`candles.py` (RF-005):**
        *   **Mensajes:** `ProtoOAGetTrendbarsReq` (inputs: `ctidTraderAccountId`, `symbolId`, `period`, `fromTimestamp`, `toTimestamp`), `ProtoOAGetTrendbarsRes` (output: lista de `ProtoOATrendbar`).
        *   **Argumentos CLI:** `--symbol-id <int>`, `--period <str>`, (`--weeks <int>` | `--days <int>` | `--from <YYYY-MM-DD>` `--to <YYYY-MM-DD>`). Validar `period` contra `ProtoOATrendbarPeriod` enum.
        *   **Salida Consola (Formato Exacto):** (Tabla formateada)
            ```text
            --- Candles {symbolName} ({symbolId}) {period} (Account: {ctidTraderAccountId}) ---
            Timestamp (UTC)        Open      High       Low     Close    Volume
            -------------------  --------  --------  --------  --------  --------
            {YYYY-MM-DD HH:MM:SS}  {open:.5f}  {high:.5f}  {low:.5f}  {close:.5f}  {volume}
            ... (más velas)
            ```
            *(Nota: OHLC se derivan de `deltaOpen`, `deltaHigh`, `low`, `deltaClose` relativo a `low` y se multiplican por `symbol.pipValue`. Timestamps son UTC en ms)*

    *   **`positions.py` (RF-007):**
        *   **Mensajes:** `ProtoOAGetPositionListReq` (input: `ctidTraderAccountId`), `ProtoOAGetPositionListRes` (output: lista de `ProtoOAPosition`).
        *   **Salida Consola (Formato Exacto):** (Tabla formateada)
            ```text
            --- Open Positions (Account: {ctidTraderAccountId}) ---
            Position ID  Symbol Name    Volume     Trade Side    Entry Price    Timestamp (UTC)      P/L (Gross)
            -----------  -------------  ---------  ------------  -------------  -------------------  -----------
            {positionId}  {symbolName:<13} {volume/100}  {tradeSide}    {price:.5f}     {YYYY-MM-DD HH:MM:SS}  {grossProfit / 100.0:.2f}
            ... (más posiciones)
            (Si no hay posiciones: "No open positions found.")
            ```

    *   **`history.py` (RF-008):**
        *   **Mensajes:** `ProtoOAGetDealListReq` (inputs: `ctidTraderAccountId`, `fromTimestamp`, `toTimestamp`), `ProtoOAGetDealListRes` (output: lista de `ProtoOADeal`).
        *   **Argumentos CLI:** (`--weeks <int>` | `--days <int>` | `--from <YYYY-MM-DD>` `--to <YYYY-MM-DD>`).
        *   **Salida Consola (Formato Exacto):** (Tabla formateada)
            ```text
            --- Deal History (Account: {ctidTraderAccountId}) ---
               Deal ID  Position ID    Symbol Name      Volume  Trade Side    Execution Price    Timestamp (UTC)      Close Pos. Detail    Commission
            ----------  -----------  ---------------  --------  ------------  -----------------  -------------------  -------------------  ----------
            {dealId}  {positionId}  {symbolName:<15} {volume/100}  {tradeSide}    {executionPrice:.5f}  {YYYY-MM-DD HH:MM:SS}  {closePositionDetail}  {commission / 100.0:.2f}
            ... (más deals)
            (Si no hay deals: "No deals found in the specified period.")
            ```

    *   **`ticks.py` (RF-006):**
        *   **Mensajes:** `ProtoOAGetTickDataReq` (inputs: `ctidTraderAccountId`, `symbolId`, `type` (`ProtoOAQuoteType`), `fromTimestamp`, `toTimestamp`), `ProtoOAGetTickDataRes` (output: lista de `ProtoOATickData`).
        *   **Argumentos CLI:** `--symbol-id <int>`, `--type <BID|ASK>`, (`--days <int>` | `--from <YYYY-MM-DD>` `--to <YYYY-MM-DD>`).
        *   **Salida Consola (Formato Exacto):** (Tabla formateada, potencialmente larga)
            ```text
            --- Tick Data {type} {symbolName} ({symbolId}) (Account: {ctidTraderAccountId}) ---
            Timestamp (UTC+ms)     Tick
            ---------------------  --------
            {YYYY-MM-DD HH:MM:SS.fff}  {tick:.5f}
            ... (más ticks)
            (Si no hay ticks: "No tick data found.")
            ```

*   **4.3. Módulo `utils` (`src/utils/`):**
    *   `config.py`: Carga y valida config. Debe proveer un objeto o dict fácil de usar.
    *   `logging_setup.py`: Configura `logging`. Formato: `%(asctime)s - %(levelname)s - %(name)s - %(message)s`.
    *   *(Potencialmente `helpers.py` para conversiones de timestamp, formateo de tablas, etc.)*
*   **4.4. Punto de Entrada `main.py` (`src/main.py`):**
    *   Configura `argparse` con subparsers para cada comando.
    *   Maneja el ciclo de vida del `CTraderClient` y el reactor Twisted.
    *   Llama a la función `run_<comando>(client, args)` apropiada.

## 5. Entorno de Ejecución y Despliegue

*(Sin cambios respecto a la versión anterior)*

## 6. Estrategia de Pruebas y Validación

*(Se mantiene la estrategia general, pero se enfatiza la verificación contra los formatos de salida definidos)*

*   **Pruebas Unitarias (`src/tests/unit/`):** Mockear dependencias (cliente API, utils). Probar lógica de comandos aislada (construcción de requests, parsing de args, formateo *potencial* de salida con datos mock).
*   **Pruebas de Integración (`src/tests/integration/`):**
    *   Usar cuenta **Demo**. Configurar credenciales vía entorno de prueba.
    *   **Verificar el formato de salida exacto** para cada comando contra los ejemplos en la sección 4.2 (usar `assertMultiLineEqual` o captura de `stdout`).
    *   Probar casos borde: rangos de fechas inválidos, IDs de símbolos incorrectos, parámetros faltantes.
    *   Verificar manejo de errores API (comparar `errorCode` esperado).
*   **Ejecución de Pruebas:** Usar los comandos `docker exec ... unittest discover ...`.

## 7. Consideraciones Adicionales

*   **Gestión de Símbolos:** Crucial usar `list_symbols` para obtener `symbolId`. El nombre `symbolName` puede usarse para la salida.
*   **Rate Limiting:** No implementado activamente, pero evitar bucles excesivos.
*   **Manejo de Grandes Datos:** Para `candles` y `ticks`, si se solicitan rangos muy grandes, considerar imprimir solo un resumen o las primeras/últimas N entradas, o usar paginación si la API lo soporta para esos requests (revisar documentación Proto).
*   **Timezones:** API usa UTC (timestamps en ms). Convertir a formato legible `YYYY-MM-DD HH:MM:SS` (o `... .fff` para ticks) para la salida.
*   **Precisión Decimal:** Los precios y volúmenes tienen precisión específica. Usar formateo adecuado (ej. `.5f` para precios FX, `.2f` para P/L en moneda).

## 8. Notas para Desarrollo con IA

*   **Prioridades:** Seguir las prioridades P0, P1, P2, P3 definidas en la sección 2.1.
*   **Formatos de Salida:** Implementar los formatos de salida *exactamente* como se describen en la sección 4.2.
*   **Mensajes Proto:** Usar las definiciones de `ctrader_open_api.messages.v2.protobuf` y los ejemplos/campos mencionados en 4.2.
*   **Errores y Logging:** Implementar manejo robusto de `errorCode` y excepciones Twisted. Loggear información útil.
*   **Twisted Deferreds:** Usar `inlineCallbacks` o encadenamiento `.addCallback()/.addErrback()` para manejar la asincronía.
*   **Pandas:** Recomendado usar `pandas.DataFrame` para manejar y formatear los datos tabulares (velas, ticks, símbolos, posiciones, historial) antes de imprimirlos (ej. con `df.to_string()`).
