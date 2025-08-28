# Example: This could fetch data from Open-Meteo or any free source and save as CSV
import pandas as pd

forecast_data = [
    {'date': '2025-09-03', 'temp_max': 29, 'temp_min': 16},
    {'date': '2025-09-04', 'temp_max': 30, 'temp_min': 17},
    # Add more rows...
]

df = pd.DataFrame(forecast_data)
df.to_csv("../data/centreville_forecast.csv", index=False)
print("Forecast CSV updated")
