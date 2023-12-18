import pytest
from tests.conftest import client


@pytest.mark.asyncio
async def test_create_wallet():
    user_data = {"name": "Kawasaki", "email": "cago@gmail.com"}

    client.post("/create_user/", json=user_data)

    response = client.get("/get_user", params={"user_data": user_data["name"]})
    print(response.url)
    assert response.status_code == 200
    assert response.json() == user_data
