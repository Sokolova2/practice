import pytest
from src.main import app
from src.tests.conftest import client, accountant_token, cashier_token

@pytest.mark.asyncio
async def test_get_orders_validate(client, accountant_token):
    response = await client.get(
        "/accountant/orders", 
        params={'start_data': '2025-05-04', 'end_data': '2025-06-30'},
        headers={'Authorization': f'Bearer {accountant_token}'}
        )
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    
@pytest.mark.asyncio
async def test_get_orders_invalid(client, accountant_token):
    response = await client.get(
        "/accountant/orders", 
        params={'start_data': '2025.05.04', 'end_data': '2025.06.30'},
        headers={'Authorization': f'Bearer {accountant_token}'}
        )
    assert response.status_code == 422
    data = response.json()
    assert data is not None
    
@pytest.mark.asyncio
async def test_get_order_unauthorized(client):
    response = await client.get(
        "/accountant/orders",
        params={'start_data': '2025-05-04', 'end_data': '2025-06-04'}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_order_unathenticated(client, cashier_token):
    response = await client.get(
        "/accountant/orders", 
        params={'start_data': '2025.05.04', 'end_data': '2025.06.30'},
        headers={'Authorization': f'Bearer {cashier_token}'}
        )
    assert response.status_code == 403

