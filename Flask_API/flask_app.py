from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# ---- Load model + scaler ----
model = joblib.load(r"M:\Module - 19 - DSML Portfolio Project\1 - Insurance Cost Prediction\Flask_API\best_model.pkl")
scaler = joblib.load(r"M:\Module - 19 - DSML Portfolio Project\1 - Insurance Cost Prediction\Flask_API\scaler.pkl")  # we used StandardScaler on ['Age','Height','Weight','BMI']

MODEL_COLUMNS = list(model.feature_names_in_)  # 18 columns used during training
CONT_FEATURES = ['Age', 'Height', 'Weight', 'BMI']

# Ten raw inputs expected from UI/API (we derive the rest)
REQUIRED_KEYS = [
    "Age",
    "Diabetes",
    "Blood_Pressure_Problems",
    "Any_Transplants",
    "Any_Chronic_Diseases",
    "Height",
    "Weight",
    "Known_Allergies",
    "History_of_Cancer_in_Family",
    "Number_of_Major_Surgeries"
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Insurance Premium Prediction API",
        "required_keys": REQUIRED_KEYS
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_columns": MODEL_COLUMNS,
        "cont_features": CONT_FEATURES
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON with header Content-Type: application/json"
            }), 400

        data = request.get_json()

        # ---- Check required keys ----
        missing = [k for k in REQUIRED_KEYS if k not in data]
        if missing:
            return jsonify({
                "success": False,
                "error": f"Missing keys: {missing}",
                "expected": REQUIRED_KEYS
            }), 400

        # ---- Extract values ----
        age = int(data["Age"])
        diabetes = int(data["Diabetes"])
        blood_pressure = int(data["Blood_Pressure_Problems"])
        any_transplant = int(data["Any_Transplants"])
        any_chronic = int(data["Any_Chronic_Diseases"])
        height = float(data["Height"])
        weight = float(data["Weight"])
        known_allergies = int(data["Known_Allergies"])
        history_cancer = int(data["History_of_Cancer_in_Family"])
        num_surgeries = int(data["Number_of_Major_Surgeries"])

        # ---- Derived features ----
        bmi = weight / ((height / 100.0) ** 2)
        bmi_normal = 1 if 18.5 <= bmi < 25 else 0
        bmi_overweight = 1 if 25 <= bmi < 30 else 0
        bmi_obese = 1 if bmi >= 30 else 0

        age_30_39 = 1 if 30 <= age <= 39 else 0
        age_40_49 = 1 if 40 <= age <= 49 else 0
        age_50_59 = 1 if 50 <= age <= 59 else 0
        age_60_plus = 1 if age >= 60 else 0

        # ---- Build row ----
        row = {
            'Age': age,
            'Diabetes': diabetes,
            'Blood_Pressure_Problems': blood_pressure,
            'Any_Transplants': any_transplant,
            'Any_Chronic_Diseases': any_chronic,
            'Height': height,
            'Weight': weight,
            'Known_Allergies': known_allergies,
            'History_of_Cancer_in_Family': history_cancer,
            'Number_of_Major_Surgeries': num_surgeries,
            'BMI': bmi,
            'BMI_Category_Normal': bmi_normal,
            'BMI_Category_Overweight': bmi_overweight,
            'BMI_Category_Obese': bmi_obese,
            'Age_Group_30-39': age_30_39,
            'Age_Group_40-49': age_40_49,
            'Age_Group_50-59': age_50_59,
            'Age_Group_60+': age_60_plus
        }

        df = pd.DataFrame([row])
        df = df.reindex(columns=MODEL_COLUMNS, fill_value=0)  

        # ---- DEBUG LOGS ----
        print("Incoming DF columns:", list(df.columns))
        print("Scaler expects:", getattr(scaler, "feature_names_in_", CONT_FEATURES))

        # ---- Scale ----
        df[CONT_FEATURES] = scaler.transform(df[CONT_FEATURES])

        # ---- Predict ----
        pred = float(model.predict(df)[0])

        return jsonify({
            "success": True,
            "prediction": pred,
            "derived": {
                "BMI": round(bmi, 2),
                "Age_Group_30-39": age_30_39,
                "Age_Group_40-49": age_40_49,
                "Age_Group_50-59": age_50_59,
                "Age_Group_60+": age_60_plus
            }
        })

    except Exception as e:
        app.logger.exception("Prediction error")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
