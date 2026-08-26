# tests/test_geo.py

from unittest.mock import patch, MagicMock
from hamcrest import assert_that, is_
from geo import is_valid_us_zip, geocode_zip
from geocoded_zip import GeocodedZip


class IsValidUsZipTests:
    @staticmethod
    def test_zip_not_digits():
        assert_that(is_valid_us_zip("abcde"), is_(False))
        assert_that(is_valid_us_zip("123a5"), is_(False))

    @staticmethod
    def test_zip_has_spaces():
        assert_that(is_valid_us_zip("90 210"), is_(False))

    @staticmethod
    def test_zip_is_empty_string():
        assert_that(is_valid_us_zip(""), is_(False))

    @staticmethod
    def test_zip_too_short():
        assert_that(is_valid_us_zip("123"), is_(False))

    @staticmethod
    def test_zip_too_long():
        assert_that(is_valid_us_zip("123456"), is_(False))

    @staticmethod
    def test_zip_plus_4_not_supported():
        assert_that(is_valid_us_zip("20500+1600"), is_(False))
        assert_that(is_valid_us_zip("20500-1600"), is_(False))

    @staticmethod
    def test_zip_just_right():
        assert_that(is_valid_us_zip("12345"), is_(True))
        assert_that(is_valid_us_zip("90210"), is_(True))
        assert_that(is_valid_us_zip("00000"), is_(True))


class GecodeZipTests:
    @staticmethod
    def test_geocode_zip_invalid_zip():
        assert_that(geocode_zip("abcde"), is_(None))

    @staticmethod
    @patch("geo.requests.get")
    def test_geocode_zip_no_cache_happy_path(mock_get: MagicMock, clean_db):
        # Arrange – fake response from Zippopotam.us
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "post code": "90210",
            "places": [{
                "place name": "Beverly Hills",
                "longitude": "-118.4065",
                "latitude": "34.0901",
                "state abbreviation": "CA"
            }]
        }
        mock_get.return_value = mock_response

        # Act
        data = GeocodedZip(
            zip = "90210",
            latitude = 34.0901,
            longitude = -118.4065,
            city = "Beverly Hills",
            state_abbr = "CA"
        )
        assert_that(geocode_zip("90210"), is_(data))

        mock_get.assert_called_once_with(
            "https://api.zippopotam.us/us/90210",
            timeout=5
        )
