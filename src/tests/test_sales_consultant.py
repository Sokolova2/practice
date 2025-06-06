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


# def sales_consultant_token():
#     now = datetime.utcnow()
#     payload = {
#         "sub": "1",
#         "login": "sales_consultant",
#         "role": "Продавець-консультант",
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


# token_sales_consultant = sales_consultant_token()

# token_cashier = cashier_token()


# @pytest_asyncio.fixture
# async def client():
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test"
#     ) as ac:
#         yield ac


# @pytest.mark.asyncio
# async def test_get_last_order(client):
#     response = await client.get(
#         "/consultant/order",
#         headers={'Authorization': f'Bearer {token_sales_consultant}'}
#     )

#     data = response.json()

#     if response.status_code == 200:
#         assert isinstance(data, dict)
#     elif response.status_code == 404:
#         assert data == {"detail": "Not found"}
#     else:
#         pytest.fail(f"Unexpected status code: {response.status_code}")

# @pytest.mark.asyncio
# async def test_change_status(client):
#     response = await client.patch(
#         "/consultant/order/1",
#         json={"status": "Виконано"},
#         headers={'Authorization': f'Bearer {token_sales_consultant}'}
#     )
#     assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_get_order_unauthorized(client):
#     response = await client.get("/consultant/order")
#     assert response.status_code == 403
    
# @pytest.mark.asyncio
# async def test_change_status_unauthorized(client):
#     response = await client.patch(
#         "/consultant/order/1",
#         json={"status": "Виконано"}
#         )
#     assert response.status_code == 403

# @pytest.mark.asyncio
# async def test_unathenticated(client):
#     response = await client.get(
#         "/consultant/order",
#         headers={'Authorization': f'Bearer {token_cashier}'}
#     )
#     assert response.status_code == 403

# @pytest.mark.asyncio
# async def test_change_status_unathenticated(client):
#     response = await client.patch(
#         "/consultant/order/1",
#         headers={'Authorization': f'Bearer {token_cashier}'},
#         json={"status": "Виконано"}
#     )
#     assert response.status_code == 403