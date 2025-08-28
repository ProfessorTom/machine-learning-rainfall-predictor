import pandas as pd
import joblib

# Load the CSV with forecast
df = pd.read_csv("../data/centreville_forecast.csv")

# Load trained model
model = joblib.load("../rainfall_model.pkl")

# Predict precipitation
df['predicted_precipitation'] = model.predict(df[['temp_max', 'temp_min']])

# Save predictions
df.to_csv("../data/centreville_forecast.csv", index=False)
print("Predictions added to centreville_forecast.csv")
