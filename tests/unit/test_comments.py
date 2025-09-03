from instagram_schemas.comments import InstagramComment, InstagramCommentReply
from instagram_schemas.accounts import InstagramUserCore
import pytest


def test_comment_from_api_response_builds_reply_count_and_like_count(sample_comment):
    comment = InstagramComment.from_api_response(sample_comment, post_code="ABC123")
    assert comment.post_code == "ABC123"
    assert comment.replies_count == 2
    assert comment.like_count == 5
    assert comment.user.username == "testuser"


def test_reply_from_api_response_maps_like_count(sample_comment):
    # Use same payload to simulate a reply
    reply = InstagramCommentReply.from_api_response(sample_comment)
    assert reply.like_count == 5
    assert reply.text == "Nice post!"


def test_comment_none_lists_become_empty(sample_comment):
    payload = {**sample_comment, "mentions": None, "hashtags": None}
    comment = InstagramComment.from_api_response(payload, post_code="X")
    assert comment.mentions == [] and comment.hashtags == []


def test_comment_timestamp_int_parsed(sample_comment):
    comment = InstagramComment.from_api_response(sample_comment, post_code="Y")
    assert comment.created_at.year >= 1970


def test_comment_to_dict_aliases(sample_comment):
    comment = InstagramComment.from_api_response(sample_comment, post_code="Z")
    out = comment.to_dict()
    # created_at should be serialized as createdAt via to_camel
    assert "createdAt" in out


def test_comment_invalid_datetime_raises(sample_user_core):
    bad = {
        "id": "c2",
        "created_at": "not-a-date",
        "user": sample_user_core,
        "text": "t",
        "post_code": "P",
    }
    with pytest.raises(Exception):
        InstagramComment.model_validate(bad)


def test_reply_none_lists_to_empty(sample_comment):
    payload = {**sample_comment, "mentions": None, "hashtags": None}
    reply = InstagramCommentReply.from_api_response(payload)
    assert reply.mentions == [] and reply.hashtags == []
