import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """1. Проверка корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Marketplace API is running!"}


def test_register_user_success():
    """2. Успешная регистрация нового пользователя"""
    unique_user = f"user_{uuid.uuid4().hex[:8]}"
    payload = {
        "username": unique_user,
        "password": "secretpassword123",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["balance"] == 100.0
    assert "id" in data


def test_register_duplicate_user_fails():
    """3. Попытка зарегистрировать существующего пользователя (ошибка 400)"""
    unique_user = f"dup_{uuid.uuid4().hex[:8]}"
    payload = {
        "username": unique_user,
        "password": "password123",
    }
    # Первый раз — успешная регистрация
    res1 = client.post("/auth/register", json=payload)
    assert res1.status_code == 200

    # Второй раз с тем же именем — ошибка 400
    res2 = client.post("/auth/register", json=payload)
    assert res2.status_code == 400
    assert res2.json()["detail"] == "Username already taken"


def test_login_invalid_password():
    """4. Попытка входа с неверным паролем (ошибка 401)"""
    unique_user = f"auth_{uuid.uuid4().hex[:8]}"
    client.post(
        "/auth/register",
        json={"username": unique_user, "password": "correctpassword"},
    )

    form_data = {"username": unique_user, "password": "wrongpassword"}
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 401