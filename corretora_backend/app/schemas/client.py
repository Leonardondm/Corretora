from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    address: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True