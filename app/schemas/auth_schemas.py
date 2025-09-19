# app/schemas/auth_schemas.py
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime

class RegisterSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the user")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=128, description="Password with minimum 6 characters")
    confirm_password: Optional[str] = Field(None, description="Password confirmation")

    model_config = {"extra": "forbid"}

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @model_validator(mode="after")
    def passwords_match(self):
        if self.confirm_password is not None and self.password != self.confirm_password:
            raise ValueError("Password and confirm_password do not match")
        return self


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")

    model_config = {"extra": "forbid"}


class ChangePasswordSchema(BaseModel):
    current_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=6, max_length=128, description="New password")
    confirm_new_password: Optional[str] = Field(None, description="New password confirmation")

    model_config = {"extra": "forbid"}

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("New password must be at least 6 characters long")
        return v

    @model_validator(mode="after")
    def passwords_match(self):
        if self.confirm_new_password is not None and self.new_password != self.confirm_new_password:
            raise ValueError("New password and confirm_new_password do not match")
        return self


class UserOutSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: Optional[datetime] = None
    is_active: bool = True

    model_config = {"extra": "forbid", "from_attributes": True}