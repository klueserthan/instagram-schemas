"""Instagram locations models."""

from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import Field, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from .base import InstagramBase


class InstagramLocation(InstagramBase):
    """Instagram location model."""

    # Core identification
    pk: Optional[str] = Field(None, description="Location ID")
    id: Optional[str] = Field(None, description="Alternative location ID")
    facebook_places_id: Optional[int] = Field(None, description="Facebook Places ID")

    # Basic information
    name: Optional[str] = Field(None, description="Location name")
    short_name: Optional[str] = Field(None, description="Short location name")
    address: Optional[str] = Field(None, description="Full address")
    city: Optional[str] = Field(None, description="City name")

    # Geographic coordinates
    lng: Optional[float] = Field(None, description="Longitude")
    lat: Optional[float] = Field(None, description="Latitude")

    # External references
    external_source: Optional[str] = Field(None, description="External data source")
    external_id: Optional[str] = Field(None, description="External ID")
    external_id_source: Optional[str] = Field(None, description="External ID source")

    # Additional metadata
    has_viewer_saved: Optional[bool] = Field(
        None, description="User has saved location"
    )
    blurb: Optional[str] = Field(None, description="Location description")
    website: Optional[str] = Field(None, description="Location website")
    phone: Optional[str] = Field(None, description="Location phone number")

    # Social media counts
    media_count: Optional[int] = Field(None, description="Number of posts at location")

    # Timestamps
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Update timestamp"
    )

    @field_validator("lng", "lat", mode="before")
    @classmethod
    def validate_coordinates(cls, v, info):
        """Validate coordinate fields."""
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return None
        return v

    @field_validator("media_count", mode="before")
    @classmethod
    def validate_media_count(cls, v, info):
        """Validate media count."""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return None
        return v

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramLocation":
        """Create InstagramLocation from API response data."""
        location_data = {}

        # Core identification
        location_data["pk"] = data.get("pk", data.get("id"))
        location_data["id"] = data.get("id", data.get("pk"))
        location_data["facebook_places_id"] = data.get("facebook_places_id")

        # Basic information
        location_data["name"] = data.get("name")
        location_data["short_name"] = data.get("short_name")
        location_data["address"] = data.get("address")
        location_data["city"] = data.get("city")

        # Coordinates
        location_data["lng"] = data.get("lng")
        location_data["lat"] = data.get("lat")

        # External references
        location_data["external_source"] = data.get("external_source")
        location_data["external_id"] = data.get("external_id")
        location_data["external_id_source"] = data.get("external_id_source")

        # Additional metadata
        location_data["has_viewer_saved"] = data.get("has_viewer_saved")
        location_data["blurb"] = data.get("blurb")
        location_data["website"] = data.get("website")
        location_data["phone"] = data.get("phone")
        location_data["media_count"] = data.get("media_count", 0)

        return cls(**location_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return self.model_dump(by_alias=True, exclude_none=True)
