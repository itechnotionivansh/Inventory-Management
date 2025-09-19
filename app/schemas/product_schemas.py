# app/schemas/product_schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import decimal

class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    colors: List[str] = Field(..., min_items=1, description="List of available colors")
    tags: List[str] = Field(default_factory=list, description="Product tags")
    category_name: str = Field(..., min_length=1, description="Category name")

    model_config = {"extra": "forbid"}

    @field_validator("colors")
    @classmethod
    def validate_colors(cls, v: List[str]) -> List[str]:
        valid_colors = ["Black", "White", "Yellow", "Green", "Blue", "Red", "Silver", "Gold", "Deep Purple", "Lavender", "Cream", "Space Gray", "Starlight", "Midnight"]
        invalid_colors = [color for color in v if color not in valid_colors]
        if invalid_colors:
            raise ValueError(f"Invalid colors: {invalid_colors}. Valid colors: {valid_colors}")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Price must be positive")
        # Round to 2 decimal places
        return round(v, 2)


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    colors: Optional[List[str]] = Field(None, min_items=1)
    tags: Optional[List[str]] = None
    category_name: Optional[str] = Field(None, min_length=1)

    model_config = {"extra": "forbid"}

    @field_validator("colors")
    @classmethod
    def validate_colors(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return v
        valid_colors = ["Black", "White", "Yellow", "Green", "Blue", "Red", "Silver", "Gold", "Deep Purple", "Lavender", "Cream", "Space Gray", "Starlight", "Midnight"]
        invalid_colors = [color for color in v if color not in valid_colors]
        if invalid_colors:
            raise ValueError(f"Invalid colors: {invalid_colors}")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Price must be positive")
        return round(v, 2) if v is not None else v


class ProductOutSchema(BaseModel):
    id: int
    name: str
    category: str
    price: float
    colors: List[str]
    tags: List[str]
    rating: dict
    uploader: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"extra": "forbid", "from_attributes": True}