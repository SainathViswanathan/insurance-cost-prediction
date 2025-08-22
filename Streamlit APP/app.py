# File: app.py
# Streamlit App for Insurance Premium Prediction - Styled UI with Live API Integration

import streamlit as st
import pandas as pd
import requests

# Continuous features used in scaling (not needed locally anymore)
cont_features = ['Age', 'Height', 'Weight', 'BMI']

# -------------------------------
# Streamlit Page Configuration
# -------------------------------
st.set_page_config(page_title="💰 Insurance Premium Estimator", layout="wide")

# -------------------------------
# Custom CSS Styling
# -------------------------------
st.markdown("""
<style>
/* Title styling */
h1 {
    text-align: center;   /* Center the title */
    color: #00b3b3;       /* Teal color for title */
    font-size: 42px;      /* Increased font size by 1 step */
}

/* Subheader styling (form description) */
.form-desc {
    text-align: center;   /* Center the description */
    font-size: 30px;      /* Larger than feature labels */
    font-weight: 500;     /* Medium bold */
    margin-bottom: 25px;  /* Add spacing below */
}

/* Feature input box styling */
.stNumberInput, .stSelectbox {
    max-width: 250px;     /* Restrict input width */
    margin: auto;         /* Center align input boxes */
    display: block;
}

/* Button styling */
.stButton>button {
    background-color: #00b3b3; /* Teal button */
    color: white;              /* White text */
    height: 3em;               /* Button height */
    width: 220px;              /* Button width */
    border-radius: 10px;       /* Rounded corners */
    font-size: 20px;           /* Larger text */
    margin: 0 auto;         /* Center align with spacing */
    display: block;
    text-align: center;        /* Center align text */
}

/* Premium output box styling */
.premium-box {
    background-color: #00b3b3; /* Teal background */
    color: white;              /* White text */
    padding: 15px;             /* Padding inside box */
    border-radius: 8px;        /* Rounded corners */
    text-align: center;        /* Center align text */
    font-size: 22px;           /* Bigger font */
    font-weight: bold;         /* Bold text */
    max-width: 400px;          /* Restrict width */
    margin: 10px auto 10px auto; /* Position box lower */
}

/* Download CSV button styling */
.stDownloadButton>button {
    font-size: 18px;     /* Bigger font for button */
    padding: 10px 20px;  /* Add padding */
    margin-top: 10px;    /* Raised 2 lines higher than before */
    margin-left: auto;   /* Center align */
    margin-right: auto;
    display: block;
}

/* Footer styling */
.footer {
    position: fixed;   /* Fix at bottom-right */
    bottom: 5px;
    right: 10px;
    font-size: 14px;
    color: gray;       /* Subtle gray */
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title Section
# -------------------------------
st.title("💰 Insurance Premium Estimator")
st.markdown('<div class="form-desc">Predict your insurance premium using the form below:</div>', unsafe_allow_html=True)

# -------------------------------
# Input Layout
# -------------------------------
row1 = st.columns([1, 1, 1], gap="small")
with row1[0]:
    age = st.number_input("Age", min_value=18, max_value=66, value=30)
with row1[1]:
    diabetes = st.selectbox("Do you have Diabetes?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
with row1[2]:
    blood_pressure = st.selectbox("Blood Pressure Problems?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

row2 = st.columns([1, 1, 1], gap="small")
with row2[0]:
    any_transplant = st.selectbox("Any Transplants?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
with row2[1]:
    any_chronic = st.selectbox("Any Chronic Diseases?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
with row2[2]:
    height = st.number_input("Height (cm)", min_value=145, max_value=188, value=170)

row3 = st.columns([1, 1, 1], gap="small")
with row3[0]:
    weight = st.number_input("Weight (kg)", min_value=51, max_value=132, value=70)
with row3[1]:
    known_allergies = st.selectbox("Known Allergies?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
with row3[2]:
    history_cancer = st.selectbox("Family History of Cancer?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

row4 = st.columns([1, 1, 1], gap="small")
with row4[1]:
    num_surgeries = st.number_input("Number of Major Surgeries", min_value=0, max_value=3, value=0)

# -------------------------------
# Auto-calculate BMI
# -------------------------------
bmi = weight / ((height / 100) ** 2)
st.markdown(f"#### 📊 Your BMI: **{bmi:.2f}**")

bmi_normal = 1 if 18.5 <= bmi < 25 else 0
bmi_overweight = 1 if 25 <= bmi < 30 else 0
bmi_obese = 1 if bmi >= 30 else 0

age_30_39 = 1 if 30 <= age <= 39 else 0
age_40_49 = 1 if 40 <= age <= 49 else 0
age_50_59 = 1 if 50 <= age <= 59 else 0
age_60_plus = 1 if age >= 60 else 0

# -------------------------------
# Prepare payload for API
# -------------------------------
payload = {
    'Age': int(age),
    'Diabetes': int(diabetes),
    'Blood_Pressure_Problems': int(blood_pressure),
    'Any_Transplants': int(any_transplant),
    'Any_Chronic_Diseases': int(any_chronic),
    'Height': float(height),
    'Weight': float(weight),
    'Known_Allergies': int(known_allergies),
    'History_of_Cancer_in_Family': int(history_cancer),
    'Number_of_Major_Surgeries': int(num_surgeries)
}


# -------------------------------
# Prediction + Output via API
# -------------------------------
if st.button("Estimate Premium"):
    try:
        api_url = "https://insurance-cost-prediction-jef1.onrender.com/predict"
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                prediction = result["prediction"]
                
                # Display premium box
                st.markdown(f'<div class="premium-box">💵 Estimated Insurance Premium: ₹{prediction:,.2f}</div>', unsafe_allow_html=True)
                
                # -------------------------------
                # Download CSV
                # -------------------------------
                input_data = pd.DataFrame([{
                    **payload,
                    'BMI': bmi,
                    'BMI_Category_Normal': bmi_normal,
                    'BMI_Category_Overweight': bmi_overweight,
                    'BMI_Category_Obese': bmi_obese,
                    'Age_Group_30-39': age_30_39,
                    'Age_Group_40-49': age_40_49,
                    'Age_Group_50-59': age_50_59,
                    'Age_Group_60+': age_60_plus
                }])

                st.write("### Download your input data")
                csv = input_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='insurance_input.csv',
                    mime='text/csv',
                )

            else:
                st.error(f"API Error: {result.get('error')}")
        else:
            st.error(f"Request failed with status code {response.status_code}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# -------------------------------
# Footer
# -------------------------------
st.markdown('<div class="footer">Sainath Viswanathan</div>', unsafe_allow_html=True)
