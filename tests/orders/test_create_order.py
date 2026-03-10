# tests para la creacion de ordenes
import pytest
from pydantic import ValidationError
from src.assertions.http_assertions import assert_is_json_response, assert_status_code
from src.models.orders import CreateOrderResponse
from src.models.errors import ErrorResponse


INVALID_ORDER_CASES = [
    ({"customer_id": "CUST-2001", "items": [], "currency": "COP"}, "items"),
    ({"customer_id": "CUST-3001", "items": [{"sku": "SKU-1", "qty": 0, "price": 50}], "currency": "COP"}, "items[0].qty"),
    ({"customer_id": "CUST-4001", "items": [{"sku": "SKU-1", "qty": 1, "price": -10}], "currency": "COP"}, "items[0].price"),
]

# Assert 1 que la creacion de orden con payload valido retorna 201 y estructura correcta
@pytest.mark.integration
def test_create_order_returns_201_when_payload_is_valid(client):
    payload = {
        "customer_id": "CUST-1001",
        "items": [{"sku": "SKU-1", "qty": 1, "price": 50}],
        "currency": "COP",
    }
    # TEST DE INTEGRACION
    response = client.post("/orders", json=payload)

    assert_status_code(response, 201)
    assert_is_json_response(response)

    data = response.json()
    parsed = CreateOrderResponse.model_validate(data)

    assert parsed.id
    assert parsed.status in ("CREATED", "PENDING")


# Assert 2 que la creacion de orden con multiples items calcula el total correctamente
@pytest.mark.integration
def test_create_order_returns_calculates_total_correctly_for_multiple_items(client):
    payload = {
        "customer_id": "CUST-4001",
        "items": [
            {"sku": "SKU-1", "qty": 2, "price": 50},
            {"sku": "SKU-2", "qty": 1, "price": 30},
        ],
        "currency": "COP",
    }
    # TEST DE INTEGRACION
    response = client.post("/orders", json=payload)

    assert_status_code(response, 201)
    assert_is_json_response(response)

    data = response.json()
    parsed = CreateOrderResponse.model_validate(data)

    expected_total = 2 * 50 + 1 * 30
    assert parsed.total == expected_total


# Assert 3 - casos invalidos de creacion de orden retornan error de validacion
@pytest.mark.integration
@pytest.mark.parametrize("payload, expected_field", INVALID_ORDER_CASES)
def test_create_order_returns_validation_error_for_invalid_payloads(client, payload, expected_field):
    response = client.post("/orders", json=payload)

    assert_status_code(response, (400, 422))
    assert_is_json_response(response)

    data = response.json()
    if "code" in data and "details" in data:
        err = ErrorResponse.model_validate(data)
        assert err.code == "VALIDATION_ERROR"
        fields = [d.field for d in err.details]
    else:
        assert "detail" in data
        fields = []
        for detail in data["detail"]:
            loc = detail.get("loc", [])
            if not loc:
                continue

            if len(loc) >= 4 and loc[0] == "body" and isinstance(loc[2], int):
                fields.append(f"{loc[1]}[{loc[2]}].{loc[3]}")
            elif len(loc) >= 2 and loc[0] == "body":
                fields.append(str(loc[1]))

    assert expected_field in fields


# Assert 4 - integracion: la respuesta real de crear orden cumple contrato CreateOrderResponse
@pytest.mark.integration
def test_create_order_response_matches_create_order_response_model(client):
    payload = {
        "customer_id": "CUST-5001",
        "items": [{"sku": "SKU-1", "qty": 1, "price": 50}],
        "currency": "COP",
    }
    # TEST DE INTEGRACION
    response = client.post("/orders", json=payload)

    assert_status_code(response, 201)
    assert_is_json_response(response)

    data = response.json()
    parsed = CreateOrderResponse.model_validate(data)

    assert parsed.id
    assert parsed.currency == payload["currency"]


# Assert 5 - contrato: created_at en formato no valido falla la validacion del modelo
@pytest.mark.contract
def test_create_order_response_model_validation_fails_for_invalid_created_at():
    data = {
        "id": "ORD-5001",
        "status": "CREATED",
        "total": 50,
        "currency": "COP",
        "created_at": "invalid-date-format",
    }
    with pytest.raises(ValidationError):
        CreateOrderResponse.model_validate(data)
