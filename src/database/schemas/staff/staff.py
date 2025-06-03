from pydantic import BaseModel, Field

class StaffAddSchemas(BaseModel):
 
    last_name: str = Field(min_length=1, max_length=70)
    first_name: str = Field(min_length=1, max_length=70)
    login: str = Field(min_length=1, max_length=70)
    password: str = Field(min_length=8, max_length=128)
    role: str 

class StaffGetSchemas(BaseModel):

    id: int
    last_name: str
    first_name: str
    login: str
    password: str
    role: str

class StaffLoginSchemas(BaseModel):

    login: str
    password: str
