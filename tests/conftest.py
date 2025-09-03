import pytest
from datetime import datetime, timedelta


@pytest.fixture
def now():
    return datetime.now()


@pytest.fixture
def sample_user_core():
    return {
        "id": "123",
        "username": "testuser",
        "full_name": "Test User",
    }


@pytest.fixture
def sample_user_metrics(now):
    return {
        "follower_count": 100,
        "following_count": 50,
        "media_count": 10,
        "total_igtv_videos": 2,
        "updated_at": now,
    }


@pytest.fixture
def sample_post_metrics(now):
    return {
        "like_count": 10,
        "comment_count": 2,
        "view_count": 100,
        "play_count": 90,
        "fb_like_count": 1,
        "fb_play_count": 3,
        "updated_at": now,
    }


@pytest.fixture
def sample_media_image():
    return {
        "id": "m1",
        "media_type": 1,
        "original_width": 1080,
        "original_height": 1350,
        "image_versions": [
            {"url": "https://img/1.jpg", "width": 1080, "height": 1350},
            {"url": "https://img/1_sm.jpg", "width": 640, "height": 800},
        ],
        "tagged_users": [
            {
                "x": 0.4,
                "y": 0.6,
                "user": {"id": "u2", "username": "alice", "full_name": "Alice"},
            }
        ],
    }


@pytest.fixture
def sample_media_video():
    return {
        "id": "v1",
        "media_type": 2,
        "original_width": 1080,
        "original_height": 1920,
        "video_versions": [{"url": "https://vid/1.mp4", "width": 1080, "height": 1920}],
        "video_duration": 12.3,
        "has_audio": True,
    }


@pytest.fixture
def sample_post(sample_user_core, sample_media_image, sample_post_metrics):
    return {
        "id": "p1",
        "code": "ABC123",
        "taken_at": int(datetime.now().timestamp()),
        "media_type": 1,
        "user": sample_user_core,
        "media": [],
        "metrics": sample_post_metrics,
        "image_versions": sample_media_image["image_versions"],
        "original_width": sample_media_image["original_width"],
        "original_height": sample_media_image["original_height"],
    }


@pytest.fixture
def sample_story_item(sample_user_core, sample_media_image):
    return {
        "id": "s1",
        "code": "ST1",
        "taken_at": int(datetime.now().timestamp()),
        "media_type": 1,
        "user": sample_user_core,
        "image_versions": sample_media_image["image_versions"],
        "original_width": sample_media_image["original_width"],
        "original_height": sample_media_image["original_height"],
    }


@pytest.fixture
def sample_comment(sample_user_core):
    return {
        "id": "c1",
        "created_at": int(datetime.now().timestamp()),
        "user": sample_user_core,
        "text": "Nice post!",
        "comment_like_count": 5,
        "child_comment_count": 2,
    }


@pytest.fixture
def sample_highlight(sample_user_core):
    return {
        "highlight_id": "h1",
        "user": sample_user_core,
        "title": "Highlights",
        "created_at": int(datetime.now().timestamp()),
        "media_count": 3,
    }
