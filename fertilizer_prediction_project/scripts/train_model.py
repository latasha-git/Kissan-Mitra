import joblib
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Ensure model directory exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "fertilizer_prediction_model.pkl")

# Sample dataset (Replace this with actual dataset)
data = {
    "Nitrogen": [10, 20, 30, 40, 50],
    "Phosphorus": [5, 15, 25, 35, 45],
    "Potassium": [10, 20, 30, 40, 50],
    "Crop": ["Wheat", "Rice", "Maize", "Barley", "Soybean"],
    "pH Level": [6.5, 6.8, 7.0, 7.2, 6.9],
    "Fertilizer": ["Urea", "DAP", "MOP", "NPK", "Compost"]
}

df = pd.DataFrame(data)

# Splitting dataset
X = df[["Nitrogen", "Phosphorus", "Potassium", "Crop", "pH Level"]]
y = df["Fertilizer"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X.drop(columns=["Crop"]), y)  # Ignore 'Crop' for now

# Save model
joblib.dump(model, MODEL_PATH)

print(f"✅ Model saved at: {MODEL_PATH}")
