from pydantic import BaseModel, Field
from datetime import datetime

class OrdersGetSchemas(BaseModel):
    """Схема для отримання замовленнь"""

    id_order: int
    name_product: str 
    status: str
    price: float
    discount: float
    create_data: datetime

class OrdersAddSchemas(BaseModel):
    """Схема для додавання замовлень"""

    id_product: int

class OrdersUpdateSchemas(BaseModel):
    """Схема для оновлення замовлень"""

    status: str

class OrdersCheckSchemas(BaseModel):
    """Схема для формування рахунку"""

    id_order: int
    name_product: str
    price: float
    discount: float
    create_data: datetime
    create_data_order: datetime

class OrderCreateResponse(BaseModel):
    """Схема для виводу повідомлення після додавання замовлення"""

    message: str
    id_order: int
    id_product: int
    price: float
    discount: float
    status: str
    create_data: datetime