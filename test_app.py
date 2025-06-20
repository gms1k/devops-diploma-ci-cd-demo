from fastapi.testclient import TestClient
from app import app
from app import items_db # Додаємо імпорт items_db для тестів POST та GET /items

# Створюємо тестовий клієнт для нашого FastAPI застосунку
# TestClient дозволяє виконувати запити до нашого застосунку, не запускаючи його як окремий сервер.
# Це значно пришвидшує тестування.
client = TestClient(app)

# Тест для головного маршруту ("/") - ТЕПЕР ПЕРЕВІРЯЄ HTML-ВІДПОВІДЬ
def test_read_root_html():
    response = client.get("/")
    assert response.status_code == 200
    # Перевіряємо, що відповідь є HTML (а не JSON)
    assert "text/html" in response.headers["content-type"]
    # Перевіряємо, що певний текст з HTML присутній
    assert "Мій DevOps-проект з FastAPI" in response.text
    assert "Ласкаво просимо на демо-сторінку" in response.text
    assert "Ця сторінка розгорнута за допомогою DevOps CI/CD!" in response.text


# Тест для отримання всіх елементів ("/items")
def test_get_all_items():
    response = client.get("/items")
    assert response.status_code == 200
    # Перевіряємо, що кількість повернутих елементів дорівнює кількості в нашій імітованій БД
    assert len(response.json()) == len(items_db)
    # Перевіряємо ім'я першого елемента для підтвердження, що дані вірні
    assert response.json()[0]["name"] == "Smartphone X"

# Тест для отримання елемента за ID ("/items/{item_id}")
def test_get_item_by_id():
    response = client.get("/items/1") # Запитуємо елемент з ID = 1
    assert response.status_code == 200
    assert response.json()["name"] == "Smartphone X"

# Тест для отримання неіснуючого елемента
def test_get_nonexistent_item():
    response = client.get("/items/999") # Запитуємо елемент з ID = 999 (якого немає)
    assert response.status_code == 404 # Очікуємо статус-код 404 (Not Found)
    assert response.json() == {"detail": "Item not found"} # Перевіряємо повідомлення про помилку

# Тест для створення нового елемента ("POST /items")
def test_create_new_item():
    new_item_data = {
        "id": 4, # Новий унікальний ID
        "name": "Bluetooth Speaker",
        "price": 79.99
    }
    # Виконуємо POST-запит, передаючи дані нового елемента
    response = client.post("/items", json=new_item_data)
    assert response.status_code == 201 # Очікуємо статус-код 201 (Created)
    assert response.json()["name"] == "Bluetooth Speaker"
    # Примітка: Оскільки items_db - це список у пам'яті, доданий елемент буде існувати
    # лише протягом цього тестового запуску. При наступному запуску тестів items_db буде
    # ініціалізовано заново. Це нормально для юніт-тестів, які повинні бути незалежними.

# Тест для спроби створити елемент з існуючим ID
def test_create_item_with_existing_id():
    existing_item_data = {
        "id": 1, # ID, який вже існує в items_db
        "name": "Existing Item",
        "price": 10.0
    }
    response = client.post("/items", json=existing_item_data)
    assert response.status_code == 400 # Очікуємо статус-код 400 (Bad Request)
    assert response.json() == {"detail": "Item with this ID already exists"} # Перевіряємо повідомлення про помилку