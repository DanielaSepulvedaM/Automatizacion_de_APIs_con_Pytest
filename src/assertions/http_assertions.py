#helper de funciones de asercion para respuestas HTTP, como verificar el status code o el content type

from collections.abc import Iterable


def assert_status_code(response, expected_status: int | Iterable[int]) -> None:
    if isinstance(expected_status, int):
        assert response.status_code == expected_status
        return

    assert response.status_code in expected_status


def assert_is_json_response(response) -> None:
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type
