from datetime import date

from hamcrest import assert_that, is_, has_length, empty

from db import save_location, get_cached_location, save_historical_data, get_historical_data
from entities import GeocodedZip, HistoricalDay


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


SAMPLE_DAYS = [
    HistoricalDay(
        date=date(2024, 1, 1),
        temp_max=18.5,
        temp_min=8.2,
        precipitation=0.0,
    ),
    HistoricalDay(
        date=date(2024, 1, 2),
        temp_max=20.1,
        temp_min=9.0,
        precipitation=2.3,
    ),
    HistoricalDay(
        date=date(2024, 1, 3),
        temp_max=17.0,
        temp_min=7.5,
        precipitation=1.1,
    ),
]

class GetHistoricalDataTests:

    @staticmethod
    def test_returns_empty_list_when_not_found(clean_db):
        result = get_historical_data("90210")
        assert_that(result, has_length(0))

    @staticmethod
    def test_returns_saved_days(clean_db):
        save_historical_data("90210", SAMPLE_DAYS)

        result = get_historical_data("90210")

        assert_that(result, is_(SAMPLE_DAYS))

    @staticmethod
    def test_filters_by_date_range(clean_db):
        save_historical_data("90210", SAMPLE_DAYS)

        result = get_historical_data(
            "90210",
            start_date=date(2024, 1, 2),
            end_date=date(2024, 1, 2),
        )

        assert_that(result, has_length(1))
        assert_that(result[0], is_(SAMPLE_DAYS[1]))

    @staticmethod
    def test_does_not_return_other_zip_codes(clean_db):
        save_historical_data("90210", SAMPLE_DAYS)

        result = get_historical_data("20500")

        assert_that(result, is_(empty()))


class SaveHistoricalDataTests:

    @staticmethod
    def test_overwrites_existing_day(clean_db):
        save_historical_data("90210", SAMPLE_DAYS)

        updated_day = HistoricalDay(
            date=date(2024, 1, 2),
            temp_max=99.9,
            temp_min=1.1,
            precipitation=5.5,
        )
        save_historical_data("90210", [updated_day])

        result = get_historical_data("90210", start_date=date(2024, 1, 2), end_date=date(2024, 1, 2))

        assert_that(result, has_length(1))
        assert_that(result[0], is_(updated_day))
