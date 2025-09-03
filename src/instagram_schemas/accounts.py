"""Instagram user/account models."""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import (
    Field,
    ConfigDict,
    field_validator,
)
from pydantic.alias_generators import to_camel
from .base import InstagramBase


class InstagramBiographyWithEntities(InstagramBase):
    """Biography with entity information."""

    raw_text: str = Field(..., description="Raw biography text")
    entities: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Entities in biography"
    )


class InstagramHDProfilePicUrlInfo(InstagramBase):
    """HD profile picture URL information."""

    url: str = Field(..., description="HD profile picture URL")
    width: int = Field(..., description="Image width")
    height: int = Field(..., description="Image height")


class InstagramUserMetrics(InstagramBase):
    """Metrics for Instagram user."""

    follower_count: int = Field(..., description="Number of followers")
    following_count: int = Field(..., description="Number of following")
    media_count: int = Field(..., description="Number of media posts")
    total_igtv_videos: int = Field(default=0, description="Total IGTV videos")
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    @field_validator(
        "follower_count",
        "following_count",
        "media_count",
        "total_igtv_videos",
        mode="before",
    )
    @classmethod
    def validate_counts(cls, v, info):
        """Validate count fields."""
        if v is None:
            # For required fields, None should cause validation to fail
            # Only total_igtv_videos has a default, so it can handle None
            return v
        if isinstance(v, str):
            # Handle string numbers
            try:
                return int(v)
            except ValueError:
                # For invalid strings, raise validation error instead of returning None
                raise ValueError(
                    f"Cannot convert '{v}' to integer for field {info.field_name}"
                )
        return v


class InstagramUserCore(InstagramBase):
    """Core fields for Instagram user."""

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="ignore"
    )

    id: str = Field(..., alias="_id", description="User ID")
    username: str = Field(..., description="Username")
    full_name: str = Field(default="", description="Full display name")

    @field_validator("id", "username", mode="after")
    @classmethod
    def check_not_null(cls, v, info):
        if v is None or (v == ""):
            raise ValueError(f"{info.field_name!r} must not be empty")
        return v

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramUserCore":
        """Create InstagramUserCore from API response data."""
        return cls.model_validate(data)


