import json
import os
import pytest

from instagram_schemas import (
    InstagramUser,
    InstagramPost,
    InstagramStory,
    InstagramStoryItem,
    InstagramHighlight,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)


def _load_json(path):
    with open(path, "r") as f:
        return json.load(f)


@pytest.mark.integration
def test_users_from_real_data():
    path = os.path.join(DATA_DIR, "instagram_user_data.json")
    data = _load_json(path)
    assert isinstance(data, list) and len(data) > 0

    parsed = []
    for raw in data:
        try:
            user = InstagramUser.from_api_response(raw)
            parsed.append(user)
        except Exception:
            # Skip malformed entries
            continue

    assert len(parsed) > 0
    # Spot-check a known account like 'instagram' is present
    assert any(u.username.lower() == "instagram" for u in parsed if u.username)


@pytest.mark.integration
def test_posts_from_real_data():
    path = os.path.join(DATA_DIR, "instagram_user_media.json")
    # media list contains posts entries in this dataset
    media_list = _load_json(path)
    assert isinstance(media_list, list) and len(media_list) > 0

    parsed_posts = []
    for raw in media_list:
        try:
            # The dataset is mixed; some items are in a post-like shape already
            # Ensure required fields exist or derive minimal ones
            raw.setdefault("id", str(raw.get("pk", "")))
            raw.setdefault("code", raw.get("code", str(raw.get("pk", ""))))
            # The API data often includes user under caption.user or top-level user
            if "user" not in raw:
                caption_user = ((raw.get("caption") or {}) or {}).get("user") or {}
                if caption_user:
                    raw["user"] = caption_user
            # Ensure media_type
            raw.setdefault("media_type", 2 if raw.get("video_versions") else 1)
            # taken_at
            raw.setdefault("taken_at", raw.get("device_timestamp", raw.get("taken_at")))

            post = InstagramPost.from_api_response(raw)
            parsed_posts.append(post)
        except Exception:
            continue

    assert len(parsed_posts) > 0
    # Make sure we parsed media
    assert any(len(p.media) > 0 for p in parsed_posts)


@pytest.mark.integration
def test_post_details_from_real_data():
    path = os.path.join(DATA_DIR, "instagram_user_post_details.json")
    details = _load_json(path)
    assert isinstance(details, list) and len(details) > 0

    parsed_posts = []
    for raw in details:
        try:
            raw.setdefault("id", str(raw.get("pk", "")))
            raw.setdefault("code", raw.get("code", str(raw.get("pk", ""))))
            if "user" not in raw:
                caption_user = ((raw.get("caption") or {}) or {}).get("user") or {}
                if caption_user:
                    raw["user"] = caption_user
            raw.setdefault("media_type", 2 if raw.get("video_versions") else 1)
            raw.setdefault("taken_at", raw.get("device_timestamp", raw.get("taken_at")))
            post = InstagramPost.from_api_response(raw)
            parsed_posts.append(post)
        except Exception:
            continue

    assert len(parsed_posts) > 0


@pytest.mark.integration
def test_stories_from_real_data():
    path = os.path.join(DATA_DIR, "instagram_user_stories.json")
    stories = _load_json(path)
    assert isinstance(stories, list) and len(stories) > 0

    # Build a container per story item with minimal required fields
    parsed_items = []
    for raw in stories:
        try:
            # Build a story item directly
            raw.setdefault("id", str(raw.get("pk", "")))
            raw.setdefault("code", raw.get("code", str(raw.get("pk", ""))))
            raw.setdefault("media_type", 2 if raw.get("video_versions") else 1)
            raw.setdefault(
                "taken_at", raw.get("device_timestamp", raw.get("taken_at", 0))
            )
            # Map user
            if (
                "user" not in raw
                and "caption" in raw
                and raw["caption"]
                and "user" in raw["caption"]
            ):
                raw["user"] = raw["caption"]["user"]
            item = InstagramStoryItem.from_api_response(raw)
            parsed_items.append(item)
        except Exception:
            continue

    assert len(parsed_items) > 0


@pytest.mark.integration
def test_highlights_from_real_data():
    path = os.path.join(DATA_DIR, "instagram_user_highlights.json")
    highlights = _load_json(path)
    assert isinstance(highlights, list) and len(highlights) > 0

    parsed = []
    for raw in highlights:
        try:
            # Normalize id field
            if (
                "id" in raw
                and isinstance(raw["id"], str)
                and raw["id"].startswith("highlight:")
            ):
                raw["highlight_id"] = raw.pop("id")
            # Ensure user exists
            if "user" not in raw:
                continue
            hl = InstagramHighlight.from_api_response(raw)
            parsed.append(hl)
        except Exception:
            continue

    assert len(parsed) > 0
