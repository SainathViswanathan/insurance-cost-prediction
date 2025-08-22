# File: flask_app.py
# Flask API for Insurance Premium Prediction

from flask import Flask, request, jsonify
import joblib
import pickle
import pandas as pd

app = Flask(__name__)

# Load model + scaler
model = joblib.load("best_model.pkl")
scaler = joblib.load("scaler.pkl")

# Continuous features
cont_features = ['Age', 'Height', 'Weight', 'BMI']


@app.route('/')
def home():
    return "✅ Insurance Premium Prediction API is running!"


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON input
        data = request.get_json(force=True)

        # Extract raw inputs (10 features)
        age = data['Age']
        diabetes = data['Diabetes']
        blood_pressure = data['Blood_Pressure_Problems']
        any_transplant = data['Any_Transplants']
        any_chronic = data['Any_Chronic_Diseases']
        height = data['Height']
        weight = data['Weight']
        known_allergies = data['Known_Allergies']
        history_cancer = data['History_of_Cancer_in_Family']
        num_surgeries = data['Number_of_Major_Surgeries']

        # --- Feature engineering (same as Streamlit) ---
        bmi = weight / ((height / 100) ** 2)
        bmi_normal = 1 if 18.5 <= bmi < 25 else 0
        bmi_overweight = 1 if 25 <= bmi < 30 else 0
        bmi_obese = 1 if bmi >= 30 else 0

        age_30_39 = 1 if 30 <= age <= 39 else 0
        age_40_49 = 1 if 40 <= age <= 49 else 0
        age_50_59 = 1 if 50 <= age <= 59 else 0
        age_60_plus = 1 if age >= 60 else 0

        # --- Build full row with 18 features ---
        input_df = pd.DataFrame([{
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
        }])

        # Ensure same column order as training
        input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)

        # Scale continuous features
        cont_features = ['Age', 'Height', 'Weight', 'BMI']
        input_df[cont_features] = scaler.transform(input_df[cont_features])

        # Predict
        prediction = model.predict(input_df)[0]

        return jsonify({
            "success": True,
            "prediction": float(prediction)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)
