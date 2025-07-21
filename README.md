
# 🏢 UrbanNest – Intelligent Flat Price Estimator for Kolkata

**UrbanNest** is a Streamlit-based web application that provides accurate market valuations for residential flats in Kolkata using multiple machine learning models. It enables users to input property features and instantly get an estimated price using trained regression models.

---

## 📘 Project Overview

This project is aimed at developing a predictive solution to estimate flat prices in the Kolkata metropolitan region based on detailed property attributes. The application leverages advanced regression models such as:

* ElasticNet
* Random Forest
* Gradient Boosting
* XGBoost

Users can interactively select features like BHK, floor, area, amenities, furnishing level, location, and more. The app integrates geolocation services to determine latitude and longitude from user-provided addresses.

---

## 📊 Dataset Summary

The dataset used for training the models includes:

* Location-specific flat listings from **99acers (Kolkata region)**
* 1,100+ entries with 30+ features per property
* Features include:

  * Structural: BHK, Area, Floor, Total Floors, Bathrooms, Balcony
  * Amenities: Lift, Park, Gym, Servant Room, Store Room, etc.
  * Premium facilities: Swimming pool, Wi-Fi, Power backup, Clubhouse, etc.
  * Geographical: Latitude, Longitude (derived from address)

Target Variable: **Price in Lakhs (INR)**

---

## 🚀 Instructions to Run

### ✅ Prerequisites

Ensure Python 3.7+ is installed with the following libraries:

```bash
pip install streamlit pandas numpy joblib geopy
```

### ▶️ Run the App

```bash
streamlit run app.py
```

* Input property details from the sidebar
* Choose a model
* Click on “Predict Price” to get the estimated price and insights

---

## 🤖 Model Comparisons

| Model             | RMSE (₹ Lakhs) | R² Score |
| ----------------- | -------------- | -------- |
| ElasticNet        | 36.35          | 0.7733   |
| Random Forest     | 35.48          | 0.7840   |
| Gradient Boosting | 31.07          | 0.8344   |
| XGBoost           | 30.30          | 0.8425   |

* **XGBoost** outperforms others in both accuracy and generalization.
* Feature importances are visualized for tree-based models.

---

## 🖼️ Screenshots

### 📌 Main Interface

![Main Interface](screenshots/main_interface.png)

### 📌 Feature Inputs Sidebar

![Sidebar](screenshots/sidebar_inputs.png)

### 📌 Prediction Result

![Prediction](screenshots/predicted_price.png)

<!-- 
---
## 🌐 Deployment

If hosted, add your deployment link here:

🔗 [View Live App on Streamlit Cloud](#)

> *(Replace with actual deployment URL if applicable)* -->

---

## 👨‍💻 Developed By

**Tanmoy Giri**
MTech. CSDP, IIT Kharagpur

