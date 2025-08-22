# File: app.py
# Streamlit App for Insurance Premium Prediction - Styled UI

import streamlit as st
import pandas as pd
import joblib

# --- Load trained model ---
model = joblib.load("best_model.pkl")

# --- Columns expected by the model ---
#model_columns = [
#    'Age', 'Diabetes', 'Blood_Pressure_Problems', 'Any_Transplants',
#    'Any_Chronic_Diseases', 'Height', 'Weight', 'Known_Allergies',
#    'History_of_Cancer_in_Family', 'Number_of_Major_Surgeries', 'BMI'
#]

# --- Streamlit Page Config ---
st.set_page_config(page_title="Insurance Premium Estimator", layout="wide")

# --- Custom CSS for styling ---
st.markdown("""
<style>
/* Title styling */
h1 {
    text-align: center;
    color: #00b3b3;  /* Change title color here */
}

/* Button styling */
.stButton>button {
    background-color: #00b3b3;  /* Change button color here */
    color: white;
    height: 3em;
    width: 200px;
    border-radius:10px;
    font-size:16px;
}

/* Premium output styling */
.premium-box {
    background-color: #00b3b3;  /* Change output background here */
    color: white;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}

/* Bottom-right corner name */
.footer {
    position: fixed;
    bottom: 5px;
    right: 10px;
    font-size: 14px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("Insurance Premium Estimator")
st.write("Predict your insurance premium using the form below:")

# --- Input Features in 3-column Layout ---
cols = st.columns(3)

# Feature inputs
with cols[0]:
    age = st.number_input("Age", min_value=18, max_value=66, value=30)
    diabetes = st.selectbox("Do you have Diabetes?", options=[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    height = st.number_input("Height (cm)", min_value=145, max_value=188, value=170)
    known_allergies = st.selectbox("Known Allergies?", options=[0,1], format_func=lambda x: "Yes" if x==1 else "No")

with cols[1]:
    blood_pressure = st.selectbox("Blood Pressure Problems?", options=[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    any_transplant = st.selectbox("Any Transplants?", options=[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    weight = st.number_input("Weight (kg)", min_value=51, max_value=132, value=70)
    history_cancer = st.selectbox("Family History of Cancer?", options=[0,1], format_func=lambda x: "Yes" if x==1 else "No")

with cols[2]:
    any_chronic = st.selectbox("Any Chronic Diseases?", options=[0,1], format_func=lambda x: "Yes" if x==1 else "No")
    num_surgeries = st.number_input("Number of Major Surgeries", min_value=0, max_value=3, value=0)
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0)

# --- Prepare input DataFrame ---
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
    'BMI': bmi
}])

# Ensure columns match model
#input_data = input_data.reindex(columns=model_columns, fill_value=0)
# --- Ensure columns match the model ---
input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

# --- Estimate Premium Button ---
if st.button("Estimate Premium"):
    prediction = model.predict(input_data)[0]
    st.markdown(f'<div class="premium-box">Estimated Insurance Premium: ₹{prediction:,.2f}</div>', unsafe_allow_html=True)

# --- Download CSV Option ---
st.write("### Download your input data")
csv = input_data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='insurance_input.csv',
    mime='text/csv',
)

# --- Footer with Name ---
st.markdown('<div class="footer">Sainath Viswanathan</div>', unsafe_allow_html=True)
