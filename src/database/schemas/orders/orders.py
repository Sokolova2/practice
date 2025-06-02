from pydantic import BaseModel, Field
from datetime import datetime

class OrdersGetSchemas(BaseModel):
    id_order: int
    name_product: str 
    status: str
    discount: float
    create_data: datetime

class OrdersAddSchemas(BaseModel):
    id_product: int
    discount: float