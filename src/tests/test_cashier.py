import pytest 
import pytest_asyncio
from src.main import app
from httpx import AsyncClient, ASGITransport
import os
from dotenv import load_dotenv
from datetime import datetime
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ACCESS_COOKIE_NAME = os.getenv("JWT_ACCESS_COOKIE_NAME")

def cashier_token():
    now = datetime.utcnow()
    payload = {
        "sub": "1",
        "login": "cashier",
        "role": "Касир",
        "iat": int(now.timestamp()),
        "type": "access"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def accountant_token():
    now = datetime.utcnow()
    payload = {
        "sub": "1",
        "login": "accountant",
        "role": "Бухгалтер",
        "iat": int(now.timestamp()),
        "type": "access"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

token_cashier = cashier_token()

token_accountant = accountant_token()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    )as ac: 
        yield ac
        
@pytest.mark.asyncio
async def test_get_product(client):
    response = await client.get(
        "cashier/product",
        headers={'Authorization': f'Bearer {token_cashier}'}
    )
    data = response.json()
    
    if response.status_code == 200:
        assert isinstance(data, list)
    elif response.status_code == 404:
        assert data == {"detail": "Not found"}
    else: 
        pytest.fail(f"Unexpected status code: {response.status_code}")
        
@pytest.mark.asyncio
async def test_create_order(client):
    response = await client.post(
        "cashier/create/order",
        json={"id_product": "1"},
        headers={'Authorization': f'Bearer {token_cashier}'}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_last_order(client):
    response = await client.get(
        "cashier/order",
        headers={'Authorization': f'Bearer {token_cashier}'}
    )
    assert response.status_code == 200
       
@pytest.mark.asyncio
async def test_generation_check(client):
    response = await client.get(
        "cashier/check/1",
        headers={'Authorization': f'Bearer {token_cashier}'}
    )
    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_change_status(client):
    response = await client.patch(
        "cashier/order/status/1",
        json={"status": "Сплачено"},
        headers={'Authorization': f'Bearer {token_cashier}'}
    )
    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_get_product_unauthorized(client):
    response = await client.get(
        "cashier/product"
    )
    assert response.status_code == 403
    
@pytest.mark.asyncio
async def test_create_order_unauthorized(client):
    response = await client.post(
        "cashier/create/order",
        json={"id_product": "1"}
    )
    assert response.status_code == 403
    
@pytest.mark.asyncio
async def test_get_last_order_unauthorized(client):
    response = await client.get(
        "cashier/order",
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_generation_check_unauthorized(client):
    response = await client.get(
        "cashier/check/1"
    )
    assert response.status_code == 403
      
@pytest.mark.asyncio
async def test_change_status_unauthorized(client):
    response = await client.patch(
        "cashier/order/status/1",
        json={"status": "Сплачено"}
    )
    assert response.status_code == 403
    
    
@pytest.mark.asyncio
async def test_create_order_unauthenticated(client):
    response = await client.post(
        "cashier/create/order",
        json={"id_product": "1"},
        headers={'Authorization': f'Bearer {token_accountant}'}
    )
    
    assert response.status_code == 403
    
@pytest.mark.asyncio
async def test_get_product_unauthenticated(client):
    response = await client.get(
        "cashier/product",
        headers={'Authorization': f'Bearer {token_accountant}'}
    )
    
    assert response.status_code == 403
    
@pytest.mark.asyncio
async def test_get_last_order_unauthenticated(client):
    response = await client.get(
        "cashier/order",
        headers={'Authorization': f'Bearer {token_accountant}'}
    )
    
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_generation_check_unauthenticated(client):
    response = await client.get(
        "cashier/check/1",
        headers={'Authorization': f'Bearer {token_accountant}'}
    )
    assert response.status_code == 403
    
@pytest.mark.asyncio
async def test_change_status_unauthenticated(client):
    response = await client.patch(
        "cashier/order/status/1",
        json={"status": "Сплачено"},
        headers={'Authorization': f'Bearer {token_accountant}'}
    )
    assert response.status_code == 403


