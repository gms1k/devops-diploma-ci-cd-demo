from fastapi.testclient import TestClient
from app import app, items_db

client = TestClient(app)

def test_read_root_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Мій оновлений DevOps-проект з FastAPI" in response.text
    assert "оновлена демо-сторінка" in response.text
    assert "Додаткові деталі" in response.text
    assert "Автоматичне тестування" in response.text
    assert "Автоматичний деплой" in response.text
    assert "FastAPI + GitHub Actions + Render" in response.text

def test_get_all_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == len(items_db)
    assert response.json()[0]["name"] == "Smartphone X"

def test_get_item_by_id():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Smartphone X"

def test_get_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_new_item():
    new_item_data = {
        "id": 4,
        "name": "Bluetooth Speaker",
        "price": 79.99
    }
    response = client.post("/items", json=new_item_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Bluetooth Speaker"

def test_create_item_with_existing_id():
    existing_item_data = {
        "id": 1,
        "name": "Existing Item",
        "price": 10.0
    }
    response = client.post("/items", json=existing_item_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Item with this ID already exists"}
