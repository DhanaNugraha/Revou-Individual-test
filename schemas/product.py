from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List
from decimal import Decimal


class ProductCreateRequest(BaseModel):
    name: str 
    description: str 
    price: Decimal = Field(..., gt=0, decimal_places=2) #greater than 0, 2 decimal places
    category_id: int = None
    tags: List[str] = []
    sustainability_attributes: List[str] = []
    stock_quantity: int
    min_order_quantity: int = 1

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 100:
            raise ValueError("Name must be between 3 and 100 characters")
        
        return value
    
    @field_validator("description")
    def validate_description(cls, value):
        if len(value) < 10 or len(value) > 2000:
            raise ValueError("Description must be between 10 and 2000 characters")
        
        return value
    
    @field_validator("tags")
    def validate_tags(cls, value):
        if len(value) > 10:
            raise ValueError("Maximum of 10 tags allowed")
        
        return value
    
    @field_validator("sustainability_attributes")
    def validate_sustainability_attributes(cls, value):
        if len(value) > 5:
            raise ValueError("Maximum of 5 sustainability attributes allowed")
        
        return value
    
    @field_validator("stock_quantity")
    def validate_stock_quantity(cls, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        return value
    
    @field_validator("min_order_quantity")
    def validate_min_order_quantity(cls, value):
        if value < 1:
            raise ValueError("Minimum order quantity must be at least 1")
        
        return value



class ProductCreatedResponse(BaseModel):
    id: int
    name: str
    vendor_id: int

    model_config = ConfigDict(from_attributes=True)
