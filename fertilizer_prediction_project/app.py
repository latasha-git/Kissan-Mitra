from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model and encoders
model = joblib.load("models/fertilizer_prediction_model.pkl")
crop_encoder = joblib.load("models/crop_encoder.pkl")
fertilizer_encoder = joblib.load("models/fertilizer_encoder.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        nitrogen = data["nitrogen"]
        phosphorus = data["phosphorus"]
        potassium = data["potassium"]
        crop_type = data["crop_type"]
        pH_level = data["pH_level"]
        
        # Encode crop type
        crop_encoded = crop_encoder.transform([crop_type])[0]
        
        # Prepare input data
        input_data = [[nitrogen, phosphorus, potassium, crop_encoded, pH_level]]
        
        # Predict fertilizer
        prediction = model.predict(input_data)[0]
        
        # Decode fertilizer recommendation
        recommended_fertilizer = fertilizer_encoder.inverse_transform([prediction])[0]
        
        return jsonify({"recommended_fertilizer": recommended_fertilizer})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
