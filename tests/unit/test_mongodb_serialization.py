"""Test MongoDB serialization aliases for all models with id fields."""

import pytest
import json
from datetime import datetime

from src.instagram_schemas.accounts import InstagramUser, InstagramUserCore
from src.instagram_schemas.posts import InstagramPost
from src.instagram_schemas.comments import InstagramComment
from src.instagram_schemas.stories import InstagramStory
from src.instagram_schemas.highlights import InstagramHighlight
from src.instagram_schemas.media import InstagramMedia
from src.instagram_schemas.locations import InstagramLocation


@pytest.mark.mongodb
class TestMongoDBSerialization:
    """Test that id fields are serialized as _id for MongoDB compatibility."""

    def test_user_core_serialization_alias(self):
        """Test InstagramUserCore id field serializes as _id."""
        user = InstagramUserCore(
            _id="123456789", username="testuser", full_name="Test User"
        )
        user_dict = user.model_dump(by_alias=True)

        assert "_id" in user_dict
        assert "id" not in user_dict
        assert user_dict["_id"] == "123456789"

    def test_user_core_validation_then_serialization(self):
        """Test validation with 'id' field then serialization with '_id'."""
        user_data = {"id": "123", "username": "test"}
        user = InstagramUserCore.model_validate(user_data)

        # Internal access still uses 'id'
        assert user.id == "123"

        # Serialization uses '_id'
        serialized = user.model_dump(by_alias=True)
        assert "_id" in serialized
        assert "id" not in serialized
        assert serialized["_id"] == "123"

    def test_instagram_user_serialization_alias(self):
        """Test InstagramUser inherits id serialization from core."""
        # Create minimal InstagramUser instance using model_validate
        user_data = {
            "id": "987654321",
            "username": "instagram_user",
            "full_name": "Real User",
        }
        user = InstagramUser.model_validate(user_data)

        # Serialize for MongoDB
        mongodb_doc = user.model_dump(by_alias=True, exclude_none=True)

        assert "_id" in mongodb_doc
        assert "id" not in mongodb_doc
        assert mongodb_doc["_id"] == "987654321"

    def test_post_serialization_alias(self):
        """Test InstagramPost id serialization via validation."""
        post_data = {
            "id": "post123",
            "code": "ABC123",
            "taken_at": datetime.now().isoformat(),
            "media_type": 1,  # Required field - 1 for image
            "user": {"id": "user123", "username": "poster"},
        }
        post = InstagramPost.model_validate(post_data)

        serialized = post.model_dump(by_alias=True, exclude_none=True)

        assert "_id" in serialized
        assert "id" not in serialized
        assert serialized["_id"] == "post123"

    def test_comment_serialization_alias(self):
        """Test InstagramComment id serialization via validation."""
        comment_data = {
            "id": "comment123",
            "created_at": datetime.now().isoformat(),
            "user": {"id": "user123", "username": "commenter"},
            "text": "Great post!",
            "post_code": "ABC123",  # Required field
        }
        comment = InstagramComment.model_validate(comment_data)

        serialized = comment.model_dump(by_alias=True, exclude_none=True)

        assert "_id" in serialized
        assert "id" not in serialized
        assert serialized["_id"] == "comment123"

    def test_story_serialization_alias(self):
        """Test InstagramStory id serialization via validation."""
        story_data = {
            "id": "story123",
            "user": {"id": "user123", "username": "storyteller"},
            "expiring_at": datetime.now().isoformat(),
        }
        story = InstagramStory.model_validate(story_data)

        serialized = story.model_dump(by_alias=True, exclude_none=True)

        assert "_id" in serialized
        assert "id" not in serialized
        assert serialized["_id"] == "story123"

    def test_highlight_serialization_with_existing_alias(self):
        """Test InstagramHighlight with both alias and serialization_alias."""
        # Test with highlight_id alias (how API provides data)
        highlight_data = {
            "highlight_id": "highlight123",
            "user": {"id": "user123", "username": "highlighter"},
        }
        highlight = InstagramHighlight.model_validate(highlight_data)

        # Internal access uses 'id'
        assert highlight.id == "highlight123"

        # Serialization uses '_id'
        serialized = highlight.model_dump(by_alias=True, exclude_none=True)

        assert "_id" in serialized
        assert "id" not in serialized
        assert "highlight_id" not in serialized  # Replaced by _id
        assert serialized["_id"] == "highlight123"

    def test_media_serialization_alias(self):
        """Test InstagramMedia optional id serialization."""
        media_data = {"id": "media123"}
        media = InstagramMedia.model_validate(media_data)

        serialized = media.model_dump(by_alias=True, exclude_none=True)

        assert "_id" in serialized
        assert "id" not in serialized
        assert serialized["_id"] == "media123"

    def test_location_serialization_alias(self):
        """Test InstagramLocation optional id serialization."""
        location_data = {"name": "Test Location", "id": "location123"}
        location = InstagramLocation.model_validate(location_data)

        serialized = location.model_dump(by_alias=True, exclude_none=True)

        assert "_id" in serialized
        assert "id" not in serialized
        assert serialized["_id"] == "location123"

    def test_nested_id_fields_serialization(self):
        """Test that nested models also get _id serialization."""
        comment_data = {
            "id": "comment123",
            "created_at": datetime.now().isoformat(),
            "user": {"id": "user123", "username": "commenter"},
            "text": "Great post!",
            "post_code": "ABC123",  # Required field
        }
        comment = InstagramComment.model_validate(comment_data)

        serialized = comment.model_dump(by_alias=True, exclude_none=True)

        # Check main object
        assert "_id" in serialized
        assert serialized["_id"] == "comment123"

        # Check nested user object
        assert "user" in serialized
        assert "_id" in serialized["user"]
        assert "id" not in serialized["user"]
        assert serialized["user"]["_id"] == "user123"

    def test_backward_compatibility_validation(self):
        """Test that existing code using 'id' field still works."""
        test_cases = [
            # Direct id field
            {"id": "123", "username": "test"},
            # With existing alias (highlight_id)
            {
                "highlight_id": "highlight123",
                "user": {"id": "user123", "username": "highlighter"},
            },
        ]

        # Test UserCore with id
        user = InstagramUserCore.model_validate(test_cases[0])
        assert user.id == "123"

        # Test Highlight with highlight_id alias
        highlight = InstagramHighlight.model_validate(test_cases[1])
        assert highlight.id == "highlight123"

        # Both should serialize with _id
        user_serialized = user.model_dump(by_alias=True)
        highlight_serialized = highlight.model_dump(by_alias=True, exclude_none=True)

        assert user_serialized["_id"] == "123"
        assert highlight_serialized["_id"] == "highlight123"

    def test_none_id_handling(self):
        """Test that None id values are handled correctly."""
        media_data = {"id": None}
        media = InstagramMedia.model_validate(media_data)

        # Serialize excluding None values
        serialized = media.model_dump(by_alias=True, exclude_none=True)

        # _id should not be present when id is None
        assert "_id" not in serialized
        assert "id" not in serialized
