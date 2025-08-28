# Centreville Rainfall Predictor

## Overview
Predicts rainfall for today and tomorrow in Centreville, Michigan using historical weather data and current forecast.

## Setup
1. Install dependencies:
   pip install -r requirements.txt

2. Generate historical data:
   python scripts/generate_csv.py

3. Fetch the latest forecast:
   python scripts/fetch_forecast.py

4. Train the model:
   python scripts/train_model.py

5. Predict rainfall:
   python scripts/predict_rainfall.py

6. run a server:
   python -m http.server 8000

7. navigate to localhost:8000/index.html in your browser
