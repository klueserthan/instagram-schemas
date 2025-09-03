import pytest
from datetime import datetime, timedelta
from instagram_schemas.accounts import (
    InstagramUserCore,
    InstagramUser,
    InstagramUserMetrics,
)


def test_user_core_validation_success(sample_user_core):
    user = InstagramUserCore.model_validate(sample_user_core)
    assert user.id == "123"
    assert user.username == "testuser"
    assert user.full_name == "Test User"


def test_user_core_validation_failure_empty_username(sample_user_core):
    bad = {**sample_user_core, "username": ""}
    with pytest.raises(Exception):
        InstagramUserCore.model_validate(bad)


def test_user_metrics_parsing_from_strings():
    metrics = InstagramUserMetrics.model_validate(
        {
            "follower_count": "100",
            "following_count": "50",
            "media_count": "10",
            "total_igtv_videos": "2",
        }
    )
    assert metrics.follower_count == 100
    assert metrics.following_count == 50
    assert metrics.media_count == 10
    assert metrics.total_igtv_videos == 2


def test_user_from_api_response_builds_metrics(sample_user_core):
    payload = {
        **sample_user_core,
        "follower_count": 10,
        "following_count": 5,
        "media_count": 2,
    }
    user = InstagramUser.from_api_response(payload)
    assert isinstance(user, InstagramUser)
    assert len(user.metrics) == 1
    latest = user.get_latest_metrics()
    assert latest is not None and latest.follower_count == 10


def test_user_metrics_history_sorted():
    now = datetime.now()
    m1 = InstagramUserMetrics(
        follower_count=1,
        following_count=1,
        media_count=1,
        updated_at=now - timedelta(days=1),
    )
    m2 = InstagramUserMetrics(
        follower_count=2, following_count=2, media_count=2, updated_at=now
    )
    user = InstagramUser.model_validate(
        {
            "id": "1",
            "username": "u",
            "full_name": "U",
            "metrics": [m2, m1],
        }
    )
    history = user.get_metrics_history()
    assert [m.updated_at for m in history] == [m1.updated_at, m2.updated_at]


def test_user_core_from_api_response(sample_user_core):
    user = InstagramUserCore.from_api_response(sample_user_core)
    assert user.username == "testuser"


def test_user_core_id_not_null():
    with pytest.raises(Exception):
        InstagramUserCore.model_validate({"id": None, "username": "x", "full_name": ""})


def test_instagram_user_boolean_and_fbid_v2_parsing(sample_user_core):
    data = {
        **sample_user_core,
        "is_verified": "True",
        "is_private": "0",
        "is_business": 1,
        "fbid_v2": 12345,
        "follower_count": 1,
        "following_count": 1,
        "media_count": 1,
    }
    user = InstagramUser.from_api_response(data)
    assert user.is_verified is True
    assert user.is_private is False
    assert user.is_business is True
    assert user.fbid_v2 == "12345"


def test_instagram_user_from_api_response_about_section_and_list_defaults(
    sample_user_core,
):
    data = {
        **sample_user_core,
        "about": {"country": "DE", "date_joined": "Jan 2020"},
        "hd_profile_pic_versions": None,
        "follower_count": 0,
        "following_count": 0,
        "media_count": 0,
    }
    user = InstagramUser.from_api_response(data)
    assert user.country == "DE"
    assert user.date_joined == "Jan 2020"
    assert user.hd_profile_pic_versions == []


def test_instagram_user_metrics_failure_leads_to_empty_metrics(sample_user_core):
    data = {
        **sample_user_core,
        "follower_count": "nope",  # invalid -> metrics creation fails
        "following_count": 1,
        "media_count": 1,
    }
    user = InstagramUser.from_api_response(data)
    assert user.metrics == []
    assert user.follower_count is None  # property reads from latest metrics


def test_instagram_user_to_dict_uses_aliases():
    user = InstagramUser.model_validate(
        {"id": "1", "username": "u", "full_name": "Full"}
    )
    out = user.to_dict()
    # full_name should be serialized as fullName
    assert "fullName" in out
