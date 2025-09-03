"""Integration tests for MongoDB serialization with realistic data patterns."""

import pytest
import json
from datetime import datetime

from src.instagram_schemas.accounts import InstagramUser, InstagramUserCore
from src.instagram_schemas.highlights import InstagramHighlight


@pytest.mark.mongodb
@pytest.mark.integration
class TestMongoDBIntegration:
    """Integration tests demonstrating MongoDB compatibility with realistic scenarios."""

    def test_complete_user_mongodb_workflow(self):
        """Test complete workflow: API data → validation → MongoDB serialization."""
        # Simulate API response data
        api_user_data = {
            "id": "987654321",
            "username": "real_instagram_user",
            "full_name": "Real Instagram User",
            "biography": "Travel photographer 📸",
            "follower_count": 10500,
            "following_count": 892,
            "media_count": 1205,
            "is_verified": True,
            "is_private": False,
        }

        # Step 1: Validate API data
        user = InstagramUser.model_validate(api_user_data)
        assert user.id == "987654321"
        assert user.username == "real_instagram_user"

        # Step 2: Serialize for MongoDB storage
        mongodb_document = user.model_dump(by_alias=True, exclude_none=True)

        # Step 3: Verify MongoDB-ready format
        assert "_id" in mongodb_document
        assert "id" not in mongodb_document
        assert mongodb_document["_id"] == "987654321"
        assert mongodb_document["username"] == "real_instagram_user"
        assert mongodb_document["fullName"] == "Real Instagram User"  # camelCase

        # Step 4: Simulate reading from MongoDB and reconstructing
        # MongoDB would return data with _id, but we need to convert back to id for validation
        mongodb_read_data = mongodb_document.copy()
        mongodb_read_data["id"] = mongodb_read_data.pop("_id")  # Convert _id back to id

        reconstructed_user = InstagramUser.model_validate(mongodb_read_data)
        assert reconstructed_user.id == user.id
        assert reconstructed_user.username == user.username

    def test_highlight_with_alias_mongodb_workflow(self):
        """Test highlight workflow with existing highlight_id alias."""
        # API data uses highlight_id
        api_highlight_data = {
            "highlight_id": "highlight_travel_2024",
            "user": {
                "id": "user123456",
                "username": "travel_blogger",
                "full_name": "Travel Blogger",
            },
            "title": "Best of 2024 🌍",
            "created_at": "2024-12-01T15:30:00Z",
            "media_count": 12,
        }

        # Validate from API
        highlight = InstagramHighlight.model_validate(api_highlight_data)
        assert highlight.id == "highlight_travel_2024"

        # Serialize for MongoDB
        mongodb_doc = highlight.model_dump(by_alias=True, exclude_none=True)

        # Check MongoDB format
        assert "_id" in mongodb_doc
        assert "id" not in mongodb_doc
        assert "highlight_id" not in mongodb_doc  # Should be replaced by _id
        assert mongodb_doc["_id"] == "highlight_travel_2024"

        # Nested user should also have _id
        assert "_id" in mongodb_doc["user"]
        assert "id" not in mongodb_doc["user"]
        assert mongodb_doc["user"]["_id"] == "user123456"

    def test_batch_processing_mongodb_serialization(self):
        """Test processing multiple models for bulk MongoDB insertion."""
        # Simulate batch of user data from API
        api_users = [
            {"id": "user001", "username": "user1", "full_name": "User One"},
            {"id": "user002", "username": "user2", "full_name": "User Two"},
            {"id": "user003", "username": "user3", "full_name": "User Three"},
        ]

        # Process for MongoDB bulk insert
        mongodb_documents = []
        for user_data in api_users:
            user = InstagramUserCore.model_validate(user_data)
            mongodb_doc = user.model_dump(by_alias=True, exclude_none=True)
            mongodb_documents.append(mongodb_doc)

        # Verify all documents are MongoDB-ready
        for i, doc in enumerate(mongodb_documents):
            assert "_id" in doc
            assert "id" not in doc
            assert doc["_id"] == f"user00{i+1}"
            assert doc["username"] == f"user{i+1}"

        # Verify we can reconstruct from MongoDB format
        reconstructed_users = []
        for doc in mongodb_documents:
            # Convert _id back to id for validation
            api_format = doc.copy()
            api_format["id"] = api_format.pop("_id")
            user = InstagramUserCore.model_validate(api_format)
            reconstructed_users.append(user)

        assert len(reconstructed_users) == 3
        assert all(user.id.startswith("user00") for user in reconstructed_users)

    def test_mongodb_query_compatibility(self):
        """Test that serialized data is compatible with MongoDB query patterns."""
        user_data = {
            "id": "query_test_user",
            "username": "queryable_user",
            "full_name": "Queryable User",
        }

        user = InstagramUserCore.model_validate(user_data)
        mongodb_doc = user.model_dump(by_alias=True)

        # Simulate MongoDB queries would work on this document
        # MongoDB typically queries by _id
        assert mongodb_doc["_id"] == "query_test_user"

        # Verify field names match MongoDB/camelCase conventions
        assert "fullName" in mongodb_doc  # camelCase for frontend compatibility
        assert "username" in mongodb_doc  # snake_case preserved where appropriate

        # This document structure would work with queries like:
        # db.users.find({"_id": "query_test_user"})
        # db.users.find({"username": "queryable_user"})
        # db.users.find({"fullName": "Queryable User"})

    def test_error_handling_with_mongodb_serialization(self):
        """Test error scenarios don't break MongoDB serialization."""
        # Test with minimal required data
        minimal_user_data = {"id": "minimal_user", "username": "minimal"}
        user = InstagramUserCore.model_validate(minimal_user_data)

        # Should still serialize correctly even with minimal data
        mongodb_doc = user.model_dump(by_alias=True, exclude_none=True)
        assert "_id" in mongodb_doc
        assert mongodb_doc["_id"] == "minimal_user"
        assert mongodb_doc["username"] == "minimal"

        # fullName should get default empty string
        assert mongodb_doc.get("fullName") == ""

    def test_timestamp_fields_mongodb_compatibility(self):
        """Test that timestamp fields work correctly with MongoDB."""
        current_time = datetime.now()
        user_data = {
            "id": "timestamp_user",
            "username": "timeuser",
            "full_name": "Time User",
        }

        user = InstagramUser.model_validate(user_data)
        mongodb_doc = user.model_dump(by_alias=True, exclude_none=True)

        # updated_at should be present (has default_factory)
        assert "updatedAt" in mongodb_doc  # camelCase

        # Should be a datetime that can be stored in MongoDB
        # MongoDB stores datetime objects natively
        assert isinstance(user.updated_at, datetime)
