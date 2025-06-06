# import pytest
# import os
# from dotenv import load_dotenv
# from datetime import datetime
# import jwt
# import pytest_asyncio
# from httpx import AsyncClient, ASGITransport
# from src.main import app

# load_dotenv()

# JWT_SECRET = os.getenv("JWT_SECRET")
# JWT_ACCESS_COOKIE_NAME = os.getenv("JWT_ACCESS_COOKIE_NAME")

# def accountant_token():
#     now = datetime.utcnow()
#     payload = {
#         "sub": "1",
#         "login": "accountant",
#         "role": "Бухгалтер",  
#         "iat": int(now.timestamp()),
#         "type": "access"
#     }
#     return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# def cashier_token():
#     now = datetime.utcnow()
#     payload = {
#         "sub": "1",
#         "login": "accountant",
#         "role": "Касир",  
#         "iat": int(now.timestamp()),
#         "type": "access"
#     }
#     return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# token_accountant = accountant_token()

# token_cashier = cashier_token()

# @pytest_asyncio.fixture
# async def client():
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test"
#     ) as ac:
#         yield ac


# @pytest.mark.asyncio
# async def test_get_orders_validate(client):
#     response = await client.get(
#         "/accountant/orders", 
#         params={'start_data': '2025-05-04', 'end_data': '2025-06-30'},
#         headers={'Authorization': f'Bearer {token_accountant}'}
#         )
#     assert response.status_code == 200
    
# @pytest.mark.asyncio
# async def test_get_orders_invalid(client):
#     response = await client.get(
#         "/accountant/orders", 
#         params={'start_data': '2025.05.04', 'end_data': '2025.06.30'},
#         headers={'Authorization': f'Bearer {token_accountant}'}
#         )
#     assert response.status_code == 422
    
# @pytest.mark.asyncio
# async def test_get_order_unauthorized(client):
#     response = await client.get(
#         "/accountant/orders",
#         params={'start_data': '2025-05-04', 'end_data': '2025-06-04'}
#     )
#     assert response.status_code == 403

# @pytest.mark.asyncio
# async def test_get_order_unathenticated(client):
#     response = await client.get(
#         "/accountant/orders", 
#         params={'start_data': '2025.05.04', 'end_data': '2025.06.30'},
#         headers={'Authorization': f'Bearer {token_accountant}'}
#         )
#     assert response.status_code == 422

