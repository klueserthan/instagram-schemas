from instagram_schemas.highlights import InstagramHighlight
from instagram_schemas.stories import InstagramStoryItem


def test_highlight_from_api_response_and_add_story(sample_highlight, sample_story_item):
    hl = InstagramHighlight.from_api_response(sample_highlight)
    assert hl.id == "h1"
    assert hl.user.username == "testuser"
    assert hl.story_count() == 0

    item = InstagramStoryItem.from_api_response(sample_story_item)
    hl.add_story(item)
    assert hl.story_count() == 1
    assert hl.has_stories() is True


def test_highlight_validators_and_to_dict(sample_highlight):
    payload = {**sample_highlight, "highlight_id": "highlight:h2"}
    hl = InstagramHighlight.from_api_response(payload)
    assert hl.id == "h2"
    out = hl.to_dict()
    assert "createdAt" in out


def test_highlight_add_stories(sample_highlight, sample_story_item):
    hl = InstagramHighlight.from_api_response(sample_highlight)
    items = [InstagramStoryItem.from_api_response(sample_story_item)]
    hl.add_stories(items)
    assert hl.story_count() == 1


def test_highlight_defaults_and_created_at_int(sample_user_core):
    payload = {
        "highlight_id": "h3",
        "user": sample_user_core,
        "created_at": 0,
    }
    hl = InstagramHighlight.from_api_response(payload)
    assert hl.title is None and hl.media_count is None
    assert hl.created_at is not None and hl.created_at.year == 1970


def test_highlight_add_story_type_error(sample_highlight):
    hl = InstagramHighlight.from_api_response(sample_highlight)
    try:
        hl.add_story("not-a-story")  # type: ignore[arg-type]
        assert False, "Expected TypeError"
    except TypeError:
        assert True
