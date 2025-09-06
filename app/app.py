# Required libraries
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from geopy.geocoders import Nominatim
# import shap


# === Model Load ===
model_paths = {
    'ElasticNet': '../models/elasticnet_model.pkl',
    'Random Forest': '../models/random_forest_model.pkl',
    'Gradient Boosting': '../models/gradient_boosting_model.pkl',
    'XGBoost': '../models/xgboost_model.pkl'
}
column_paths = {
    'ElasticNet': '../models/elasticnet_model_columns.pkl',
    'Random Forest': '../models/random_forest_model_columns.pkl',
    'Gradient Boosting': '../models/gradient_boosting_model_columns.pkl',
    'XGBoost': '../models/xgboost_model_columns.pkl'
}
models = {name: joblib.load(path) for name, path in model_paths.items()}

model_metrics = {
    'ElasticNet': {'RMSE': 36.35, 'R²': 0.7733},
    'Random Forest': {'RMSE': 35.48, 'R²': 0.7840},
    'Gradient Boosting': {'RMSE': 31.07, 'R²': 0.8344},
    'XGBoost': {'RMSE': 30.30, 'R²': 0.8425}
}

# === Geolocation Utility ===
def get_coordinates(address):
    try:
        geolocator = Nominatim(user_agent="geoapi_kolkata_project")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return 22.5959, 88.4026  # Default (Kolkata)

# === Sidebar UI ===
st.sidebar.title("🏠 House Features")
model_choice = st.sidebar.selectbox("Select Model", list(models.keys()))

# Inputs
BHK = st.sidebar.selectbox("BHK", [1, 2, 3, 4, 5, 6], index=1)
Area = st.sidebar.number_input("Area (350 - 6000 sq.ft)", min_value=350, max_value=6000, value=1000)
Bathrooms = st.sidebar.selectbox("No of Bathrooms", [2, 3, 4, 5], index=0)
Balcony = st.sidebar.selectbox("No of Balconies", [0, 1, 2, 3], index=1)
Total_Floors = st.sidebar.number_input("Total Floors in the Building", min_value=2, max_value=27, value=4)
Floor = st.sidebar.number_input("At which Floor", min_value=1, max_value=int(Total_Floors), value=int(min(3, Total_Floors)))

# Encoded Mappings
property_age_map = {
    '0 to 1 Year Old': 0.5, '1 to 5 Year Old': 3, '5 to 10 Year Old': 7.5,
    '10+ Year Old': 12.5, 'Within 3 months': -0.25, 'Within 6 months': -0.5, 'Under Construction': -1.0
}
Property_Age_Years = property_age_map[st.sidebar.selectbox("Property Age", list(property_age_map), index=1)]

area_type_map = {'Carpet Area': 0, 'Built-up Area': 1, 'Super Built-up Area': 2}
Area_Type_Encoded = area_type_map[st.sidebar.selectbox("Area Type", list(area_type_map), index=2)]

furnishing_map = {'Unfurnished': 0, 'Semi-Furnished': 1, 'Fully-Furnished': 2}
Furnishing_Level_Code = furnishing_map[st.sidebar.selectbox("Furnishing Level", list(furnishing_map), index=0)]

# Boolean Features
bool_features = [
    'Store_Room', 'Study_Room', 'Pooja_Room', 'Servant_Room', 'Lift',
    'Maintenance', 'WaterStorage', 'VaastuCompliant', 'FireSecurity',
    'VisitorParking', 'Intercom', 'Park', 'AiryRooms', 'Gym'
]
checkbox_inputs = {
    feature: int(st.sidebar.checkbox(feature.replace('_', ' '),
        value=True if feature in ['Lift', 'Maintenance', 'WaterStorage', 'VisitorParking', 'Park', 'AiryRooms'] else False
    )) for feature in bool_features
}

# Facility Premium
facility_options = [
    'Swimming Pool', 'Club house / Community Center', 'Security Personnel',
    'Power Back-up', 'High Ceiling Height', 'Spacious Interiors',
    'Water softening plant', 'Low Density Society', 'Shopping Centre',
    'Private Garden / Terrace', 'Internet/wi-fi connectivity',
    'Centrally Air Conditioned'
]
Facility_Premium = len(st.sidebar.multiselect("Select Premium Facilities", facility_options))

# Address-based geolocation
address = st.sidebar.text_input("Enter locality or address (Kolkata)", "Lake Gardens, Kolkata")
Latitude, Longitude = get_coordinates(address)

# Construct input dictionary
input_data = {
    'BHK': BHK, 'Area': Area, 'Bathrooms': Bathrooms, 'Balcony': Balcony,
    'Floor': Floor, 'Total_Floors': Total_Floors,
    'Property_Age_Years': Property_Age_Years,
    'Area_Type_Encoded': Area_Type_Encoded,
    'Furnishing_Level_Code': Furnishing_Level_Code,
    'Facility_Premium': Facility_Premium,
    'Latitude': Latitude, 'Longitude': Longitude,
    'Floor_Ratio': Floor / Total_Floors
}
input_data.update(checkbox_inputs)

