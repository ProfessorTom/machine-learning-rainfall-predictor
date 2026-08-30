from datetime import date
from typing import Optional, List
import requests
from dateutil.relativedelta import relativedelta

from db import get_missing_historical_ranges, save_historical_data, get_historical_data
from entities import GeocodedZip, HistoricalDay
from tests.conftest import BEVERLY_HILLS_LOCATION


def fetch_historical_weather(
        location: GeocodedZip,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
) -> List[HistoricalDay]:
    """
    Fetch daily historical weather for a location from Open-Meteo.

    Defaults to the last 2 years ending today.

    Returns a list of HistoricalDay objects containing:
        - date
        - temp_max
        - temp_min
        - precipitation

    Raises an exception if the request fails.
    """
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - relativedelta(years=2)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    daily = data["daily"]
    results: List[HistoricalDay] = []

    for i, day_str in enumerate(daily["time"]):
        results.append(
            HistoricalDay(
                date=date.fromisoformat(day_str),
                temp_max=daily["temperature_2m_max"][i],
                temp_min=daily["temperature_2m_min"][i],
                precipitation=daily["precipitation_sum"][i],
            )
        )

    return results


def get_or_fetch_historical_weather(
        location: GeocodedZip,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
) -> List[HistoricalDay]:
    """
    Return historical weather for a location.

    Uses cached data when possible and only fetches missing
    start/end ranges from Open-Meteo.
    """
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - relativedelta(years=2)

    missing_ranges = get_missing_historical_ranges(
        location.zip,
        start_date,
        end_date,
    )

    for range_start, range_end in missing_ranges:
        new_days = fetch_historical_weather(
            location,
            start_date=range_start,
            end_date=range_end,
        )
        save_historical_data(location.zip, new_days)

    return get_historical_data(location.zip, start_date, end_date)


if __name__ == "__main__":
    data = fetch_historical_weather(BEVERLY_HILLS_LOCATION)

    for d in data:
        print(d)

    resultCount = len(data)
    print(f"{resultCount} results")
    print(f"{resultCount//365} year(s), {resultCount%365} day(s)")
