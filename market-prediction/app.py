from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained models
cost_model = joblib.load("models/cost_model.pkl")
price_model = joblib.load("models/price_model.pkl")

# Define the home route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input from the form
        state_input = request.form.get("state").strip()
        crop_input = request.form.get("crop").strip()

        # Check if the inputs are valid
        if not state_input or not crop_input:
            return render_template("index.html", message="Please provide valid inputs.")

        # Prepare the user input for prediction
        # Load the column names from the training data (you need to ensure this column list matches your model)
        df = pd.read_excel(r"data\cleaned_datasetof market analysis.xlsx")
        df = pd.get_dummies(df, columns=["state", "crop"], drop_first=False)
        X_columns = df.drop(columns=["costcultivation", "price"]).columns

        # Create a dataframe for prediction
        user_input = pd.DataFrame(columns=X_columns, data=[[0] * len(X_columns)])

        # Set categorical values based on user input
        for col in X_columns:
            if col == f"state_{state_input}":
                user_input[col] = 1
            elif col == f"crop_{crop_input}":
                user_input[col] = 1

        # Make predictions
        cost_prediction = cost_model.predict(user_input)[0]
        price_prediction = price_model.predict(user_input)[0]

        # Render results on the page
        return render_template(
            "index.html",
            state=state_input,
            crop=crop_input,
            cost_prediction=round(cost_prediction, 2),
            price_prediction=round(price_prediction, 2),
        )

    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
