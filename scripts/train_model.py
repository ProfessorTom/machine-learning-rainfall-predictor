import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load historical weather data
df = pd.read_csv("../data/centreville_weather.csv")

# Features and target
X = df[['temp_max', 'temp_min']]
y = df['precipitation']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "../rainfall_model.pkl")
print("Model trained and saved as rainfall_model.pkl")
