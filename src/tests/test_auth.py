# import pytest
# import pytest_asyncio
# from httpx import AsyncClient, ASGITransport
# from src.main import app
# from src.tests.client import client

# # @pytest_asyncio.fixture
# # async def client():
# #     async with AsyncClient(
# #         transport=ASGITransport(app=app),
# #         base_url="http://test",
# #     ) as ac:
# #         yield ac


# @pytest.mark.asyncio
# async def test_get_user(client):
#     response = await client.get("/auth/staff")
#     data = response.json()

#     if response.status_code == 200:
#         assert isinstance(data, list)
#     elif response.status_code == 404:
#         assert data == {"detail": "Not found"}  
#     else:
#         pytest.fail(f"Unexpected status code: {response.status_code}")


# # @pytest.mark.asyncio
# # async def test_add_valid(client):
# #     response_validate = await client.post(
# #         "/auth/new",
# #         json={
# #             "last_name": "Кротов",
# #             "first_name": "Дмитро",
# #             "login": "krotov_dmitro",
# #             "password": "12345678",
# #             "role": "Продавець-консультант"
# #         }
# #     )
# #     assert response_validate.status_code == 200

# #     response_invalid = await client.post(

# #         "/auth/new",
# #         json={
# #             "last_name": "Іваненко",
# #             "first_name": "Іван",
# #             "login": "ivanenko_ivan",
# #             "password": "12345678",
# #             "role": "Продавець-консультант"
# #         }
# #     )
# #     assert response_invalid.status_code == 400

#     # data = response_validate.json()
#     # assert data == {
#     #         "message": f"Successfully add user"
#     #     }


# @pytest.mark.asyncio
# async def test_login_user(client):
#     response_valid = await client.post(
#         "/auth/login",
#         json={
#             "login": "petrov_petro",
#             "password": "12345678",
#         }
#     )

#     assert response_valid.status_code == 200

#     response_invalid_password = await client.post(
#         "/auth/login",
#         json={
#             "login": "ivanenko_ivan",
#             "password": "12345679",
#         }
#     )

#     assert response_invalid_password.status_code == 403

#     response_invalid_login = await client.post(
#         "/auth/login",
#         json={
#             "login": "ivanenko_ivan1",
#             "password": "12345678",
#         }
#     )

#     assert response_invalid_login.status_code == 401

