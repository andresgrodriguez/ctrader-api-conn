# Diario de Desarrollo: Cliente API cTrader

Este documento es una guía paso a paso para construir el cliente CLI de la API de cTrader, siguiendo las `PROJECT_SPECIFICATIONS.md` y utilizando la estructura de proyecto definida en `README.md`.

**Filosofía:** Desarrollar iterativamente, módulo por módulo (siguiendo las prioridades de `PROJECT_SPECIFICATIONS.md`), con pruebas integradas en cada paso y asegurando que cada fase cumple su "Definición de Terminado" (DoD).

**Referencias Clave:**
*   [Documentación OpenApiPy](https://spotware.github.io/OpenApiPy/)
*   [Definiciones Proto Messages](https://github.com/spotware/openapi-proto-messages)

## Fase 0: Preparación y Verificación del Entorno

*Objetivo: Asegurar que el contenedor `ctrader-api-conn` está operativo y tiene las herramientas y configuraciones necesarias.*
*DoD: Todos los comandos de verificación se ejecutan correctamente, mostrando las versiones/configuraciones esperadas y conectividad exitosa.* 

1.  **Verificar Estado del Contenedor:**
    ```bash
    # Comprobar que el contenedor está en ejecución
    docker ps | grep ctrader-api-conn 
    ```
    *Si no está corriendo, inícialo con `cd /home/arodriguez/docker/hugo.local/ && docker compose up -d ctrader-api-conn`.* 

2.  **Verificar Intérprete Python:**
    ```bash
    docker exec -it ctrader-api-conn python --version
    ```
    *Debe mostrar Python 3.8 o superior.*

3.  **Verificar Dependencias Instaladas:**
    ```bash
    # Listar paquetes y buscar los clave
    docker exec -it ctrader-api-conn python -m pip list | grep -E 'ctrader-open-api|Twisted|protobuf|pyOpenSSL|service_identity|python-dotenv|pandas'
    ```
    *Asegúrate de que las versiones coinciden (o son compatibles) con las especificadas en `requirements.txt` y `PROJECT_SPECIFICATIONS.md`. Si faltan, idealmente deberías reconstruir la imagen Docker actualizando `requirements.txt` y el `Dockerfile`. Como alternativa temporal (menos recomendada), puedes instalarlas directamente:* 
    ```bash
    # Ejemplo de instalación directa (si es estrictamente necesario)
    # docker exec -it ctrader-api-conn python -m pip install -r /app/requirements.txt 
    ```

4.  **Verificar Variables de Entorno:**
    ```bash
    # Verificar las obligatorias
    docker exec -it ctrader-api-conn bash -c 'echo "CLIENT_ID: $CTRADER_CLIENT_ID"'
    docker exec -it ctrader-api-conn bash -c 'echo "CLIENT_SECRET: $CTRADER_CLIENT_SECRET"'
    docker exec -it ctrader-api-conn bash -c 'echo "ACCOUNT_ID: $CTRADER_ACCOUNT_ID"'
    # Verificar opcionales (ejemplo)
    docker exec -it ctrader-api-conn bash -c 'echo "API_HOST: $CTRADER_API_HOST"'
    docker exec -it ctrader-api-conn bash -c 'echo "LOG_LEVEL: $LOG_LEVEL"'
    ```
    *Confirma que las variables obligatorias tienen valor. Estas deberían haberse pasado al crear el contenedor o estar definidas en un archivo `.env` si el punto de entrada del contenedor lo soporta (aunque `docker exec` no usa `.env` directamente).*

5.  **Comprobar Acceso a la API:**
    ```bash
    # Usar netcat para verificar conectividad al host demo (o live si está configurado) y puerto
    docker exec -it ctrader-api-conn nc -zv demo.ctraderapi.com 5035
    docker exec -it ctrader-api-conn nc -zv live.ctraderapi.com 5035
    ```
    *Debería indicar "succeeded". Si falla, revisa la configuración de red del contenedor/host.*

## Fase 1: Módulos Base - Configuración y Logging (Prioridad P0)

*Objetivo: Crear las utilidades para cargar configuración y establecer el logging estándar.*
*DoD: Funciones `load_config` y `setup_logging` implementadas, probadas unitariamente (config) y manualmente (logging), logs generados correctamente en consola y archivo.* 

1.  **Crear `src/utils/config.py`:**
    *   Implementar `load_config()`:
        *   Usar `dotenv.load_dotenv()` y `os.getenv()`.
        *   Leer `CTRADER_CLIENT_ID`, `CTRADER_CLIENT_SECRET`, `CTRADER_ACCOUNT_ID` (obligatorias, lanzar `ValueError` si faltan).
        *   Leer opcionales (`CTRADER_API_HOST`, `CTRADER_API_PORT`, `LOG_LEVEL`, `OUTPUT_DIR`, `ACCESS_TOKEN`) con valores por defecto (ej. `host='demo'`, `port=5035`, `log_level='INFO'`, `output_dir='/app/data/output'`).
        *   Validar tipos (`port` y `account_id` deben ser enteros). Convertir `host` ('live'/'demo') a URL real (`live.ctraderapi.com`, `demo.ctraderapi.com`).
        *   Considerar argumentos CLI (`args` de argparse) para sobrescribir valores de env/defaults.
        *   Retornar un diccionario o un objeto simple (ej. `SimpleNamespace`).
    *   **Test Unitario (`src/tests/unit/test_config.py`):**
        *   Usar `unittest.mock.patch.dict` para simular `os.environ` con diferentes escenarios (todas las vars, solo obligatorias, faltan obligatorias, tipos inválidos).
        *   Verificar que la configuración se carga correctamente, se aplican defaults y se lanzan excepciones.
        *   *Ejemplo Snippet Test:*
            ```python
            import unittest
            from unittest.mock import patch
            from src.utils.config import load_config # Asumiendo esta estructura

            class TestConfig(unittest.TestCase):
                @patch.dict('os.environ', {'CTRADER_CLIENT_ID': 'test_id', 
                                        'CTRADER_CLIENT_SECRET': 'test_secret', 
                                        'CTRADER_ACCOUNT_ID': '12345'})
                def test_load_config_minimal(self):
                    config = load_config()
                    self.assertEqual(config['client_id'], 'test_id')
                    self.assertEqual(config['account_id'], 12345)
                    self.assertEqual(config['host'], 'demo.ctraderapi.com') # Default
                    self.assertEqual(config['port'], 5035) # Default

                @patch.dict('os.environ', {'CTRADER_CLIENT_ID': 'test_id', 
                                        'CTRADER_CLIENT_SECRET': 'test_secret'})
                def test_load_config_missing_account(self):
                    with self.assertRaises(ValueError):
                        load_config()
            # ... más tests
            ```

2.  **Crear `src/utils/logging_setup.py`:**
    *   Implementar `setup_logging(log_level='INFO', log_dir='/app/data/logs')`:
        *   Crear directorio `log_dir` si no existe (`os.makedirs(..., exist_ok=True)`).
        *   Configurar `logging.basicConfig` o obtener logger raíz.
        *   Crear `StreamHandler` (consola) y `RotatingFileHandler` (archivo: `{log_dir}/ctrader_client.log`, ej. max 5MB, 3 backups).
        *   Crear `Formatter` (`'%(asctime)s - %(levelname)s - %(name)s - %(message)s'`).
        *   Asignar formatter a handlers.
        *   Añadir handlers al logger raíz.
        *   Establecer nivel del logger raíz (`log_level.upper()`).
    *   **Test (Manual/Inspección):**
        *   Llamar a `setup_logging('DEBUG')` en un script temporal.
        *   Verificar logs en consola y en `/app/data/logs/ctrader_client.log`. Comprobar formato y niveles.

## Fase 2: Core del Cliente API (`src/client/`) (Prioridad P0)

*Objetivo: Implementar la conexión básica, autenticación y envío/recepción de mensajes Proto.*
*DoD: Clase `CTraderClient` implementada con métodos `connect`, `disconnect`, `send_message`. Test de integración `test_core_client.py` pasa, demostrando conexión, autenticación (app y cuenta) y envío/recepción de un mensaje simple (`ProtoOAGetVersionReq`) con la API Demo.* 

1.  **Crear `src/client/auth.py`:**
    *   Importar mensajes Proto: `ProtoOAApplicationAuthReq`, `ProtoOAAccountAuthReq`.
    *   Función `authenticate(client, config)`:
        *   Construir `ProtoOAApplicationAuthReq(clientId=config['client_id'], clientSecret=config['client_secret'])`.
        *   Llamar `return client.send_message(request)`.
    *   Función `authorize_account(client, config, access_token)`:
        *   Construir `ProtoOAAccountAuthReq(accessToken=access_token, ctidTraderAccountId=config['account_id'])`.
        *   Llamar `return client.send_message(request)`.
    *   **Test Unitario (`src/tests/unit/test_auth.py`):**
        *   Mockear `client.send_message`. Verificar que se llama con los mensajes Proto correctos y los datos de `config`.

2.  **Crear `src/client/core.py`:**
    *   Importar `Client` de `ctrader_open_api.client`, `TcpProtocol` de `twisted.internet.protocol`, `endpoint` de `twisted.internet`, mensajes Proto relevantes (`ProtoOAApplicationAuthRes`, `ProtoOAAccountAuthRes`, `ProtoErrorRes`), `Deferred` de `twisted.internet.defer`, `logging`, `auth` de `.auth`.
    *   Clase `CTraderClient`:
        *   `__init__(self, config, reactor)`: Guardar `config`, `reactor`. Inicializar `_client = None`, `_is_connected = False`, `_is_authenticated = False`, `_pending_requests = {}`, `_connect_deferred = None`.
        *   `connect(self)`:
            *   Si ya conectado/conectando, retornar `_connect_deferred`.
            *   `self._connect_deferred = Deferred()`
            *   Obtener `host`, `port` de `config`.
            *   Crear `endpoint = endpoints.TCP4ClientEndpoint(self.reactor, host, port)` (o SSL si se requiere/configura)
            *   `self._client = Client(endpoint, TcpProtocol, self.reactor)`
            *   `self._client.setConnectedCallback(self._on_connect)`
            *   `self._client.setDisconnectedCallback(self._on_disconnect)`
            *   `self._client.setMessageReceivedCallback(self._on_message)`
            *   `self._client.startService()`
            *   `return self._connect_deferred`
        *   `disconnect(self)`: Si `_client`, llamar `_client.stopService()`. Resetear flags.
        *   `_on_connect(self, client)`:
            *   `self._is_connected = True`. Log `INFO: Connected to {host}:{port}`.
            *   `d = auth.authenticate(self, self.config)`
            *   `d.addCallbacks(self._handle_auth_response, self._handle_auth_error)`
        *   `_handle_auth_response(self, response)`:
            *   Si `response.payloadType == ProtoOAApplicationAuthRes`: # Chequear tipo exacto
                *   `access_token = response.payload.accessToken`
                *   Log `INFO: Application authenticated. Authorizing account...`
                *   `d = auth.authorize_account(self, self.config, access_token)`
                *   `d.addCallbacks(self._handle_account_auth_response, self._handle_auth_error)`
            *   Else: Log `ERROR: Unexpected auth response type`. Disparar `self._connect_deferred.errback(...)`.
        *   `_handle_account_auth_response(self, response)`:
            *   Si `response.payloadType == ProtoOAAccountAuthRes`: # Chequear tipo exacto
                *   `self._is_authenticated = True`
                *   Log `INFO: Account {account_id} authorized successfully.`
                *   Disparar `self._connect_deferred.callback(self)` # Éxito
            *   Else if `response.payloadType == ProtoErrorRes`:
                *   Log `ERROR: Account authorization failed: {response.payload.errorCode} - {response.payload.description}`.
                *   Disparar `self._connect_deferred.errback(...)`
            *   Else: Log `ERROR: Unexpected account auth response`. Disparar `self._connect_deferred.errback(...)`.
        *   `_handle_auth_error(self, failure)`:
            *   Log `ERROR: Authentication failed: {failure.getTraceback()}`.
            *   Disparar `self._connect_deferred.errback(failure)`.
            *   Llamar `self.disconnect()`.
        *   `_on_disconnect(self, client, reason)`:
            *   `self._is_connected = False`, `self._is_authenticated = False`. Log `INFO: Disconnected. Reason: {reason}`.
            *   Limpiar `_pending_requests`, disparando `errback` en los `Deferreds` pendientes con error de desconexión.
            *   Si `_connect_deferred` y no disparado, disparar `errback`.
        *   `_on_message(self, client, message)`:
            *   Log `DEBUG: Received message: {message.payloadType}`.
            *   `client_msg_id = getattr(message, 'clientMsgId', None)`
            *   If `client_msg_id` and `client_msg_id in self._pending_requests`:
                *   `deferred = self._pending_requests.pop(client_msg_id)`
                *   If `message.payloadType == ProtoErrorRes`:
                    *   Log `WARNING: Received error response for msg {client_msg_id}: {message.payload.errorCode}`
                    *   Disparar `deferred.errback(message)` # Pasar el mensaje de error
                *   Else:
                    *   Disparar `deferred.callback(message)`
            *   Else: # Mensajes no solicitados (eventos, etc.)
                *   Log `DEBUG: Unhandled message type: {message.payloadType}` (ignorar por ahora).
        *   `send_message(self, message, expects_response=True)`:
            *   If not `self._is_authenticated`: Raise `Exception("Client not authenticated")`
            *   `client_msg_id = getattr(message, 'clientMsgId', None)`
            *   If not `client_msg_id`: # Asignar uno si no existe
                *   `client_msg_id = str(uuid.uuid4())`
                *   `message.clientMsgId = client_msg_id`
            *   `deferred = Deferred()`
            *   If `expects_response`:
                *   `self._pending_requests[client_msg_id] = deferred`
            *   Log `DEBUG: Sending message: {message.payloadType} (ID: {client_msg_id})`
            *   `self._client.send(message)`
            *   If not `expects_response`:
                *   `deferred.callback(None)` # Disparar inmediatamente si no se espera respuesta
            *   Return `deferred`
    *   **Test de Integración (`src/tests/integration/test_core_client.py`):**
        *   **Requiere Credenciales Demo VÁLIDAS en el entorno.**
        *   Usar `twisted.trial.unittest.TestCase` y `inlineCallbacks`.
        *   Test `test_connect_authenticate_disconnect`: Crear cliente, llamar `yield client.connect()`, verificar `client._is_authenticated is True`. Llamar `yield client.disconnect()`, verificar flags a `False`.
        *   Test `test_send_receive_version`: Conectar, autenticar. Construir `ProtoOAGetVersionReq()`. Llamar `response = yield client.send_message(request)`. Verificar `response.payloadType == ProtoOAGetVersionRes`. Verificar `response.payload.version`.
        *   Testear errores (ej. credenciales inválidas): esperar que `client.connect()` lance un `errback` y verificar el tipo de error/log.
        *   *Ejemplo Snippet Respuesta API (Mock o Real):*
            ```protobuf
            # ProtoOAApplicationAuthRes
            payloadType: PROTO_OA_APPLICATION_AUTH_RES
            payload {
              accessToken: "VALID_ACCESS_TOKEN"
              tokenType: BEARER
              expiresIn: 3600 # O el valor que sea
            }
            # ProtoOAAccountAuthRes
            payloadType: PROTO_OA_ACCOUNT_AUTH_RES
            payload {
              ctidTraderAccountId: 1234567
            }
            # ProtoErrorRes (Ejemplo: Cuenta inválida)
            payloadType: PROTO_ERROR_RES
            payload {
              errorCode: "ACCOUNT_NOT_FOUND"
              description: "The specified account was not found."
            }
            clientMsgId: "uuid-del-request-original"
            ```

## Fase 3: Implementación de Comandos CLI (Prioridad P1, P2, P3)

*Objetivo: Crear la interfaz de línea de comandos y la lógica para cada comando específico, siguiendo las prioridades.*
*DoD (por comando): Comando implementado en `src/commands/`, integrado en `main.py` con `argparse`, test de integración pasa verificando la solicitud/respuesta y el formato de salida exacto definido en `PROJECT_SPECIFICATIONS.md`.* 

1.  **Crear `src/main.py`:**
    *   Importar `argparse`, `sys`, `logging`, `reactor` de Twisted, `load_config`, `setup_logging`, `CTraderClient`.
    *   Importar funciones `run_<comando>` de `src/commands/`.
    *   Función `main()`:
        *   `parser = argparse.ArgumentParser(...)`
        *   Añadir args globales: `--host`, `--log-level`, etc.
        *   `subparsers = parser.add_subparsers(dest='command', required=True)`
        *   Para cada comando (ej. `account_info`):
            *   `parser_account = subparsers.add_parser('account_info', help='...')`
            *   Añadir args específicos si los hay.
            *   `parser_account.set_defaults(func=run_account_info)` # Asociar función
        *   `args = parser.parse_args()`
        *   `config = load_config(args)` # Pasar args para overrides
        *   `setup_logging(config['log_level'], config['log_dir'])`
        *   `client = CTraderClient(config, reactor)`
        *   `d = client.connect()`
        *   `d.addCallback(lambda _, args: args.func(client, args), args)` # Llamar a la func del comando
        *   `d.addErrback(handle_connection_error)` # Loggear error y parar reactor
        *   `d.addBoth(lambda _: client.disconnect())` # Desconectar siempre
        *   `d.addBoth(lambda _: stop_reactor())` # Parar reactor siempre
        *   `reactor.run()`
    *   Funciones `handle_connection_error`, `stop_reactor`.
    *   Bloque `if __name__ == "__main__": main()`. 

2.  **Implementar Comando `account_info` (`src/commands/account_info.py`) (P1):**
    *   Importar `ProtoOATraderReq`, `ProtoOATraderRes`, `logging`, `inlineCallbacks`.
    *   `@inlineCallbacks`
    *   `def run_account_info(client, args):`
        *   Log `INFO: Requesting account info...`
        *   `request = ProtoOATraderReq(ctidTraderAccountId=client.config['account_id'])`
        *   Try:
            *   `response = yield client.send_message(request)`
            *   If `response.payloadType == ProtoOATraderRes`:
                *   `trader = response.payload.trader`
                *   Formatear e imprimir la salida como en `PROJECT_SPECIFICATIONS.md`.
                *   Log `INFO: Account info retrieved successfully.`
            *   Else: # Ya manejado por errback genérico de send_message, pero doble check
                *   Log `ERROR: Unexpected response type: {response.payloadType}`
        *   Except Exception as e: # Captura errback de send_message o errores de conexión
            *   Log `ERROR: Failed to get account info: {e}` (el error ya puede ser el `ProtoErrorRes`)
    *   **Test de Integración (`src/tests/integration/test_account_info_cmd.py`):**
        *   Simular `main.py account_info` (quizás llamando a `main()` con `sys.argv` mockeado o llamando directamente a `run_account_info` después de conectar).
        *   Capturar `stdout` y comparar con el formato exacto esperado.

3.  **Implementar Comando `list_symbols` (`src/commands/list_symbols.py`) (P1):**
    *   Similar a `account_info`, usar `ProtoOASymbolsListReq` -> `ProtoOASymbolsListRes`. 
    *   Iterar sobre `response.payload.symbol` y `response.payload.archivedSymbol`. 
    *   Necesitarás mapear `symbolCategoryId` a nombres usando `response.payload.symbolCategory`.
    *   Formatear la tabla de salida. Usar `pandas` o `tabulate` es buena idea.
    *   **Test de Integración:** Verificar tabla de salida.

4.  **Implementar Comando `candles` (`src/commands/candles.py`) (P1):**
    *   Importar `ProtoOAGetTrendbarsReq`, `ProtoOATrendbarsRes`, `ProtoOATrendbarPeriod`, `datetime`, `timedelta`.
    *   Parsear args (`symbol_id`, `period`, rango temporal).
    *   Convertir `period` string a enum `ProtoOATrendbarPeriod[args.period.upper()]`. Manejar `KeyError`.
    *   Calcular `fromTimestamp`, `toTimestamp` (en ms UTC) desde `args.weeks/days/from/to`. Usar `datetime.utcnow()`, `timedelta`.
    *   Construir `ProtoOAGetTrendbarsReq`.
    *   Enviar mensaje. En callback:
        *   Procesar `ProtoOAGetTrendbarsRes`. Iterar `response.payload.trendbar`.
        *   Para cada `trendbar`: calcular OHLC (cuidado con `delta` y `pipValue`, puede requerir info del símbolo obtenida previamente o en `ProtoOASymbolsListRes`). Convertir `timestamp` (ms) a `datetime`. 
        *   Formatear tabla. `pandas` muy recomendado aquí.
    *   **Manejo de Excepciones:** `KeyError` en periodo, errores API (`INVALID_SYMBOL`, `NO_HISTORY_DATA`), errores de conexión.
    *   **Test de Integración:** Probar diferentes periodos, rangos, símbolo válido/inválido. Verificar formato tabla y datos OHLC calculados.

5.  **Implementar Comandos Restantes (positions, history, ticks) (P2, P3):**
    *   Seguir patrón similar: Parsear args -> Construir Request -> Enviar -> Procesar Response en callback -> Formatear salida -> Manejar errores.
    *   Prestar atención a los tipos de datos (volumen en centavos, timestamps, enums). 
    *   Añadir tests de integración para cada uno.

## Fase 4: Pruebas Finales y Refinamiento

*Objetivo: Asegurar la robustez y calidad general de la aplicación.*
*DoD: Todos los tests (unitarios y de integración) pasan. Todos los comandos funcionan según especificaciones con diversas entradas válidas/inválidas. Logs son claros y útiles. Documentación actualizada.* 

1.  **Ejecutar Todos los Tests:**
    ```bash
    docker exec -it ctrader-api-conn python -m unittest discover /app/src/tests
    ```
    *Corregir cualquier fallo.* 

2.  **Pruebas Manuales Exhaustivas (CLI):**
    *   Ejecutar cada comando con combinaciones válidas e inválidas (ver `README.md`).
    *   Verificar salida y logs. Probar `--log-level DEBUG`.
    *   Probar errores de conexión (si es posible, ej. deteniendo el contenedor temporalmente).
    *   Probar con `--host live` (**con extrema precaución** y solo si es necesario).

3.  **Revisión de Código:**
    *   PEP 8, docstrings, claridad, manejo de excepciones robusto.

4.  **Refinamiento:**
    *   Mejorar mensajes de error al usuario.
    *   Optimizar si es necesario (poco probable).
    *   Asegurar detención limpia del reactor Twisted en todos los casos.

5.  **Actualizar Documentación:**
    *   `README.md` y `PROJECT_SPECIFICATIONS.md` deben reflejar el estado final.

*Una vez completadas estas fases, deberías tener un cliente CLI funcional, bien probado y documentado.* 
