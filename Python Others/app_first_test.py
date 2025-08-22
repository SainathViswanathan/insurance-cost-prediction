# File: app.py
# Streamlit App for Insurance Premium Prediction

import streamlit as st
import pandas as pd
import joblib

# --- Load trained model ---
model = joblib.load("best_model.pkl")

# --- Load trained model ---
#model = joblib.load("best_model.pkl")
# scaler = joblib.load("scaler.pkl")  # if needed


# --- Columns expected by the model ---
# model_columns = [
#    'Age', 'Diabetes', 'BloodPressureProblems', 'AnyTransplants', 'AnyChronicDiseases',
#    'KnownAllergies', 'HistoryOfCancerInFamily', 'Height', 'Weight', 'NumberOfMajorSurgeries', 'BMI'
#]

# --- Streamlit UI ---
st.title("Insurance Premium Estimator")
st.write("Enter your details below to estimate your insurance premium:")

# User Inputs
age = st.number_input("Age", min_value=18, max_value=66, value=30)
diabetes = st.selectbox("Do you have Diabetes?", options=[0, 1], format_func=lambda x: "Yes" if x==1 else "No")
blood_pressure = st.selectbox("Do you have Blood Pressure Problems?", options=[0, 1], format_func=lambda x: "Yes" if x==1 else "No")
any_transplant = st.selectbox("Have you had any Transplants?", options=[0, 1], format_func=lambda x: "Yes" if x==1 else "No")
any_chronic = st.selectbox("Do you have any Chronic Diseases?", options=[0, 1], format_func=lambda x: "Yes" if x==1 else "No")
height = st.number_input("Height (cm)", min_value=145, max_value=188, value=170)
weight = st.number_input("Weight (kg)", min_value=51, max_value=132, value=70)
known_allergies = st.selectbox("Do you have Known Allergies?", options=[0, 1], format_func=lambda x: "Yes" if x==1 else "No")
history_cancer = st.selectbox("Family History of Cancer?", options=[0, 1], format_func=lambda x: "Yes" if x==1 else "No")
num_surgeries = st.number_input("Number of Major Surgeries", min_value=0, max_value=3, value=0)

# --- Calculate BMI ---
bmi = weight / ((height/100) ** 2)

# Compute BMI categories
bmi_normal = 1 if 18.5 <= bmi < 25 else 0
bmi_overweight = 1 if 25 <= bmi < 30 else 0
bmi_obese = 1 if bmi >= 30 else 0

# Compute Age Groups
age_30_39 = 1 if 30 <= age <= 39 else 0
age_40_49 = 1 if 40 <= age <= 49 else 0
age_50_59 = 1 if 50 <= age <= 59 else 0
age_60_plus = 1 if age >= 60 else 0


# Prepare input DataFrame
input_data = pd.DataFrame([{
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

# --- Ensure columns match the model ---
input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

# --- Prediction ---
if st.button("Estimate Premium"):
    prediction = model.predict(input_data)[0]
    st.success(f"Estimated Insurance Premium: ₹{prediction:,.2f}")