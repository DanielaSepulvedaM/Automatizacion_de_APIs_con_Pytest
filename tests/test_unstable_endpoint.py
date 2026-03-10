import pytest

from src.assertions.http_assertions import assert_status_code


@pytest.mark.integration
def test_unstable_endpoint_succeeds_with_retries(client):
    response = client.get("/unstable")
    assert_status_code(response, 200)