class InstagramUser(InstagramUserCore):
    """Instagram user profile model."""

    # Profile information
    biography: Optional[str] = Field(None, description="User biography")
    biography_email: Optional[str] = Field(None, description="Email in biography")
    external_url: Optional[str] = Field(None, description="External URL")
    external_lynx_url: Optional[str] = Field(None, description="External lynx URL")
    country: Optional[str] = Field(None, description="Country of the user")

    # Profile picture
    profile_pic_url: Optional[str] = Field(None, description="Profile picture URL")
    profile_pic_url_hd: Optional[str] = Field(
        None, description="HD profile picture URL"
    )
    profile_pic_id: Optional[str] = Field(None, description="Profile picture ID")
    hd_profile_pic_url_info: Optional[InstagramHDProfilePicUrlInfo] = Field(
        None, description="HD profile picture info"
    )
    hd_profile_pic_versions: List[Dict[str, Any]] = Field(
        default_factory=list, description="HD profile pic versions"
    )
    has_anonymous_profile_picture: Optional[bool] = Field(
        None, description="Has anonymous profile picture"
    )

    # Counts and metrics
    metrics: List[InstagramUserMetrics] = Field(
        default_factory=list, description="User metrics"
    )

    # Account status and verification
    is_verified: Optional[bool] = Field(None, description="Is verified account")
    is_private: Optional[bool] = Field(None, description="Is private account")
    is_business: Optional[bool] = Field(None, description="Is business account")
    is_professional: Optional[bool] = Field(None, description="Is professional account")

    # Business information
    account_type: Optional[int] = Field(None, description="Account type")
    category: Optional[str] = Field(None, description="Account category")
    category_id: Optional[int] = Field(None, description="Business category ID")
    business_contact_method: Optional[str] = Field(
        None, description="Business contact method"
    )
    contact_phone_number: Optional[str] = Field(
        None, description="Contact phone number"
    )
    public_phone_number: Optional[str] = Field(None, description="Public phone number")
    public_phone_country_code: Optional[str] = Field(
        None, description="Phone country code"
    )
    public_email: Optional[str] = Field(None, description="Public email")

    # Additional fields
    fbid_v2: Optional[str] = Field(None, description="Facebook ID v2")
    # account_badges: Optional[List[Dict[str, Any]]] = Field(
    #     default_factory=list, description="Account badges"
    # )
    bio_links: List[Dict[str, Any]] = Field(
        default_factory=list, description="Bio links"
    )
    has_chaining: Optional[bool] = Field(None, description="Has chaining")
    has_guides: Optional[bool] = Field(None, description="Has guides")
    has_igtv_series: Optional[bool] = Field(None, description="Has IGTV series")
    latest_reel_media: Optional[int] = Field(
        None, description="Latest reel media timestamp"
    )

    # Interaction settings
    direct_messaging: Optional[str] = Field(
        None, description="Direct messaging settings"
    )
    is_call_to_action_enabled: Optional[bool] = Field(None, description="CTA enabled")
    is_category_tappable: Optional[bool] = Field(None, description="Category tappable")
    is_eligible_for_request_message: Optional[bool] = Field(
        None, description="Eligible for request message"
    )
    is_profile_audio_call_enabled: Optional[bool] = Field(
        None, description="Profile audio call enabled"
    )
    is_favorite: Optional[bool] = Field(None, description="Is favorite")
    is_favorite_for_clips: Optional[bool] = Field(
        None, description="Favorite for clips"
    )
    is_favorite_for_igtv: Optional[bool] = Field(None, description="Favorite for IGTV")
    is_favorite_for_stories: Optional[bool] = Field(
        None, description="Favorite for stories"
    )

    # Subscription and monetization
    ads_incentive_expiration_date: Optional[str] = Field(
        None, description="Ads incentive expiration"
    )
    ads_page_id: Optional[str] = Field(None, description="Ads page ID")
    ads_page_name: Optional[str] = Field(None, description="Ads page name")
    current_catalog_id: Optional[str] = Field(None, description="Current catalog ID")

    # Fundraisers
    active_standalone_fundraisers: Optional[Dict[str, Any]] = Field(
        None, description="Active fundraisers"
    )

    # Additional metadata
    date_joined: Optional[str] = Field(
        None, description="Account creation date (Month Year)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update"
    )

    @field_validator("fbid_v2", mode="before")
    @classmethod
    def validate_fbid_v2(cls, v):
        """Validate fbid_v2 field - convert int to string."""
        if v is None:
            return None
        if isinstance(v, int):
            return str(v)
        return v

    @field_validator("is_verified", "is_private", "is_business", mode="before")
    @classmethod
    def validate_booleans(cls, v):
        """Validate boolean fields."""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return bool(v) if v is not None else None

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramUser":
        """Create InstagramUser from API response data.

        Args:
            data: API response data for the user
        """

        # Prepare user data by extracting only fields that exist in our model
        user_data = {}

        # Get model fields from the class
        model_fields = cls.model_fields.keys()

        # Extract fields that exist in both the API response and our model
        for field in model_fields:
            if field in data:
                user_data[field] = data[field]

        # Handle lists that might be None
        list_fields = ["bio_links", "account_badges", "hd_profile_pic_versions"]
        for field in list_fields:
            if field in user_data and user_data[field] is None:
                user_data[field] = []

        # Collect information from the "about" section if available
        if "about" in data:
            about_data = data["about"]
            if isinstance(about_data, dict):
                # Extract country and date_joined from about section
                if "country" in about_data:
                    user_data["country"] = about_data["country"]
                if "date_joined" in about_data:
                    user_data["date_joined"] = about_data["date_joined"]

                # Extract other fields that exist in both about and our model
                for key, value in about_data.items():
                    if key in model_fields and key not in ["country", "date_joined"]:
                        user_data[key] = value

        # Create metrics from count fields in the main data
        metrics_data = {
            "follower_count": data.get("follower_count", 0),
            "following_count": data.get("following_count", 0),
            "media_count": data.get("media_count", 0),
            "total_igtv_videos": data.get("total_igtv_videos", 0),
            "updated_at": datetime.now(),
        }

        try:
            metrics = InstagramUserMetrics.model_validate(metrics_data)
            user_data["metrics"] = [metrics]
        except Exception:
            # If metrics validation fails, create empty metrics list
            user_data["metrics"] = []

        return cls.model_validate(user_data)

    def get_latest_metrics(self) -> Optional[InstagramUserMetrics]:
        """Get the most recent metrics for this user."""
        if not self.metrics:
            return None
        return max(self.metrics, key=lambda m: m.updated_at)

    def add_metrics(self, metrics: InstagramUserMetrics) -> None:
        """Add new metrics to this user."""
        self.metrics.append(metrics)

    def get_metrics_history(self) -> List[InstagramUserMetrics]:
        """Get all metrics sorted by date (oldest to newest)."""
        return sorted(self.metrics, key=lambda m: m.updated_at)

    # Backward compatibility properties
    @property
    def follower_count(self) -> Optional[int]:
        """Get the latest follower count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.follower_count if latest_metrics else None

    @property
    def following_count(self) -> Optional[int]:
        """Get the latest following count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.following_count if latest_metrics else None

    @property
    def media_count(self) -> Optional[int]:
        """Get the latest media count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.media_count if latest_metrics else None

    @property
    def total_igtv_videos(self) -> Optional[int]:
        """Get the latest IGTV videos count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.total_igtv_videos if latest_metrics else None

    # Backward-compat for removed field: account_badges
    @property
    def account_badges(self) -> List[Dict[str, Any]]:
        """Deprecated: kept for compatibility with older code/tests."""
        return []

    @account_badges.setter
    def account_badges(self, value: Any) -> None:
        # Ignore writes; field no longer exists
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return self.model_dump(by_alias=True, exclude_none=True)
