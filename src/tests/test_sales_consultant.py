import pytest
from src.main import app
from src.tests.conftest import client, sales_consultant_token, cashier_token

@pytest.mark.asyncio
async def test_change_status(client, sales_consultant_token):
    response = await client.patch(
        "/consultant/order/1",
        json={"status": "Виконано"},
        headers={'Authorization': f'Bearer {sales_consultant_token}'}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_order_unauthorized(client):
    response = await client.get("/consultant/order")
    assert response.status_code == 403
    
@pytest.mark.asyncio
async def test_change_status_unauthorized(client):
    response = await client.patch(
        "/consultant/order/1",
        json={"status": "Виконано"}
        )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_unathenticated(client, cashier_token):
    response = await client.get(
        "/consultant/order",
        headers={'Authorization': f'Bearer {cashier_token}'}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_change_status_unathenticated(client, cashier_token):
    response = await client.patch(
        "/consultant/order/1",
        headers={'Authorization': f'Bearer {cashier_token}'},
        json={"status": "Виконано"}
    )
    assert response.status_code == 403