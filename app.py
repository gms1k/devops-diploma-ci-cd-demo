from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="DevOps Pipeline Demo API",
    description="A simple FastAPI application to demonstrate a DevOps CI/CD pipeline.",
    version="1.0.0"
)

# Модель даних для елемента (Product)
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Laptop Pro",
                    "description": "High-performance laptop for professionals",
                    "price": 1500.0,
                    "tax": 150.0
                }
            ]
        }
    }

# Імітація бази даних (зберігаємо дані у пам'яті)
items_db: List[Item] = [
    Item(id=1, name="Smartphone X", description="Latest model smartphone", price=999.99, tax=50.0),
    Item(id=2, name="Wireless Earbuds", description="Noise-cancelling earbuds", price=149.99),
    Item(id=3, name="Smartwatch 5", description="Fitness tracker and smartwatch", price=299.99, tax=20.0),
]

@app.get("/", tags=["Root"])
async def read_root():
    """
    Головний маршрут, повертає вітальне повідомлення.
    """
    return {"message": "Hello from FastAPI! This is your DevOps Pipeline."}

@app.get("/items", response_model=List[Item], tags=["Items"])
async def get_items():
    """
    Повертає список всіх товарів.
    """
    return items_db

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    """
    Повертає інформацію про товар за його ID.
    """
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, status_code=201, tags=["Items"])
async def create_item(item: Item):
    """
    Додає новий товар до списку.
    """
    if any(db_item.id == item.id for db_item in items_db):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db.append(item)
    return item