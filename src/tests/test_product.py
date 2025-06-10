import pytest
import pytest_asyncio 
from src.tests.conftest import client,  cashier_token, accountant_token
from src.main import app
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_get_product(client, cashier_token):
    response = await client.get(
        "/cashier/product",
        headers={'Authorization': f'Bearer {cashier_token}'}
    )
    data = response.json()

    if response.status_code == 200:
        assert isinstance(data, list)
    elif response.status_code == 404:
        assert data == {"detail": "Not found"}
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")










