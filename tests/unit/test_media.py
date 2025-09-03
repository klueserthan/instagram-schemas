from instagram_schemas.media import InstagramMedia, TaggedUser


def test_media_from_api_response_builds_image_versions(sample_media_image):
    media = InstagramMedia.from_api_response(sample_media_image)
    assert media.media_type == 1
    assert media.image_versions is not None and len(media.image_versions) == 2
    assert media.original_width == 1080


def test_media_from_api_response_builds_video_versions(sample_media_video):
    media = InstagramMedia.from_api_response(sample_media_video)
    assert media.media_type == 2
    assert media.has_audio is True
    assert media.video_versions and media.video_versions[0].url.endswith(".mp4")


def test_media_from_api_response_with_carousel_items(sample_media_image):
    payload = {
        **sample_media_image,
        "carousel_media": [
            {
                "id": "i1",
                "media_type": 1,
                "image_versions": sample_media_image["image_versions"],
            },
            {
                "id": "v2",
                "media_type": 2,
                "video_versions": [{"url": "https://vid/3.mp4"}],
            },
        ],
        "carousel_media_count": 2,
    }
    media = InstagramMedia.from_api_response(payload)
    assert media.carousel_media is not None and len(media.carousel_media) == 2


def test_media_to_dict_has_aliases(sample_media_image):
    media = InstagramMedia.from_api_response(sample_media_image)
    out = media.to_dict()
    assert "mediaType" in out


def test_tagged_user_from_api_response_with_position_array():
    payload = {
        "position": [0.1, 0.2],
        "user": {"id": "u1", "username": "bob", "full_name": "Bob"},
    }
    tagged = TaggedUser.from_api_response(payload)
    assert tagged.x == 0.1 and tagged.y == 0.2
    assert tagged.username == "bob"
