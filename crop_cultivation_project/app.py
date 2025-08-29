from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Load trained model and label encoder
try:
    model = joblib.load("crop_climate_model.pkl")
    label_encoder = joblib.load("crop_label_encoder.pkl")
    print("✅ Model and Label Encoder loaded successfully!")
except Exception as e:
    print("❌ Error loading model or label encoder:", e)

@app.route("/", methods=["GET"])
def home():
    return "Crop Cultivation Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict_cultivation():
    try:
        data = request.json
        print("📥 Received Data:", data)

        # Extract input values
        crop = data.get("crop")
        temperature = float(data.get("temperature", 0))
        rainfall = float(data.get("rainfall", 0))
        humidity = float(data.get("humidity", 0))
        soil_moisture = float(data.get("soil_moisture", 0))
        pH = float(data.get("pH", 0))
        sunlight = float(data.get("sunlight", 0))
        wind_speed = float(data.get("wind_speed", 0))

        # Encode crop name
        crop_encoded = label_encoder.transform([crop])[0]

        # Prepare features for model prediction
        features = pd.DataFrame([[crop_encoded, temperature, rainfall, humidity, soil_moisture, pH, sunlight, wind_speed]],
                                columns=["Crop", "Temperature", "Rainfall", "Humidity", "Soil Moisture", "pH Level", "Sunlight", "Wind Speed"])

        # Predict cultivation feasibility
        prediction = model.predict(features)[0]
        result = "Cultivate" if prediction == 1 else "Do not cultivate"

        print("✅ Prediction:", result)
        return jsonify({"result": result})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": "Invalid input or server error"}), 400

if __name__ == "__main__":
    app.run(debug=True)
