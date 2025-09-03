"""Instagram media models."""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import Field, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from .accounts import InstagramUserCore
from .base import InstagramBase


class InstagramMediaInfo(InstagramBase):
    """Instagram media information model."""

    url: str = Field(..., description="Media URL")
    path: Optional[str] = Field(None, description="Local file path")
    width: Optional[int] = Field(None, description="Media width")
    height: Optional[int] = Field(None, description="Media height")


class TaggedUser(InstagramUserCore):
    """Tagged user in media model."""

    # Position coordinates (0.0 to 1.0)
    x: float = Field(..., description="X coordinate (0.0 to 1.0)")
    y: float = Field(..., description="Y coordinate (0.0 to 1.0)")
    position: Optional[List[float]] = Field(
        None, description="Position as [x, y] array"
    )

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "TaggedUser":
        """Create TaggedUser from API response data."""
        # Handle position array format
        x = data.get("x", 0.5)
        y = data.get("y", 0.5)

        # If position array is provided, use those values
        if (
            "position" in data
            and isinstance(data["position"], list)
            and len(data["position"]) >= 2
        ):
            x = data["position"][0]
            y = data["position"][1]

        user_data = data.get("user", {})

        # Extract required fields with fallbacks
        user_id = user_data.get("id") or "unknown_user"
        username = user_data.get("username") or "unknown"
        full_name = user_data.get("full_name") or ""

        # Create a data dict and use model_validate instead of direct construction
        user_data = {
            "x": x,
            "y": y,
            "position": data.get("position"),
            "id": user_id,  # This will work with model_validate
            "username": username,
            "full_name": full_name,
        }

        return cls.model_validate(user_data)


class InstagramMedia(InstagramBase):
    """Instagram media model for carousel items and standalone media."""

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, arbitrary_types_allowed=True
    )

    # Core identification
    id: Optional[str] = Field(None, description="Media ID")
    pk: Optional[str] = Field(None, description="Primary key")

    # Media type and format
    media_type: Optional[int] = Field(None, description="Media type (1=image, 2=video)")

    # Format and product type
    media_format: Optional[str] = Field(None, description="Media format")
    product_type: Optional[str] = Field(None, description="Product type")

    # Dimensions
    original_width: Optional[int] = Field(None, description="Original width")
    original_height: Optional[int] = Field(None, description="Original height")

    # Image information
    image_versions: Optional[List[InstagramMediaInfo]] = Field(
        default_factory=list, description="Image versions"
    )

    # Video information
    video_versions: Optional[List[InstagramMediaInfo]] = Field(
        default_factory=list, description="Video versions"
    )
    video_duration: Optional[float] = Field(
        None, description="Video duration in seconds"
    )
    has_audio: Optional[bool] = Field(None, description="Has audio track")

    # Tagged users
    tagged_users: List[TaggedUser] = Field(
        default_factory=list, description="Tagged users in media"
    )

    # Status
    is_video: Optional[bool] = Field(None, description="Is video media")

    # Carousel specific
    carousel_media_count: Optional[int] = Field(
        None, description="Number of items in carousel"
    )
    carousel_media: Optional[List["InstagramMedia"]] = Field(
        default_factory=list, description="Carousel media items"
    )

    # Additional metadata
    accessibility_caption: Optional[str] = Field(
        None, description="Accessibility caption"
    )
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now, description="Update timestamp"
    )

    @field_validator("media_type", mode="before")
    @classmethod
    def validate_media_type(cls, v, info):
        """Validate media type."""
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return 1  # Default to image
        return v or 1

    @field_validator("video_duration", mode="before")
    @classmethod
    def validate_video_duration(cls, v, info):
        """Validate video duration."""
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return None
        return v

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramMedia":
        """Create InstagramMedia from API response data."""
        media_data = {}
        # Core fields
        media_data["id"] = data.get("id", data.get("pk"))
        media_data["pk"] = data.get("pk", data.get("id"))
        media_data["media_type"] = data.get("media_type", 1)
        media_data["media_format"] = data.get("media_format")
        media_data["product_type"] = data.get("product_type")

        # Dimensions
        media_data["original_width"] = data.get("original_width")
        media_data["original_height"] = data.get("original_height")

        # Image versions
        if "image_versions" in data:
            image_versions = []
            image_data = data["image_versions"]
            # Handle both list format and dict with "items" format
            if isinstance(image_data, list):
                image_list = image_data
            else:
                image_list = image_data.get("items", [])

            for img in image_list:
                image_versions.append(
                    InstagramMediaInfo(
                        url=img["url"],
                        path=None,  # Path is optional and can be set later
                        width=img.get("width"),
                        height=img.get("height"),
                    )
                )
            media_data["image_versions"] = image_versions

        # Video versions
        if "video_versions" in data and data["video_versions"]:
            video_versions = []
            for vid in data["video_versions"]:
                video_versions.append(
                    InstagramMediaInfo(
                        url=vid["url"],
                        path=None,  # Path is optional and can be set later
                        width=vid.get("width"),
                        height=vid.get("height"),
                    )
                )
            media_data["video_versions"] = video_versions

        # Video specific
        media_data["video_duration"] = data.get("video_duration")
        media_data["has_audio"] = data.get("has_audio")
        media_data["is_video"] = data.get("is_video", data.get("media_type") == 2)

        # Carousel
        if "carousel_media_count" in data:
            media_data["carousel_media_count"] = data["carousel_media_count"]

        if "carousel_media" in data and data["carousel_media"]:
            carousel_items = []
            for item in data["carousel_media"]:
                carousel_items.append(cls.from_api_response(item))
            media_data["carousel_media"] = carousel_items

        # Tagged users
        tagged_users = []
        for tag_data in data.get("tagged_users") or []:
            tagged_users.append(TaggedUser.from_api_response(tag_data))
        media_data["tagged_users"] = tagged_users

        # Additional fields
        media_data["accessibility_caption"] = data.get("accessibility_caption")

        return cls.model_validate(media_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return self.model_dump(by_alias=True, exclude_none=True)
