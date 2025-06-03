from pydantic import BaseModel, Field
from datetime import datetime

class OrdersGetSchemas(BaseModel):
    id_order: int
    name_product: str 
    status: str
    price: float
    discount: float
    create_data: datetime

class OrdersAddSchemas(BaseModel):
    id_product: int

class OrdersUpdateSchemas(BaseModel):
    status: str

class OrdersCheckSchemas(BaseModel):
    id_order: int
    name_product: str
    price: float
    discount: float
    create_data: datetime