from datetime import date
from unittest.mock import patch, MagicMock

from dateutil.relativedelta import relativedelta
from hamcrest import assert_that, is_, has_length

from weather import fetch_historical_weather
from entities import HistoricalDay
from tests.conftest import BEVERLY_HILLS_LOCATION


# Minimal fake Open-Meteo response
FAKE_OPEN_METEO_RESPONSE = {
    "daily": {
        "time": ["2024-01-01", "2024-01-02"],
        "temperature_2m_max": [18.5, 20.1],
        "temperature_2m_min": [8.2, 9.0],
        "precipitation_sum": [0.0, 2.3],
    }
}

class FetchHistoricalWeatherTests:

    @patch("weather.requests.get")
    def test_fetch_historical_weather_happy_path(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = FAKE_OPEN_METEO_RESPONSE
        mock_get.return_value = mock_response

        # Act
        result = fetch_historical_weather(BEVERLY_HILLS_LOCATION)

        # Assert
        assert_that(result, has_length(2))

        expected = [
            HistoricalDay(
                date=date(2024, 1, 1),
                temp_max=18.5,
                temp_min=8.2,
                precipitation=0.0
            ),
            HistoricalDay(
                date=date(2024, 1, 2),
                temp_max=20.1,
                temp_min=9.0,
                precipitation=2.3
            ),
        ]
        assert_that(result, is_(expected))

        # verify the call
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        params = kwargs["params"]

        today = date.today()
        expected_start = today - relativedelta(years=2)

        assert_that(params["start_date"], is_(expected_start.isoformat()))
        assert_that(params["end_date"], is_(today.isoformat()))
