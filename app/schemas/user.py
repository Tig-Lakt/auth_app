from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="strongpassword123")

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None

class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True