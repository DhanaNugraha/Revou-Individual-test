from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator
from datetime import datetime


class PublicUserProfileResponse(BaseModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    profile_image_url: str | None
    bio: str | None
    is_vendor: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class UserProfileUpdateRequest(BaseModel):
    bio: str | None = None
    profile_image_url: HttpUrl | None = None  # Validates URL format
    first_name: str | None = None
    last_name: str | None = None

    @field_validator("bio")
    def validate_bio(cls, value):
        if value and len(value) > 500:
            raise ValueError("Bio cannot exceed 500 characters")
        return value
