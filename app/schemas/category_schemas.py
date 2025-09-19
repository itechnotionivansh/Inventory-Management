# app/schemas/category_schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Category name")

    model_config = {"extra": "forbid"}


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

    model_config = {"extra": "forbid"}


class CategoryOutSchema(BaseModel):
    id: int
    name: str
    productCount: int
    created_at: Optional[datetime] = None

    model_config = {"extra": "forbid", "from_attributes": True}