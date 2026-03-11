from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, VotingRegressor

# ==========================================
# FLASK SETUP
# ==========================================

app = Flask(__name__)
CORS(app)

# ==========================================
# LOAD & TRAIN MODEL ON STARTUP
# ==========================================

print("Loading dataset and training model...")

df = pd.read_csv("ds_salaries.csv")

features = [
    "work_year",
    "experience_level",
    "employment_type",
    "job_title",
    "employee_residence",
    "remote_ratio",
    "company_location",
    "company_size"
]
target = "salary_in_usd"

X = df[features].copy()
y = df[target]

encoders = {}
for col in X.select_dtypes(include="object").columns:
    encoder = LabelEncoder()
    X[col] = encoder.fit_transform(X[col])
    encoders[col] = encoder

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=200, random_state=42)
gb = GradientBoostingRegressor(n_estimators=200)
et = ExtraTreesRegressor(n_estimators=200, random_state=42)

ensemble_model = VotingRegressor(estimators=[('rf', rf), ('gb', gb), ('et', et)])
ensemble_model.fit(X_train, y_train)

print("✅ Model trained and ready!")

# ==========================================
# PREDICT ENDPOINT
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        input_data = {}

        for feature in features:
            value = data.get(feature)

            if value is None:
                return jsonify({"error": f"Missing field: {feature}"}), 400

            if feature in encoders:
                encoder = encoders[feature]
                value = str(value)
                if value not in encoder.classes_:
                    return jsonify({"error": f"Unknown value '{value}' for field '{feature}'"}), 400
                value = encoder.transform([value])[0]
            else:
                value = int(value)

            input_data[feature] = value

        input_df = pd.DataFrame([input_data], columns=features)
        predicted_salary = ensemble_model.predict(input_df)[0]

        return jsonify({"predicted_salary": int(predicted_salary)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "AI Salary Predictor API is running"})


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)