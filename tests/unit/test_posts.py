from instagram_schemas.posts import InstagramPost, InstagramPostMetrics
import pytest


def test_post_from_api_response_builds_metrics_and_user(sample_post):
    post = InstagramPost.from_api_response(sample_post)
    assert post.id == "p1"
    assert post.code == "ABC123"
    assert post.user.username == "testuser"
    # Metrics provided in payload should be collected
    assert len(post.metrics) == 1
    assert post.like_count == 10


def test_post_media_built_from_top_level_image_fields(sample_post):
    post = InstagramPost.from_api_response(sample_post)
    assert post.media and post.media[0].media_type == 1
    assert post.media[0].original_width == 1080


def test_post_carousel_items_build_media(sample_post):
    payload = {
        **sample_post,
        "carousel_media": [
            {
                "id": "c1",
                "media_type": 1,
                "image_versions": sample_post["image_versions"],
            },
            {
                "id": "c2",
                "media_type": 2,
                "video_versions": [{"url": "https://vid/2.mp4"}],
            },
        ],
    }
    post = InstagramPost.from_api_response(payload)
    # Expect media for top-level and carousel items (3 total)
    assert len(post.media) == 3


def test_post_caption_and_location_and_properties(sample_post):
    payload = {
        **sample_post,
        "caption": {"text": "Hello", "created_at": sample_post["taken_at"]},
        "location": {"id": "loc", "name": "Place"},
        "metrics": {"like_count": "7", "comment_count": "1"},
    }
    post = InstagramPost.from_api_response(payload)
    assert post.caption and post.caption.text == "Hello"
    assert post.location and post.location.name == "Place"
    assert post.like_count == 7 and post.comment_count == 1


def test_post_to_dict_aliases(sample_post):
    post = InstagramPost.from_api_response(sample_post)
    out = post.to_dict()
    assert "takenAt" in out


def test_post_invalid_timestamp_string_raises(sample_post):
    payload = {**sample_post, "taken_at": "not-a-date"}
    with pytest.raises(Exception):
        InstagramPost.from_api_response(payload)


def test_post_gen_ai_detection_passthrough(sample_post):
    payload = {**sample_post, "gen_ai_detection_method": {"k": "v"}}
    post = InstagramPost.from_api_response(payload)
    assert post.gen_ai_detection_method == {"k": "v"}


def test_post_is_video_derivation(sample_post):
    payload = {
        **sample_post,
        "media_type": 2,
        "video_versions": [{"url": "https://vid/1.mp4"}],
        "is_video": True,
    }
    post = InstagramPost.from_api_response(payload)
    assert post.is_video is True and post.media[0].media_type == 2


def test_post_metrics_malformed_ignored(sample_post):
    payload = {**sample_post, "metrics": {"like_count": "x"}}
    post = InstagramPost.from_api_response(payload)
    # metrics parsing tries to coerce; bad values -> None inside but object still created
    assert len(post.metrics) == 1


def test_post_list_fields_replace_none(sample_post):
    payload = {
        **sample_post,
        "preview_comments": None,
        "tagged_users": None,
        "coauthor_producers": None,
    }
    post = InstagramPost.from_api_response(payload)
    assert post.preview_comments == []


def test_post_populate_taken_at_date(sample_post):
    post = InstagramPost.from_api_response(sample_post)
    assert post.taken_at_date == post.taken_at


def test_post_caption_created_at_utc_iso(sample_post):
    payload = {
        **sample_post,
        "caption": {"text": "t", "created_at_utc": "2024-01-02T03:04:05"},
    }
    post = InstagramPost.from_api_response(payload)
    assert (
        post.caption
        and post.caption.created_at_utc
        and post.caption.created_at_utc.year == 2024
    )


def test_post_caption_invalid_created_at_string(sample_post):
    payload = {**sample_post, "caption": {"text": "t", "created_at": "oops"}}
    post = InstagramPost.from_api_response(payload)
    assert post.caption and post.caption.created_at is None


def test_post_metrics_properties_latest(
    sample_user_metrics, sample_user_core, sample_media_image
):
    from instagram_schemas.posts import InstagramPostMetrics
    import datetime

    m1 = InstagramPostMetrics(
        like_count=1,
        comment_count=1,
        updated_at=datetime.datetime.now() - datetime.timedelta(days=1),
    )
    m2 = InstagramPostMetrics(
        like_count=2, comment_count=2, updated_at=datetime.datetime.now()
    )
    payload = {
        "id": "p2",
        "code": "C",
        "taken_at": int(datetime.datetime.now().timestamp()),
        "media_type": 1,
        "user": sample_user_core,
        "image_versions": sample_media_image["image_versions"],
        "original_width": sample_media_image["original_width"],
        "original_height": sample_media_image["original_height"],
    }
    post = InstagramPost.from_api_response(payload)
    post.metrics = [m1, m2]
    assert post.like_count == 2 and post.comment_count == 2
