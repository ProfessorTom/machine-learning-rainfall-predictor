import pandas as pd
import json

# Load JSON from a file
with open("../data/centreville_weather.json") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)
df.to_csv("../data/centreville_weather.csv", index=False)
print("Weather CSV generated")
