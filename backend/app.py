# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# import numpy as np
# import joblib

# app = Flask(__name__)
# CORS(app)

# # Load trained model
# model = joblib.load("pcos_phase1_model.pkl")


# # Convert Yes/No values to 1/0
# def yes_no_to_int(value):
#     if isinstance(value, str):
#         return 1 if value.lower() == "yes" else 0
#     return int(value)


# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.json

#         # Debug: see what frontend sends
#         print("Received Data:", data)

#         # Extract values from frontend
#         age = float(data["age"])
#         height = float(data["height"])
#         weight = float(data["weight"])
#         waist = float(data["waist"])
#         hip = float(data["hip"])

#         cycle = yes_no_to_int(data["cycle"])
#         cycle_length = float(data["cycle_length"])

#         weight_gain = yes_no_to_int(data["weight_gain"])
#         hair_growth = yes_no_to_int(data["hair_growth"])
#         hair_loss = yes_no_to_int(data["hair_loss"])
#         pimples = yes_no_to_int(data["pimples"])
#         fast_food = yes_no_to_int(data["fast_food"])
#         exercise = yes_no_to_int(data["exercise"])

#         # Calculate derived features
#         height_m = height / 100
#         bmi = weight / (height_m ** 2)
#         whr = waist / hip

#         # Create dataframe in SAME order as training
#         input_df = pd.DataFrame({
#             "Age (yrs)": [age],
#             "BMI": [bmi],
#             "WHR": [whr],
#             "Cycle(R/I)": [cycle],
#             "Cycle length(days)": [cycle_length],
#             "Weight gain(Y/N)": [weight_gain],
#             "hair growth(Y/N)": [hair_growth],
#             "Hair loss(Y/N)": [hair_loss],
#             "Pimples(Y/N)": [pimples],
#             "Fast food (Y/N)": [fast_food],
#             "Reg.Exercise(Y/N)": [exercise]
#         })

#         # Predict probability
#         probability = model.predict_proba(input_df)[0][1]

#         # Convert numpy value to normal Python float
#         probability = float(probability)

#         risk_percentage = round(probability * 100, 2)

#         return jsonify({
#             "risk": risk_percentage
#         })

#     except Exception as e:
#         return jsonify({
#             "error": str(e)
#         }), 400


# @app.route("/")
# def home():
#     return "PCOS Backend Running Successfully 🚀"


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("pcos_phase1_model.pkl")


def yes_no_to_int(value):
    if isinstance(value, str):
        return 1 if value.lower() == "yes" else 0
    return int(value)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Received Data:", data)

        age = float(data["age"])
        height = float(data["height"])
        weight = float(data["weight"])
        waist = float(data["waist"])
        hip = float(data["hip"])

        cycle = yes_no_to_int(data["cycle"])
        cycle_length = float(data["cycle_length"])

        weight_gain = yes_no_to_int(data["weight_gain"])
        hair_growth = yes_no_to_int(data["hair_growth"])
        hair_loss = yes_no_to_int(data["hair_loss"])
        pimples = yes_no_to_int(data["pimples"])
        fast_food = yes_no_to_int(data["fast_food"])
        exercise = yes_no_to_int(data["exercise"])

        height_m = height / 100
        bmi = weight / (height_m ** 2)
        whr = waist / hip

        input_df = pd.DataFrame({
            "Age (yrs)": [age],
            "BMI": [bmi],
            "WHR": [whr],
            "Cycle(R/I)": [cycle],
            "Cycle length(days)": [cycle_length],
            "Weight gain(Y/N)": [weight_gain],
            "hair growth(Y/N)": [hair_growth],
            "Hair loss(Y/N)": [hair_loss],
            "Pimples(Y/N)": [pimples],
            "Fast food (Y/N)": [fast_food],
            "Reg.Exercise(Y/N)": [exercise]
        })

        probability = model.predict_proba(input_df)[0][1]
        risk_percentage = round(float(probability) * 100, 2)

        # Risk classification
        if risk_percentage < 30:
            risk_level = "Low"
            recommendation = "Maintain a healthy lifestyle with balanced diet and regular exercise."
        elif risk_percentage < 60:
            risk_level = "Moderate"
            recommendation = "Consider improving lifestyle habits and monitor symptoms. A medical consultation may help."
        else:
            risk_level = "High"
            recommendation = "High PCOS risk detected. Please consult a gynecologist or healthcare professional."

        return jsonify({
            "risk": risk_percentage,
            "level": risk_level,
            "recommendation": recommendation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/")
def home():
    return "PCOS Backend Running Successfully 🚀"


if __name__ == "__main__":
    app.run(debug=True)