"""Instagram stories models."""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import (
    Field,
    field_validator,
    ValidationError,
)
from pydantic.alias_generators import to_camel

from .accounts import InstagramUserCore
from .media import InstagramMedia
from .locations import InstagramLocation
from .base import InstagramBase


class InstagramStoryMention(InstagramBase):
    """Instagram story mention model."""

    user: InstagramUserCore = Field(..., description="Mentioned user")
    display_type: Optional[str] = Field(None, description="Display type")
    x: Optional[float] = Field(None, description="X position")
    y: Optional[float] = Field(None, description="Y position")
    z: Optional[int] = Field(None, description="Z position")
    width: Optional[float] = Field(None, description="Width")
    height: Optional[float] = Field(None, description="Height")
    rotation: Optional[float] = Field(None, description="Rotation")
    start_time_ms: Optional[int] = Field(None, description="Start time in milliseconds")
    end_time_ms: Optional[int] = Field(None, description="End time in milliseconds")
    is_pinned: Optional[bool] = Field(None, description="Is pinned")
    is_hidden: Optional[bool] = Field(None, description="Is hidden")
    is_sticker: Optional[bool] = Field(None, description="Is sticker")
    is_fb_sticker: Optional[bool] = Field(None, description="Is Facebook sticker")

    @field_validator(
        "is_pinned", "is_hidden", "is_sticker", "is_fb_sticker", mode="before"
    )
    @classmethod
    def int_to_bool(cls, v: Any, info) -> Any:
        """Convert integer values to boolean, leave other types unchanged."""
        if isinstance(v, int):
            return bool(v)
        return v

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramStoryMention":
        """Create an InstagramStoryMention from API response data.

        Args:
            data: API response data for the mention

        Returns:
            An InstagramStoryMention object
        """
        # Make a copy of the data to avoid modifying the original
        processed = data.copy()

        # Extract user from user object if present
        processed["user"] = InstagramUserCore.model_validate(data.get("user", {}))

        return cls.model_validate(processed)

    @classmethod
    def from_api_response_items(
        cls, data: List[Dict[str, Any]]
    ) -> List["InstagramStoryMention"]:
        """Create a list of InstagramStoryMention from API response data.

        Args:
            data: List of API response data for mentions

        Returns:
            A list of InstagramStoryMention objects
        """
        mentions = []
        for item in data:
            try:
                mentions.append(cls.from_api_response(item))
            except ValidationError:
                continue
        return mentions


