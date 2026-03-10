<<<<<<< HEAD
# Automatizacion_de_APIs_con_Pytest
Automatizacion_de_APIs_con_Pytest es un proyecto real de QA Automation para probar APIs de órdenes con Pytest. Incluye tests positivos y negativos validación de respuestas con Pydantic, parametrización de casos, estructura modular (cliente HTTP + assertions), suites contract/integration y anti-flaky: healthcheck, timeouts por env y retries en GET
=======
# API Test Project

Proyecto base para automatizar pruebas de APIs con `pytest`, `requests`, `pydantic` y una API local en `FastAPI`.

## Comandos Rapidos

Terminal 1 (levantar API):

```powershell
cd "c:\AUTOMATIZACION\SEMANA 4 - Automatizacion de Apis\api-test"
.\.venv\Scripts\Activate.ps1
python -m uvicorn local_api.app:app --reload --port 8000
```

Terminal 2 (ejecutar tests):

```powershell
cd "c:\AUTOMATIZACION\SEMANA 4 - Automatizacion de Apis\api-test"
.\.venv\Scripts\Activate.ps1
python -m pytest -q
python -m pytest -q -m "integration"
python -m pytest -q -m "contract"
```

## Requisitos

- Python 3.10+
- PowerShell (Windows)

## Setup del entorno (venv)

Desde la carpeta `api-test`:

```powershell
cd "c:\AUTOMATIZACION\SEMANA 4 - Automatizacion de Apis\api-test"
```

Si aun no existe `.venv`:

```powershell
python -m venv .venv
```

Activar entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Validar que quedo activo el Python correcto:

```powershell
python -c "import sys; print(sys.executable)"
python -m pytest --version
```

## Levantar API local

En una terminal (terminal 1), desde `api-test`:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn local_api.app:app --reload --port 8000
```

Base URL esperada por los tests: `http://localhost:8000`

## Ejecutar tests

En otra terminal (terminal 2), desde `api-test`:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

Ejecutar solo tests de ordenes:

```powershell
python -m pytest -q tests/orders
```

Ejecutar por marcadores:

```powershell
python -m pytest -q -m "integration"
python -m pytest -q -m "contract"
```

## Nota sobre contract vs integration

En `pytest.ini` estan definidos ambos marcadores:

- `integration`: tests que llaman a la API.
- `contract`: tests de validacion/contrato.

Importante: en el estado actual del proyecto, los tests marcados como `contract` tambien usan el `client` de `tests/conftest.py`, por lo que igualmente requieren el servidor levantado en `localhost:8000`.

## Estructura del proyecto

```text
api-test/
  local_api/
    app.py
  src/
    clients/
      api_client.py
    models/
      orders.py
      errors.py
  tests/
    conftest.py
    orders/
      test_create_order.py
  pytest.ini
  requirements.txt
```

## Errores comunes

### `ConnectionError` a `localhost:8000`

Causa: la API local no esta levantada.

Solucion:

1. Levanta servidor: `python -m uvicorn local_api.app:app --reload --port 8000`
2. Verifica `http://localhost:8000/docs`
3. Reintenta: `python -m pytest -q`

### `pytest` no reconocido en terminal

Usa siempre:

```powershell
python -m pytest -q
```

Asi evitas problemas de `PATH` entre Python global y `.venv`.
>>>>>>> 5100690 (Initial commit)
