from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

model = joblib.load("random_forest_model.pkl")

def validate_input(data):
    limits = {
        "N": (0, 140),
        "P": (5, 145),
        "K": (5, 205),
        "temp": (0, 50),
        "humidity": (0, 100),
        "ph": (3, 10),
        "rainfall": (0, 500)
    }

    for key, (low, high) in limits.items():
        value = data.get(key)
        if value is None:
            return f"{key} is missing"
        if not isinstance(value, (int, float)):
            return f"{key} must be a number"
        if value < low or value > high:
            return f"{key} must be between {low} and {high}"

    return None

@app.route("/")
def home():
    return "API is running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        error = validate_input(data)
        if error:
            return jsonify({"error": error}), 400

        features = [[
            data["N"],
            data["P"],
            data["K"],
            data["temp"],
            data["humidity"],
            data["ph"],
            data["rainfall"]
        ]]

        probabilities = model.predict_proba(features)[0]
        classes = model.classes_

        top3_indices = probabilities.argsort()[-3:][::-1]
        top3 = [
            {
                "crop": str(classes[i]),
                "confidence": round(float(probabilities[i]) * 100, 1)
            }
            for i in top3_indices
        ]

        return jsonify({"results": top3})

    except Exception as e:
        return jsonify({"error": str(e)}), 500