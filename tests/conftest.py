#fixture (molde o estructura fija) para el cliente API, que luego usaremos en los tests
import pytest
from src.clients.api_client import ApiClient


@pytest.fixture(scope="session")
def client():
    # Por ahora es placeholder.
    # Luego lo apuntamos a tu API real o a un mock server.
    return ApiClient(base_url="http://localhost:8000", timeout_seconds=0.5)


@pytest.fixture(autouse=True)
def skip_integration_if_api_unavailable(request):
    if request.node.get_closest_marker("integration") is None:
        return

    api_client = request.getfixturevalue("client")
    try:
        response = api_client.get("/health")
    except Exception as exc:
        pytest.skip(f"API no disponible para integration: GET /health fallo ({exc})")

    if response.status_code != 200:
        pytest.skip(
            f"API no disponible para integration: GET /health devolvio {response.status_code}"
        )
