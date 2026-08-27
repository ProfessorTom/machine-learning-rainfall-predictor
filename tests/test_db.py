from hamcrest import assert_that, is_

from db import save_location, get_cached_location
from entities import GeocodedZip


class GetCachedLocationTests:

    @staticmethod
    def test_returns_none_when_not_found(clean_db):
        result = get_cached_location("90210 ")
        assert result is None

    @staticmethod
    def test_returns_location_when_found(clean_db):
        # Arrange – use the real save function
        original = GeocodedZip(
            zip="90210",
            latitude=34.0901,
            longitude=-118.4065,
            city="Beverly Hills",
            state_abbr="CA"
        )
        save_location(original)

        # Act
        result = get_cached_location("90210")

        # Assert
        assert_that(result, is_(original))
