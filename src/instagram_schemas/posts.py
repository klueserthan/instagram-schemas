"""Instagram posts models."""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import (
    Field,
    ConfigDict,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel

from .accounts import InstagramUserCore
from .media import InstagramMedia
from .locations import InstagramLocation
from .base import InstagramBase


class InstagramCaption(InstagramBase):
    """Instagram post caption model."""

    type: Optional[int] = Field(None, description="Caption type")
    text: Optional[str] = Field(None, description="Caption text")
    created_at: Optional[datetime] = Field(None, description="Caption creation time")
    created_at_utc: Optional[datetime] = Field(
        None, description="Caption creation time (UTC)"
    )
    hashtags: List[str] = Field(default_factory=list)
    mentions: List[str] = Field(default_factory=list)

    @field_validator("created_at", "created_at_utc", mode="before")
    @classmethod
    def convert_timestamps(cls, v, info):
        """Convert timestamp to datetime."""
        if isinstance(v, int):
            return datetime.fromtimestamp(v)
        elif isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                # For invalid string dates, return None to allow the field to be None
                return None
        return v


class InstagramPostMetrics(InstagramBase):
    """Instagram post metrics model."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,  # This allows both snake_case and camelCase
    )

    like_count: Optional[int] = Field(default=None, description="Number of likes")
    comment_count: Optional[int] = Field(default=None, description="Number of comments")
    view_count: Optional[int] = Field(default=None, description="Number of views")
    play_count: Optional[int] = Field(default=None, description="Number of plays")
    fb_like_count: Optional[int] = Field(
        default=None, description="Facebook like count"
    )
    fb_play_count: Optional[int] = Field(
        default=None, description="Facebook play count"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Update timestamp"
    )

    @field_validator(
        "like_count",
        "comment_count",
        "view_count",
        "play_count",
        "fb_like_count",
        "fb_play_count",
        mode="before",
    )
    @classmethod
    def validate_counts(cls, v, info):
        """Validate count fields."""
        if v is None:
            return None  # Use None as a placeholder for missing counts
        if isinstance(v, str):
            # Handle string numbers
            try:
                return int(v)
            except ValueError:
                return None
        return v


class InstagramPost(InstagramBase):
    """Instagram post model."""

    # Core fields
    model_type: str = Field(default="post", description="Model type identifier")
    id: str = Field(..., alias="_id", description="Post ID")
    code: str = Field(..., description="Post shortcode/identifier")
    taken_at: datetime = Field(..., description="Post creation datetime")

    taken_at_date: Optional[datetime] = Field(None, description="Post date")

    # Content
    caption: Optional[InstagramCaption] = Field(None, description="Post caption")
    accessibility_caption: Optional[str] = Field(
        None, description="Accessibility caption"
    )
    caption_is_edited: Optional[bool] = Field(None, description="Caption edited flag")

    # Media information
    media_type: int = Field(
        ..., description="Media type (1=image, 2=video, 8=carousel)"
    )
    media_format: Optional[str] = Field(None, description="Media format")
    media_name: Optional[str] = Field(None, description="Media name")
    product_type: Optional[str] = Field(None, description="Product type")

    # Media
    media: List[InstagramMedia] = Field(
        default_factory=list, description="Media items in post"
    )

    # Engagement metrics
    metrics: List[InstagramPostMetrics] = Field(
        default_factory=list, description="Engagement metrics for the post"
    )

    # User and location
    user: InstagramUserCore = Field(..., description="Post author")
    location: Optional[InstagramLocation] = Field(None, description="Post location")

    # Post settings and status
    is_video: Optional[bool] = Field(None, description="Is video post")
    is_private: Optional[bool] = Field(None, description="Is private post")
    is_paid_partnership: Optional[bool] = Field(None, description="Is paid partnership")
    is_pinned: Optional[bool] = Field(None, description="Is pinned post")
    has_liked: Optional[bool] = Field(None, description="Has user liked")
    has_viewed: Optional[bool] = Field(None, description="Has user viewed")
    can_reply: Optional[bool] = Field(None, description="Can reply to post")
    can_reshare: Optional[bool] = Field(None, description="Can reshare post")
    can_save: Optional[bool] = Field(None, description="Can save post")

    # Comments
    comments_disabled: Optional[bool] = Field(None, description="Comments disabled")
    preview_comments: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Preview comments"
    )

    # Additional metadata
    filter_type: Optional[int] = Field(None, description="Filter type")
    device_timestamp: Optional[int] = Field(None, description="Device timestamp")
    fb_user_tags: Optional[Dict[str, Any]] = Field(
        None, description="Facebook user tags"
    )
    tagged_users: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Tagged users"
    )

    # Sharing and cross-posting
    has_shared_to_fb: Optional[int] = Field(None, description="Shared to Facebook")
    fbid: Optional[str] = Field(None, description="Facebook ID")

    # Additional fields
    deleted_reason: Optional[int] = Field(None, description="Deleted reason")
    fb_aggregated_comment_count: Optional[int] = Field(
        None, description="FB aggregated comment count"
    )
    fb_aggregated_like_count: Optional[int] = Field(
        None, description="FB aggregated like count"
    )
    fundraiser_tag: Optional[Dict[str, Any]] = Field(None, description="Fundraiser tag")
    gen_ai_detection_method: Optional[Dict[str, Any]] = Field(
        None, description="Gen AI detection method"
    )
    has_high_risk_gen_ai_inform_treatment: Optional[bool] = Field(
        None, description="Has high risk gen AI inform treatment"
    )
    integrity_review_decision: Optional[str] = Field(
        None, description="Integrity review decision"
    )
    invited_coauthor_producers: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Invited coauthor producers"
    )
    is_quiet_post: Optional[bool] = Field(None, description="Is quiet post")

    # Coauthor producers
    coauthor_producer_can_see_organic_insights: Optional[bool] = Field(
        None, description="Coauthor producer can see organic insights"
    )
    coauthor_producers: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Coauthor producers"
    )

    # Comment inform treatment
    comment_inform_treatment: Optional[Dict[str, Any]] = Field(
        None, description="Comment inform treatment"
    )

    # Timestamps
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.now, description="Ingestion timestamp"
    )

    def get_latest_metrics(self) -> Optional[InstagramPostMetrics]:
        """Get the most recent metrics for this post."""
        if not self.metrics:
            return None
        return max(self.metrics, key=lambda m: m.updated_at)

    def add_metrics(self, metrics: InstagramPostMetrics) -> None:
        """Add new metrics to this post."""
        self.metrics.append(metrics)

    def get_metrics_history(self) -> List[InstagramPostMetrics]:
        """Get all metrics sorted by date (oldest to newest)."""
        return sorted(self.metrics, key=lambda m: m.updated_at)

    # Backward compatibility properties
    @property
    def like_count(self) -> Optional[int]:
        """Get the latest like count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.like_count if latest_metrics else None

    @property
    def comment_count(self) -> Optional[int]:
        """Get the latest comment count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.comment_count if latest_metrics else None

    @property
    def view_count(self) -> Optional[int]:
        """Get the latest view count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.view_count if latest_metrics else None

    @property
    def play_count(self) -> Optional[int]:
        """Get the latest play count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.play_count if latest_metrics else None

    @property
    def fb_like_count(self) -> Optional[int]:
        """Get the latest Facebook like count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.fb_like_count if latest_metrics else None

    @property
    def fb_play_count(self) -> Optional[int]:
        """Get the latest Facebook play count."""
        latest_metrics = self.get_latest_metrics()
        return latest_metrics.fb_play_count if latest_metrics else None

    @field_validator("taken_at", "taken_at_date", mode="before")
    @classmethod
    def convert_timestamps(cls, v, info):
        """Convert timestamp to datetime."""
        if isinstance(v, int):
            return datetime.fromtimestamp(v)
        elif isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                # For invalid string dates, return None to allow the field to be None
                return None
        return v

    @model_validator(mode="after")
    def populate_taken_at_date(self) -> "InstagramPost":
        """Populate taken_at_date from taken_at if not already set."""
        if self.taken_at and not self.taken_at_date:
            self.taken_at_date = self.taken_at
        return self

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramPost":
        """Create InstagramPost from API response data.

        Args:
            data: API response data for the post
        """

        # Prepare post data by extracting only fields that exist in our model
        post_data = {}

        # Get model fields from the class
        model_fields = cls.model_fields.keys()

        # Extract fields that exist in both the API response and our model
        for field in model_fields:
            if field in data:
                post_data[field] = data[field]

        # Create metrics from count fields in the main data or nested metrics
        metrics = []
        try:
            metrics_data = data.get("metrics", {})
            if metrics_data:
                metrics.append(InstagramPostMetrics.model_validate(metrics_data))
        except Exception:
            # Use empty metrics as fallback
            pass
        post_data["metrics"] = metrics

        # Handle lists that might be None
        list_fields = [
            "media",
            "preview_comments",
            "tagged_users",
            "coauthor_producers",
            "invited_coauthor_producers",
        ]
        for field in list_fields:
            if field in post_data and post_data[field] is None:
                post_data[field] = []

        # Handle caption
        post_data["caption"] = (
            InstagramCaption.model_validate(data.get("caption", {}))
            if data.get("caption")
            else None
        )

        # Handle user
        post_data["user"] = InstagramUserCore.model_validate(data.get("user", {}))

        # Handle location
        post_data["location"] = (
            InstagramLocation.model_validate(data.get("location", {}))
            if data.get("location", None)
            else None
        )

        # Handle media items
        media_items = []

        # Determine if this is a video post from top-level fields
        is_video_post = data.get("is_video", False) or data.get("media_type") == 2

        # For single video posts (is_video=True at post level)
        if is_video_post and "video_versions" in data and data["video_versions"]:
            # Create complete media data including tagged users and video info
            media_data = {
                "media_type": 2,  # Video
                "id": data.get("id", f"vid_{len(media_items)}"),
                "tagged_users": data.get("tagged_users", []),
                "video_versions": data["video_versions"],
                "video_duration": data.get("video_duration"),
                "has_audio": data.get("has_audio"),
                "original_width": data.get("original_width"),
                "original_height": data.get("original_height"),
            }
            media_items.append(InstagramMedia.from_api_response(media_data))
        # For single image posts (when not a video and has image_versions)
        elif not is_video_post and "image_versions" in data and data["image_versions"]:
            # Create complete media data including tagged users and image info
            media_data = {
                "media_type": 1,  # Image
                "id": data.get("id", f"img_{len(media_items)}"),
                "tagged_users": data.get("tagged_users", []),
                "image_versions": data["image_versions"],
                "original_width": data.get("original_width"),
                "original_height": data.get("original_height"),
            }
            media_items.append(InstagramMedia.from_api_response(media_data))

        # For carousel posts, process carousel media
        if "carousel_media" in data and data["carousel_media"]:
            for idx, item in enumerate(data["carousel_media"]):
                # Pass the complete carousel item to InstagramMedia.from_api_response
                # which will handle all image_versions and video_versions internally
                carousel_media_data = {
                    **item,
                    "id": item.get("id", f"carousel_item_{idx}"),
                }
                media_items.append(
                    InstagramMedia.from_api_response(carousel_media_data)
                )

        post_data["media"] = media_items

        # Handle gen_ai_detection_method extraction
        if "gen_ai_detection_method" in data and data["gen_ai_detection_method"]:
            gen_ai_data = data["gen_ai_detection_method"]
            if isinstance(gen_ai_data, dict):
                post_data["gen_ai_detection_method"] = gen_ai_data

        # Set is_video based on media_type for backward compatibility
        post_data["is_video"] = post_data.get("media_type") == 2

        return cls.model_validate(post_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        return data
