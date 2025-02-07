from pydantic import BaseModel, EmailStr, field_serializer
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime | None) -> str | None:
        if dt is None:
            return None
        return dt.isoformat()

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str