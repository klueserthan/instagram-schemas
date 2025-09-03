"""Instagram comments models."""

from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import (
    Field,
    ConfigDict,
    field_validator,
)
from pydantic.alias_generators import to_camel

from .accounts import InstagramUserCore
from .base import InstagramBase


class Comment(InstagramBase):
    """Base comment model."""

    id: str = Field(..., alias="_id", description="Comment ID")
    created_at: datetime = Field(..., description="Comment creation datetime")
    user: InstagramUserCore = Field(..., description="Comment author user")
    text: str = Field(..., description="Comment text")

    like_count: Optional[int] = Field(None, description="Number of likes on comment")
    hashtags: List[str] = Field(default_factory=list, description="Hashtags in reply")
    mentions: List[str] = Field(
        default_factory=list, description="Mentioned users in reply"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Processing timestamp"
    )

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


class InstagramCommentReply(Comment):
    """Instagram comment reply model."""

    pass

    @field_validator("mentions", "hashtags", mode="before")
    @classmethod
    def replace_none_with_empty_list(cls, value, info):
        if value is None:
            return []
        return value

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "InstagramCommentReply":
        """Create InstagramCommentReply from API response data."""
        # Prepare reply data
        reply_data = data.copy()
        # Convert created_at timestamp to datetime
        if "created_at" in reply_data:
            timestamp = reply_data["created_at"]
            if isinstance(timestamp, int):
                reply_data["created_at"] = datetime.fromtimestamp(timestamp)

        # Set default values for required fields if missing
        reply_data.setdefault("text", "")

        # Map comment_like_count to like_count
        if "comment_like_count" in reply_data:
            reply_data["like_count"] = reply_data.pop("comment_like_count")

        # Extract username from nested user object if present
        reply_data["user"] = InstagramUserCore.model_validate(
            reply_data.get("user", {})
        )

        return cls.model_validate(reply_data)


class InstagramComment(Comment):
    """Instagram comment model."""

    post_code: str = Field(..., description="Post code this comment belongs to")
    did_report_as_spam: Optional[bool] = Field(
        None, description="Whether comment was reported as spam"
    )
    replies_count: Optional[int] = Field(
        None, description="Number of replies to this comment"
    )
    replies: List[InstagramCommentReply] = Field(
        default_factory=list, description="Comment replies"
    )

    @field_validator("mentions", "hashtags", "replies", mode="before")
    @classmethod
    def replace_none_with_empty_list(cls, value, info):
        if value is None:
            return []
        return value

    @classmethod
    def from_api_response(
        cls, data: Dict[str, Any], post_code: str
    ) -> "InstagramComment":
        """Create InstagramComment from API response data.

        Args:
            data: API response data for the comment
            post_id: ID of the post this comment belongs to
        """
        # Prepare comment data
        comment_data = data.copy()
        comment_data["post_code"] = post_code

        # set replies_count
        comment_data["replies_count"] = comment_data.get("child_comment_count", 0)

        # Set default values for required fields if missing
        comment_data.setdefault("text", "")

        # Map comment_like_count to like_count
        if "comment_like_count" in comment_data:
            comment_data["like_count"] = comment_data.pop("comment_like_count")

        # Extract username from nested user object if present
        comment_data["user"] = InstagramUserCore.model_validate(
            comment_data.get("user", {})
        )

        return cls.model_validate(comment_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return self.model_dump(by_alias=True, exclude_none=True)
