import pytest
import pytest_asyncio
from src.main import app
from src.tests.conftest import client

@pytest_asyncio.fixture(scope="function")
async def test_add_valid(client):
    response_valid = await client.post(
        "/auth/new",
        json={
            "last_name": "Іваненко",
            "first_name": "Іван",
            "login": "ivanenko_ivan",
            "password": "12345678",
            "role": "Продавець-консультант"
        }
    )
    assert response_valid.status_code == 400
    response_invalid = await client.post(
        "/auth/new",
        json={
            "last_name": "Іваненко",
            "first_name": "Іван",
            "login": "ivanenko_ivan",
            "password": "12345678",
            "role": "Продавець-консультант"
        }
    )
    assert response_invalid.status_code == 400
    yield 
    
@pytest.mark.asyncio
async def test_login_user(client):
    response_valid = await client.post(
        "/auth/login",
        json={
            "login": "petrov_petro",
            "password": "12345678",
        }
    )

    assert response_valid.status_code == 200

    response_invalid_password = await client.post(
        "/auth/login",
        json={
            "login": "ivanenko_ivan",
            "password": "12345679",
        }
    )

    assert response_invalid_password.status_code == 403

    response_invalid_login = await client.post(
        "/auth/login",
        json={
            "login": "ivanenko_ivan1",
            "password": "12345678",
        }
    )

    assert response_invalid_login.status_code == 401

