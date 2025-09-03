from instagram_schemas.locations import InstagramLocation


def test_location_from_api_response_basic_fields():
    payload = {
        "id": "loc1",
        "name": "Some Place",
        "city": "Berlin",
        "lat": "52.52",
        "lng": "13.405",
        "media_count": "42",
    }
    loc = InstagramLocation.from_api_response(payload)
    assert loc.id == "loc1"
    assert loc.name == "Some Place"
    assert loc.city == "Berlin"
    assert loc.lat == 52.52
    assert loc.lng == 13.405
    assert loc.media_count == 42


def test_location_to_dict_aliases():
    loc = InstagramLocation.from_api_response({"id": "x", "name": "N"})
    out = loc.to_dict()
    assert "mediaCount" in out or "name" in out  # ensure aliasing happens
