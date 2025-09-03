from instagram_schemas.stories import (
    InstagramStoryItem,
    InstagramStory,
    InstagramStoryMention,
)


def test_story_item_from_api_response_builds_media_and_user(sample_story_item):
    item = InstagramStoryItem.from_api_response(sample_story_item)
    assert item.id == "s1"
    assert item.user is not None and item.user.username == "testuser"
    assert item.media.media_type == 1


def test_story_item_mentions_from_api_response_items(sample_user_core):
    data = [
        {"user": sample_user_core, "x": 0.1, "y": 0.2},
        {"user": {"id": "", "username": ""}},  # invalid -> skipped
    ]
    mentions = InstagramStoryMention.from_api_response_items(data)
    assert len(mentions) == 1


def test_story_container_from_api_response_builds_items(
    sample_user_core, sample_story_item
):
    container = {
        "id": "story_1",
        "user": sample_user_core,
        "expiring_at": sample_story_item["taken_at"],
    }
    story = InstagramStory.from_api_response(container, [sample_story_item])
    assert story.id == "story_1"
    assert story.user.username == "testuser"
    assert len(story.story_items) == 1


def test_story_mention_bools_from_int(sample_user_core):
    m = InstagramStoryMention.from_api_response(
        {
            "user": sample_user_core,
            "is_pinned": 1,
            "is_hidden": 0,
        }
    )
    assert m.is_pinned is True and m.is_hidden is False


def test_story_item_placeholder_media_when_missing_required(sample_user_core):
    payload = {
        "id": "s2",
        "code": "S2",
        "taken_at": sample_user_core.get("id", 0),
        "media_type": 1,
    }
    # minimal; media/image_versions missing -> placeholder media
    item = InstagramStoryItem.from_api_response(payload)
    assert item.media.id == "s2"


def test_story_item_to_dict_has_aliases(sample_story_item):
    item = InstagramStoryItem.from_api_response(sample_story_item)
    out = item.to_dict()
    assert "takenAt" in out
