# 🌍 EcoVision-AI

### Environmental Analytics & Sustainability Intelligence Platform

An AI-powered environmental analytics platform that integrates air quality, weather, electricity consumption, and green-space data across major global cities. The project combines data engineering, exploratory data analysis, environmental insights, outlier detection, predictive modeling, clustering analysis, and interactive Streamlit dashboards to study sustainability patterns and urban environmental behavior.

---

# 🚀 Live Application

🌿 Smart Environmental Intelligence Dashboard

An interactive Streamlit application for:
- PM2.5 pollution prediction
- Humidity cluster prediction
- Environmental insights and analysis

🔗 [Open Streamlit App](https://urban-environmental-intelligence-5f83yapjzxqvh6frjpckh4.streamlit.app/)


# 📌 Project Overview

This project analyzes how environmental and urban factors interact across different cities during 2023. The analysis focuses on relationships between:

* 🌫️ Air pollution
* 🌤️ Weather conditions
* ⚡ Electricity consumption
* 🌳 Green space
* 📅 Seasonal and weekend behavior

The project also deploys machine learning and clustering models to generate environmental predictions and discover hidden city patterns.

---

# 🌍 Cities Included

* Cairo
* Dubai
* London
* New York
* Tokyo
* Paris
* Nairobi

These cities were selected to represent different:

* Climate zones
* Urban structures
* Pollution profiles
* Development patterns

---

# 📊 Dataset Information

* **Time Period:** Daily observations for 2023
* **Final Dataset Size:** 2,548 rows
* **Features:** 17 documented columns
* **Missing Values After Preprocessing:** 0

### Main Features

* PM2.5
* PM10
* O3
* NO2
* CO
* SO2
* Temperature
* Humidity
* Wind Speed
* Pressure
* Green Space
* Electricity Consumption
* Season
* isWeekend

---

# 🔍 Main Research Questions

## 1️⃣ Does Air Quality Improve With More Green Space?

The analysis revealed a strong negative relationship between green space and pollution levels. Cities with larger green-space coverage generally showed cleaner air quality and lower PM2.5 averages.

---

## 2️⃣ Are Pollution Levels Lower on Weekends?

Weekend pollution levels were slightly lower and more stable than weekdays, supporting the idea that reduced traffic and industrial activity improve air quality.

---

## 3️⃣ How Does Temperature Affect Electricity Consumption?

Temperature showed city-specific effects on electricity demand. Hotter periods increased electricity consumption in most cities due to cooling demand.

---

# 🌱 Extra Environmental Questions

## 🌤️ Which Season Has the Worst Air Quality?

Summer recorded the highest overall pollution levels, followed closely by Spring, while Autumn showed the cleanest environmental conditions.

---

## 💨 Which Weather Conditions Are Linked to Worse Air Quality?

Hot and dry conditions were associated with worse pollution levels, while humidity and wind speed generally helped reduce pollution accumulation.

---

## 🚨 Which Cities Have the Highest Risk of Bad-Air Days?

Dubai showed the highest number of severe pollution days, followed by Tokyo, Nairobi, Cairo, and New York.

---

# 📈 Exploratory Data Analysis (EDA)

The project includes extensive visual and statistical analysis:

* Correlation analysis
* Seasonal pollution trends
* City comparison dashboards
* Pollution distribution analysis
* Temperature vs electricity analysis
* Weekend vs weekday analysis
* Environmental risk analysis
* Pollution index analysis
* Heatmaps and trend visualization

---

# 🚨 Outlier Analysis

Detailed outlier analysis was performed across all cities and environmental variables to identify abnormal pollution and weather behavior.

## Key Findings

* Pollution outliers occur more frequently on weekdays
* Dubai and Cairo show extreme summer pollution events
* Winter contains the highest abnormality levels in several cities
* Wind speed and humidity strongly influence pollution accumulation
* CO and NO2 spikes are linked with unstable air-quality periods

## City-Level Outlier Insights

### Cairo

* High variability in humidity and particulate pollution
* Winter shows the largest number of pollution outliers

### Dubai

* Extreme PM2.5, PM10, NO2, and O3 events dominate summer
* Low humidity contributes to pollution accumulation

### London

* Winter contains the strongest abnormal pollution behavior
* NO2 and humidity increase during outlier periods

### Nairobi

* Strong episodic CO and PM2.5 pollution events
* Lower wind speed contributes to pollution spikes

### New York

* Wind speed and CO drive major abnormal events
* Summer and winter show stronger variability

### Paris

* CO and SO2 dominate abnormal pollution events
* Winter contains the largest abnormality count

### Tokyo

* SO2, NO2, O3, PM10, and PM2.5 generate major outliers
* Winter displays the strongest environmental instability

### Electricity Analysis

* New York shows a strong electricity-consumption outlier during July due to peak cooling demand

---

# 🤖 Machine Learning Models

## 🌫️ PM2.5 Prediction Model

A Random Forest Regressor was trained to predict PM2.5 levels using pollution and weather indicators.

### Model Performance

* **Validation R²:** 0.9085
* **Algorithm:** Random Forest Regressor

### Features Used

* PM10
* NO2
* CO
* SO2
* Temperature
* Humidity
* Wind Speed
* Green Space
* City
* Season

---

# 🧩 Clustering Analysis

The project includes multiple clustering approaches:

## 🌍 City-Level Clustering

Grouped cities based on environmental profiles.

### Main City Groups

* Hot polluted cities → Cairo & Dubai
* Cleaner temperate cities → London, Paris, New York
* Unique environmental profile → Tokyo

---

## 🍂 Seasonal Clustering

Analyzed how environmental behavior changes across seasons.

### Key Insight

Environmental structure is more city-driven than season-driven.

---

## 💧 Humidity Prediction Clustering

Used K-Means clustering to estimate humidity patterns based on pollution and weather conditions.

---

# 🖥️ Streamlit Applications

The project includes interactive Streamlit dashboards:

## 🌫️ PM2.5 Prediction Dashboard

Users can:

* Select city and season
* Enter pollution/weather values
* Predict PM2.5 level
* View health-risk category

---

## 💧 Humidity Cluster Dashboard

Users can:

* Input environmental values
* Predict humidity cluster
* View confidence and uncertainty ranges

---

# 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Streamlit
* XGBoost
* Random Forest
* K-Means Clustering

---

# 📂 Project Structure

```bash
Data/
│
├── raw/
├── integrated/
├── final/

src/
│
├── scraping/
├── Modeling/
├── Clustering/
├── Application/

notebooks/
│
├── preprocessing.ipynb
├── merge.ipynb
├── green_space_air_quality_analysis.ipynb
├── daytype_air_quality.ipynb
├── Temperature_vs_Electricity1.ipynb
├── Outliers_visualizations.ipynb
```

# 🎯 Final Conclusion

The project demonstrates how environmental systems are interconnected through pollution, weather, energy demand, and urban structure. Results show that greener and more temperate cities generally experience cleaner air, while hotter low-green-space cities face higher pollution pressure.

The combination of analytics, machine learning, clustering, environmental insights, outlier analysis, and dashboard deployment transforms the project into a complete environmental intelligence platform.

