from pydantic import BaseModel, Field
from datetime import datetime

class ProductGetSchemas(BaseModel):
    number: int
    name: str
    price: float
    create_data: datetime

class ProductsAddSchemas(BaseModel):
    name: str = Field(min_length=1, max_length = 50)
    price: float = Field(min_length=1)
    