class InstagramStoryItem(InstagramBase):
    """Instagram story model."""

    # Core fields
    id: str = Field(..., alias="_id", description="Story ID")
    code: str = Field(..., description="Story shortcode")
    taken_at: datetime = Field(..., description="Story timestamp")

    # Content
    caption: Optional[str] = Field(None, description="Story caption")
    caption_is_edited: Optional[bool] = Field(None, description="Caption edited flag")

    # Media information
    media_type: int = Field(..., description="Media type (1=image, 2=video)")
    media_format: Optional[str] = Field(None, description="Media format")
    media_name: Optional[str] = Field(None, description="Media name")
    product_type: Optional[str] = Field(None, description="Product type")

    # Media
    media: InstagramMedia = Field(description="Media item in story item")

    # User and location
    user: Optional[InstagramUserCore] = Field(None, description="Story author")
    owner: Optional[InstagramUserCore] = Field(None, description="Story owner")
    location: Optional[InstagramLocation] = Field(None, description="Story location")

    # Story-specific fields
    is_video: Optional[bool] = Field(None, description="Is video story")
    is_private: Optional[bool] = Field(None, description="Is private story")
    is_paid_partnership: Optional[bool] = Field(None, description="Is paid partnership")
    is_pinned: Optional[bool] = Field(None, description="Is pinned story")
    is_archived: Optional[bool] = Field(None, description="Is archived story")
    is_reel_media: Optional[bool] = Field(None, description="Is reel media")

    # Story interactions
    has_liked: Optional[bool] = Field(None, description="Has user liked")
    has_privately_liked: Optional[bool] = Field(
        None, description="Has user privately liked"
    )
    has_viewed: Optional[bool] = Field(None, description="Has user viewed")
    can_reply: Optional[bool] = Field(None, description="Can reply to story")
    can_reshare: Optional[bool] = Field(None, description="Can reshare story")
    can_save: Optional[bool] = Field(None, description="Can save story")
    can_hype: Optional[bool] = Field(None, description="Can hype story")
    can_send_prompt: Optional[bool] = Field(None, description="Can send prompt")

    # Story mentions and reshares
    reel_mentions: List[InstagramStoryMention] = Field(
        default_factory=list, description="Story mentions"
    )
    reshared_story_media_author: Optional[str] = Field(
        None, description="Username of reshared story media author"
    )

    # Additional metadata
    filter_type: Optional[int] = Field(None, description="Filter type")
    device_timestamp: Optional[int] = Field(None, description="Device timestamp")
    tagged_users: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Tagged users"
    )

    # Story stickers and interactive elements
    cutout_sticker_info: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Cutout sticker info"
    )
    video_sticker_locales: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Video sticker locales"
    )

    # Sharing and cross-posting
    fbid: Optional[str] = Field(None, description="Facebook ID")
    crosspost_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Crosspost metadata"
    )
    sharing_friction_info: Optional[Dict[str, Any]] = Field(
        None, description="Sharing friction info"
    )

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

    # Coauthor producers
    coauthor_producer_can_see_organic_insights: Optional[bool] = Field(
        None, description="Coauthor producer can see organic insights"
    )
    coauthor_producers: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Coauthor producers"
    )

    # Music and audio
    music_metadata: Optional[Dict[str, Any]] = Field(None, description="Music metadata")
    can_play_spotify_audio: Optional[bool] = Field(
        None, description="Can play Spotify audio"
    )
    has_audio: Optional[bool] = Field(None, description="Has audio")

    # Story-specific flags
    is_first_take: Optional[bool] = Field(None, description="Is first take")
    is_quicksnap_recap: Optional[bool] = Field(None, description="Is quicksnap recap")
    is_photo_mash_story: Optional[bool] = Field(None, description="Is photo mash story")
    is_post_live_clips_media: Optional[bool] = Field(
        None, description="Is post live clips media"
    )
    is_cutout_sticker_allowed: Optional[bool] = Field(
        None, description="Is cutout sticker allowed"
    )
    is_comments_gif_composer_enabled: Optional[bool] = Field(
        None, description="Is comments GIF composer enabled"
    )
    is_from_discovery_surface: Optional[bool] = Field(
        None, description="Is from discovery surface"
    )
    is_in_profile_grid: Optional[bool] = Field(None, description="Is in profile grid")
    is_open_to_public_submission: Optional[bool] = Field(
        None, description="Is open to public submission"
    )
    is_organic_product_tagging_eligible: Optional[bool] = Field(
        None, description="Is organic product tagging eligible"
    )
    is_reshare_of_text_post_app_media_in_ig: Optional[bool] = Field(
        None, description="Is reshare of text post app media in IG"
    )
    is_tagged_media_shared_to_viewer_profile_grid: Optional[bool] = Field(
        None, description="Is tagged media shared to viewer profile grid"
    )
    is_terminal_video_segment: Optional[bool] = Field(
        None, description="Is terminal video segment"
    )
    is_viewer_mentioned: Optional[bool] = Field(None, description="Is viewer mentioned")

    # Story settings
    like_and_view_counts_disabled: Optional[bool] = Field(
        None, description="Like and view counts disabled"
    )
    supports_reel_reactions: Optional[bool] = Field(
        None, description="Supports reel reactions"
    )
    archive_story_deletion_ts: Optional[int] = Field(
        None, description="Archive story deletion timestamp"
    )

    # Boost and promotion
    boost_unavailable_identifier: Optional[str] = Field(
        None, description="Boost unavailable identifier"
    )
    boost_unavailable_reason: Optional[str] = Field(
        None, description="Boost unavailable reason"
    )
    boost_unavailable_reason_v2: Optional[str] = Field(
        None, description="Boost unavailable reason v2"
    )

    # Shopping and products
    shop_routing_user_id: Optional[str] = Field(
        None, description="Shop routing user ID"
    )
    product_suggestions: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Product suggestions"
    )
    should_show_author_pog_for_tagged_media_shared_to_profile_grid: Optional[bool] = (
        Field(
            None,
            description="Should show author POG for tagged media shared to profile grid",
        )
    )
    sponsor_tags: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Sponsor tags"
    )

    # Timeline and pinning
    timeline_pinned_user_ids: Optional[List[str]] = Field(
        default_factory=list, description="Timeline pinned user IDs"
    )

    # Media attributions
    media_attributions_data: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Media attributions data"
    )

    # Creative config
    creative_config: Optional[Dict[str, Any]] = Field(
        None, description="Creative config"
    )

    # Timestamps
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.now, description="Ingestion timestamp"
    )

    @field_validator("taken_at", mode="before")
    @classmethod
    def timestamps_to_datetime(cls, v, info):
        """Convert timestamps to datetime."""
        if isinstance(v, int):
            return datetime.fromtimestamp(v)
        elif isinstance(v, str):
            try:
                return datetime.fromtimestamp(int(v))
            except ValueError:
                raise ValueError(f"Invalid timestamp string: {v}")
        return v

    @classmethod
    def from_api_response_items(
        cls, data: List[Dict[str, Any]], strict=False
    ) -> List["InstagramStoryItem"]:
        """Create a list of InstagramStoryItem from API response data.
        Args:
            data: List of API response data for the stories
            strict: If True, will raise an error if any item is invalid
        """
        items = []
        for item in data:
            try:
                items.append(cls.from_api_response(item))
            except ValidationError as e:
                if strict:
                    raise
                else:
                    # Since we don't have a logger configured in the models,
                    # we'll keep the minimal output but wrap it in a more informative message
                    item_id = item.get("id", "unknown")
                    print(
                        f"Skipping invalid story item (id: {item_id}): {str(e).split('\\n')[0]}"
                    )
                    continue
        return items

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramStoryItem":
        """Create InstagramStoryItem from API response data.

        Args:
            data: API response data for the story
        """

        # Prepare story data by extracting only fields that exist in our model
        story_data = {}

        # Get model fields from the class
        model_fields = cls.model_fields.keys()

        # Extract fields that exist in both the API response and our model
        for field in model_fields:
            if field in data:
                story_data[field] = data[field]

        # Get user core information
        story_data["user"] = (
            InstagramUserCore.model_validate(data.get("user", {}))
            if data.get("user")
            else None
        )
        story_data["owner"] = (
            InstagramUserCore.model_validate(data.get("owner", {}))
            if data.get("owner")
            else None
        )

        # Handle lists that might be None
        list_fields = [
            "media",
            "reel_mentions",
            "tagged_users",
            "cutout_sticker_info",
            "video_sticker_locales",
            "coauthor_producers",
            "invited_coauthor_producers",
            "product_suggestions",
            "sponsor_tags",
            "timeline_pinned_user_ids",
            "media_attributions_data",
        ]
        for field in list_fields:
            if field in story_data and story_data[field] is None:
                story_data[field] = []

        # Handle location
        story_data["location"] = (
            InstagramLocation.model_validate(data.get("location", {}))
            if data.get("location")
            else None
        )

        # Handle media items - using a helper method
        story_data["media"] = cls._build_story_media(data)

        # Handle reshared story media author
        if (
            "reshared_story_media_author" in data
            and data["reshared_story_media_author"]
        ):
            reshared_author_data = data["reshared_story_media_author"]
            story_data["reshared_story_media_author"] = reshared_author_data.get(
                "username", ""
            )

        # Handle reel mentions
        story_data["reel_mentions"] = InstagramStoryMention.from_api_response_items(
            data.get("reel_mentions", [])
        )

        # Set is_video based on media_type for backward compatibility
        story_data["is_video"] = story_data.get("media_type") == 2

        return cls.model_validate(story_data)

    @classmethod
    def _build_story_media(cls, data: Dict[str, Any]) -> InstagramMedia:
        """Extract and build the media object from story data.

        Args:
            data: The story data containing media information

        Returns:
            An InstagramMedia object for the story
        """
        # Determine if this is a video story from top-level fields
        is_video_story = data.get("is_video", False) or data.get("media_type") == 2

        # For single video stories (is_video=True at story level)
        if is_video_story and "video_versions" in data and data["video_versions"]:
            # Create complete media data including video info
            media_data = {
                "media_type": 2,  # Video
                "id": data.get("id", f"vid_{data.get('id', 'unknown')}"),
                "tagged_users": data.get("tagged_users", []),
                "video_versions": data["video_versions"],
                "video_duration": data.get("video_duration"),
                "has_audio": data.get("has_audio"),
                "original_width": data.get("original_width"),
                "original_height": data.get("original_height"),
            }
            return InstagramMedia.from_api_response(media_data)
        # For single image stories (when not a video and has image_versions)
        elif not is_video_story and "image_versions" in data and data["image_versions"]:
            # Create complete media data including image info
            media_data = {
                "media_type": 1,  # Image
                "id": data.get("id", f"img_{data.get('id', 'unknown')}"),
                "tagged_users": data.get("tagged_users", []),
                "image_versions": data["image_versions"],
                "original_width": data.get("original_width"),
                "original_height": data.get("original_height"),
            }
            return InstagramMedia.from_api_response(media_data)
        else:
            # If no media found, create a minimal placeholder media
            return InstagramMedia.model_validate(
                {
                    "media_type": data.get("media_type", 1),
                    "id": data.get("id", "unknown"),
                }
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        return data


class InstagramStory(InstagramBase):
    """A container for Instagram stories, which can include multiple media items."""

    model_type: str = Field(default="story", description="Model type identifier")
    id: str = Field(..., alias="_id", description="Story ID")
    user: InstagramUserCore = Field(..., description="Story author")

    expiring_at: datetime = Field(..., description="Story expiration timestamp")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Story creation timestamp"
    )

    story_items: List[InstagramStoryItem] = Field(
        default_factory=list, description="List of story items"
    )

    @field_validator("expiring_at", "timestamp", mode="before")
    @classmethod
    def convert_timestamps(cls, v):
        """Convert timestamps to datetime."""
        if isinstance(v, int):
            return datetime.fromtimestamp(v)
        elif isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(f"Invalid datetime string: {v}")
        return v

    @classmethod
    def from_api_response(
        cls, data: Dict[str, Any], items_data: List[Dict[str, Any]]
    ) -> "InstagramStory":
        """Create story container and items from API response.

        Args:
            story_data: The story container data (from data.additional_data)
            items_data: The list of story item data (from data.items)
        """
        # Build container data from story_data
        data = data.copy()  # Avoid modifying the original data

        # Extract user information from user info if available
        data["user"] = InstagramUserCore.model_validate(data.get("user", {}))

        # Create story items with proper error handling
        data["story_items"] = InstagramStoryItem.from_api_response_items(items_data)
        return cls.model_validate(data)