# # === Main Area ===
# st.title("UrbanNest")
# st.subheader("Intelligent Flat Price Estimator for Greater Kolkata")
# st.markdown("**Select a prediction model and enter the property details in the sidebar to estimate the price instantly.**")

# if st.button("Predict Price"):
#     model = models[model_choice]
#     feature_columns = joblib.load(column_paths[model_choice])
#     X_input = pd.DataFrame([input_data]).reindex(columns=feature_columns)

#     prediction = model.predict(X_input)[0]

#     st.subheader("Estimated Market Price")
#     st.success(f"**₹ {prediction * 100000:,.2f}**")
#     st.markdown("This is the estimated market value of the property based on the selected model and provided inputs. Prices are in Indian Rupees (INR).")

#     st.subheader("Model Performance Overview")
#     st.markdown(f"""
#     **Model Selected:** `{model_choice}`  
#     - **Root Mean Squared Error (RMSE):** ₹ {model_metrics[model_choice]['RMSE'] * 100000:,.2f}  
#     - **R² Score:** {model_metrics[model_choice]['R²']:.4f}  
    
#     *A lower RMSE and higher R² score indicate better model performance on test data.*
#     """)

#     if model_choice in ['Random Forest', 'Gradient Boosting', 'XGBoost']:
#         st.subheader("Top Influential Features")
#         model_step = model.named_steps[model_choice.lower().replace(" ", "")]
#         importances = model_step.feature_importances_
#         importance_df = pd.DataFrame({
#             'Feature': feature_columns,
#             'Importance': importances
#         }).sort_values(by='Importance', ascending=False)

#         st.markdown("The following features most significantly impacted the prediction:")
#         st.write(importance_df.head(10))
#         st.bar_chart(importance_df.set_index('Feature').head(10))
#         st.caption("*Feature importance reflects the overall influence of each input on model predictions, based on training data—not just this specific prediction.*")

# st.markdown("---")
# st.markdown("""
# **UrbanNest** — Developed by TG  
# _Kolkata Property Valuation Platform powered by Machine Learning_""")
# st.caption('UrbanNest uses advanced machine learning models to provide reliable market valuations for residential flats in Kolkata.')



# === Main Area ===
st.title("UrbanNest")
# st.subheader("Intelligent Flat Price Estimator for Greater Kolkata")
st.markdown("**Select a prediction model and enter the property details in the sidebar to estimate the price instantly.**")

if st.button("Predict Price"):
    model = models[model_choice]
    feature_columns = joblib.load(column_paths[model_choice])
    X_input = pd.DataFrame([input_data]).reindex(columns=feature_columns)

    prediction = model.predict(X_input)[0]

    st.subheader("Estimated Market Price")
    st.success(f"**₹ {prediction * 100000:,.2f}**")
    st.caption("This is the estimated market value of the property based on the selected model and provided inputs. Prices are in Indian Rupees (INR).")

    st.subheader("Model Performance Overview")
    
    st.markdown(f'<h5>Model Selected: {model_choice}</h5>', unsafe_allow_html=True)
    st.markdown(f"""
    - **Root Mean Squared Error (RMSE):** ₹ {model_metrics[model_choice]['RMSE'] * 100000:,.2f}  
    - **R² Score:** {model_metrics[model_choice]['R²']:.4f}  
    """)
    st.caption("*A lower RMSE and higher R² score indicate better model performance on test data.*")
    

    if model_choice in ['Random Forest', 'Gradient Boosting', 'XGBoost']:
        model_step = model.named_steps[model_choice.lower().replace(" ", "")]
        importances = model_step.feature_importances_
        importance_df = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)

        # SHAP: Local Explanation
        # try:
            

            # st.subheader("Key Drivers for This Prediction (Local SHAP Explanation)")
        #     st.markdown("<h5>Most Important Factors That Influenced This Prediction</h5>", unsafe_allow_html=True)
        #     explainer = shap.Explainer(model_step)
        #     shap_values = explainer(X_input)
        #     shap_df = pd.DataFrame({
        #         'Feature': feature_columns,
        #         'SHAP Value': shap_values.values[0]
        #     }).sort_values(by='SHAP Value', key=abs, ascending=False)

        #     st.write(shap_df.head(10))
        #     st.caption("*SHAP values show the direct influence of each feature on this specific prediction.*")

        # except Exception as e:
        #     st.warning("Local explanation (SHAP) couldn't be generated. Ensure SHAP is installed and supported by the model.")
        #     st.exception(e)

        # Feature Importance: Global Explaination
        st.markdown('<h5>Top Factors That Influence Predictions (Overall)</h5>', unsafe_allow_html=True)

        st.markdown("The following features most significantly impacted predictions across the training dataset:")
        st.write(importance_df.head(10))
        st.bar_chart(importance_df.set_index('Feature').head(10))
        st.caption("*These values reflect model-wide learning from training data, not this specific flat.*")


# === Footer ===
st.markdown("---")
st.markdown("**UrbanNest** — Developed by T_Giri")
st.caption('UrbanNest uses advanced machine learning models to provide reliable market valuations for residential flats in Kolkata and and surrounding regions.')

# st.markdown(""" 
# _Kolkata Property Valuation Platform powered by Machine Learning_
# """)