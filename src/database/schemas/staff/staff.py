from pydantic import BaseModel, Field, EmailStr

class StaffAddSchemas(BaseModel):

    id: int 
    last_name: str = Field(max_length=1, max_length=70)
    first_name: str = Field(min_length=1, max_length=70)
    email: EmailStr 
    password: str = Field(min_length=8, max_length=128)
    role: str 
