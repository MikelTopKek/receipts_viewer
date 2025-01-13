from pydantic import BaseModel, EmailStr


class UserUpdateDTO(BaseModel):
    """DTO for updating user"""
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserCreateDTO(BaseModel):
    """DTO for user creating"""
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
