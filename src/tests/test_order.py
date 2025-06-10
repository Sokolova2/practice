import pytest
import pytest_asyncio 
from src.tests.conftest import client,  cashier_token, accountant_token
from src.main import app

@pytest_asyncio.fixture(scope="function")
async def created_order(client, cashier_token):
    response = await client.post(
        "/cashier/create/order",
        json={"id_product": 1},
        headers={'Authorization': f'Bearer {cashier_token}'}
    )
    assert response.status_code == 200
    yield
    
@pytest.mark.asyncio
async def test_change_status(client, cashier_token):
    response = await client.patch(
        "/cashier/order/status/1",
        json={"status": "Сплачено"},
        headers={'Authorization': f'Bearer {cashier_token}'}
    )
    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_get_last_order_unauthorized(client):
    response = await client.get(
        "/cashier/order",
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_generation_check_unauthorized(client):
    response = await client.get(
        "/cashier/check/1"
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_change_status_unauthorized(client):
    response = await client.patch(
        "/cashier/order/status/1",
        json={"status": "Сплачено"}
    )
    assert response.status_code == 403
    
    
@pytest.mark.asyncio
async def test_get_last_order_unauthenticated(client, accountant_token):
    response = await client.get(
        "/cashier/order",
        headers={'Authorization': f'Bearer {accountant_token}'}
    )

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_generation_check_unauthenticated(client, accountant_token):
    response = await client.get(
        "/cashier/check/1",
        headers={'Authorization': f'Bearer {accountant_token}'}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_change_status_unauthenticated(client, accountant_token):
    response = await client.patch(
        "/cashier/order/status/1",
        json={"status": "Сплачено"},
        headers={'Authorization': f'Bearer {accountant_token}'}
    )
    assert response.status_code == 403

