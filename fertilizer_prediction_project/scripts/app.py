from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Set correct paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level
MODEL_PATH = os.path.join(BASE_DIR, "models", "fertilizer_prediction_model.pkl")

# Load model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ Model file not found! Please train the model first.")

model = joblib.load(MODEL_PATH)

print("✅ Model loaded successfully!")

@app.route("/", methods=["GET"])
def home():
    return "Fertilizer Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict_fertilizer():
    try:
        data = request.json
        print("📥 Received Data:", data)

        # Extract input values
        nitrogen = float(data.get("nitrogen", 0))
        phosphorus = float(data.get("phosphorus", 0))
        potassium = float(data.get("potassium", 0))
        crop = data.get("crop", "Unknown")  # No encoding, accept any crop
        pH = float(data.get("pH", 0))

        # Prepare features for model prediction
        features = pd.DataFrame([[nitrogen, phosphorus, potassium, pH]],
                                columns=["Nitrogen", "Phosphorus", "Potassium", "pH Level"])

        # Predict fertilizer recommendation
        prediction = model.predict(features)[0]
        print("✅ Prediction:", prediction)
        return jsonify({"recommended_fertilizer": prediction})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": "Invalid input or server error"}), 400

if __name__ == "__main__":
    app.run(debug=True)
