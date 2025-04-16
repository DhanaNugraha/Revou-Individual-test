from pydantic import BaseModel, field_validator
import re


class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    is_vendor: bool = False

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError(
                "Username can only contain letters, numbers and underscores"
            )
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value
    
    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError('Email cannot be empty')
        
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if not re.fullmatch(pattern, value):
            raise ValueError('Invalid email format')
        
        # Additional checks
        if '..' in value:
            raise ValueError('Invalid email: consecutive dots')
            
        if len(value.split('@')[0]) > 64:
            raise ValueError('Email username too long (max 64 chars)')
            
        return value.lower()  # Normalize to lowercase