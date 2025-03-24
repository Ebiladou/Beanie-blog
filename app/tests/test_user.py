import pytest
from starlette.testclient import TestClient

@pytest.mark.anyio
async def test_create_user(client: TestClient):
    user_data = {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "1234",
        "bio": "hottie in test"
    }
    response = await client.post("/user/", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]
    assert response.json()["email"] == user_data["email"]