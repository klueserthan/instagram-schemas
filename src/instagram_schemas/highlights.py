"""Instagram highlights models."""

from datetime import datetime
from typing import Optional, List, Any, Dict, Sequence
from typing_extensions import Self
from pydantic import Field, field_validator, AliasChoices
from pydantic.alias_generators import to_camel

from .stories import InstagramStoryItem
from .accounts import InstagramUserCore
from .base import InstagramBase


class InstagramHighlight(InstagramBase):
    """Instagram highlight model - a collection of saved stories."""

    # Core fields
    model_type: str = Field(default="highlight", description="Model type identifier")
    id: str = Field(
        ...,
        validation_alias=AliasChoices("highlight_id", "_id", "id"),
        description="Highlight ID",
    )
    user: InstagramUserCore = Field(..., description="Username of the highlight owner")

    title: Optional[str] = Field(None, description="Highlight title")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    media_count: Optional[int] = Field(
        None, description="Number of stories in this highlight"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Ingestion timestamp"
    )

    # Stories in this highlight (populated separately via get_highlight method)
    story_items: List[InstagramStoryItem] = Field(
        default_factory=list, description="Stories in the highlight"
    )

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, value: Any, info) -> str:
        if isinstance(value, str) and value.startswith("highlight:"):
            value = value.removeprefix("highlight:")
        if not value:
            raise ValueError("Highlight ID cannot be empty")
        return str(value)

    @field_validator("created_at", mode="before")
    @classmethod
    def convert_timestamps(cls, v, info):
        """Convert timestamp to datetime."""
        if isinstance(v, int):
            return datetime.fromtimestamp(v)
        elif isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(f"Invalid datetime string: {v}")
        return v

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramHighlight":
        """Create InstagramHighlight from API response data.

        The API response structure has highlight metadata in 'additional_data'
        and individual stories in 'items' array.
        """

        payload = data.copy()

        # Extract user information
        payload["user"] = InstagramUserCore.model_validate(data.get("user", {}))

        return cls.model_validate(payload)

    def add_story(self, story: InstagramStoryItem) -> None:
        """Add a story to the highlight."""
        if not isinstance(story, InstagramStoryItem):
            raise TypeError("Expected an instance of InstagramStoryItem")
        self.story_items.append(story)

    def add_stories(self, stories: List[InstagramStoryItem]) -> None:
        """Add multiple stories to the highlight."""
        for story in stories:
            self.add_story(story)

    def story_count(self) -> int:
        """Get the number of stories in this highlight."""
        return len(self.story_items)

    def has_stories(self) -> bool:
        """Check if this highlight has any stories."""
        return len(self.story_items) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return self.model_dump(by_alias=True, exclude_none=True)
