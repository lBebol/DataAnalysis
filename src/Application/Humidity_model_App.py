import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import sys
import os

# Add Modeling directory to path to import HumidityClusterModel
modeling_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Modeling'))
if modeling_dir not in sys.path:
    sys.path.append(modeling_dir)

from humidity_model import HumidityClusterModel

# ============================================================================
# PAGE CONFIGURATION & STYLING
# ============================================================================
st.set_page_config(
    page_title="Humidity Cluster Prediction",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main, .stApp, [data-testid="stAppViewContainer"] {
        background: #EEF5EE;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1100px !important;
    }

    /* ── Header ── */
    .hero-wrap {
        background: linear-gradient(135deg, #1A3A2A 0%, #2D6A4F 55%, #40916C 100%);
        border-radius: 20px;
        padding: 2.8rem 3rem 2.4rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 260px; height: 260px;
        background: radial-gradient(circle, rgba(116,198,157,0.18) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-wrap::after {
        content: '';
        position: absolute;
        bottom: -80px; left: 30%;
        width: 340px; height: 340px;
        background: radial-gradient(circle, rgba(52,211,153,0.10) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-title {
        color: #ffffff;
        font-size: 2.4em;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.8px;
        line-height: 1.1;
    }

    .hero-sub {
        color: rgba(255,255,255,0.72);
        font-size: 1em;
        font-weight: 400;
        margin: 0;
    }

    /* ── Section headers ── */
    .section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #1A3A2A;
        font-size: 0.78em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin: 1.6rem 0 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #C8DFC8;
    }

    /* ── Input cards ── */
    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInputContainer"] {
        border-radius: 10px !important;
        border: 1.5px solid #C8DFC8 !important;
        background-color: #ffffff !important;
        transition: all 0.2s !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-testid="stNumberInputContainer"]:focus-within,
    div[data-baseweb="select"] > div:hover,
    div[data-testid="stNumberInputContainer"]:hover {
        border-color: #2D6A4F !important;
        box-shadow: 0 0 0 3px rgba(45,106,79,0.15) !important;
        background-color: #F4F9F4 !important;
    }

    .stNumberInput button:hover,
    .stNumberInput button:focus,
    .stNumberInput button:active {
        background-color: #D8ECD8 !important;
        color: #1A3A2A !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* ── Predict button ── */
    .stButton > button {
        width: 100%;
        background: #1A3A2A !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.9rem 2rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95em;
        font-weight: 600;
        letter-spacing: 0.5px;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(26,58,42,0.25);
    }

    .stButton > button:hover {
        background: #2D6A4F !important;
        color: #ffffff !important;
        border: none !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(26,58,42,0.3);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #E8F3E8 !important;
    }

    .sb-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        border: 1px solid #C8DFC8;
        box-shadow: 0 1px 4px rgba(26,58,42,0.06);
    }

    .sb-title {
        font-size: 0.8em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.9px;
        color: #2D6A4F;
        margin-bottom: 0.7rem;
    }

    .sb-body {
        font-size: 0.88em;
        color: #2C4A35;
        line-height: 1.6;
    }

    /* ── Divider ── */
    hr { border-color: #C8DFC8 !important; }

    /* label overrides */
    label { color: #1A3A2A !important; font-weight: 500 !important; }

    /* Table styling to make dataframe look similar */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        border: 1px solid #C8DFC8;
        overflow: hidden;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown('<div class="sb-card"><div class="sb-title">ℹ️ About</div><div class="sb-body">Humidity Cluster Prediction — AI-powered environmental humidity modeling using KMeans clustering.</div></div>', unsafe_allow_html=True)
    

# ============================================================================
# HERO HEADER
# ============================================================================
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">💧 Humidity Cluster Prediction System</div>
  <p class="hero-sub">Predict environmental humidity clusters based on air quality metrics</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL
# ============================================================================
@st.cache_resource
def load_model():
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Models/humidity_model.pkl'))
    return HumidityClusterModel.load(model_path)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ============================================================================
# INPUT FORM
# ============================================================================
st.markdown('<div class="section-label">💨 Air Quality & Weather Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    PM25 = st.number_input("PM2.5", value=35.00, format="%.2f", step=0.5)
    NO2 = st.number_input("NO2", value=40.00, format="%.2f", step=0.5)
    SO2 = st.number_input("SO2", value=30.00, format="%.2f", step=0.5)
    Wind_speed = st.number_input("Wind Speed", value=7.00, format="%.2f", step=0.5)

with col2:
    O3 = st.number_input("O3", value=25.00, format="%.2f", step=0.5)
    CO = st.number_input("CO", value=350.00, format="%.2f", step=0.5)
    Temperature_mean = st.number_input("Temperature Mean", value=20.00, format="%.2f", step=0.5)

# ============================================================================
# PREDICT BUTTON
# ============================================================================
st.markdown("---")
_, mid, _ = st.columns([1, 1.4, 1])
with mid:
    predict_button = st.button("🔮 Predict", use_container_width=True)

# ============================================================================
# PREDICTION RESULTS
# ============================================================================
if predict_button:
    input_data = {
        'PM2.5': PM25,
        'O3': O3,
        'NO2': NO2,
        'CO': CO,
        'SO2': SO2,
        'Temperature_mean': Temperature_mean,
        'Wind_speed': Wind_speed
    }
    
    try:
        prediction_df = model.predict(input_data)
        
        # --- Visualization ---
        pred_hum = prediction_df.iloc[0]['Predicted_Humidity']
        
        st.markdown('<div class="section-label">📊 Visual Analysis</div>', unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred_hum,
            title={"text": "Predicted Humidity (%)", "font": {"size": 14, "color": "#1A3A2A"}},
            number={"font": {"size": 36, "color": "#1A3A2A"}, "suffix": "%"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#9BB59B"},
                "bar": {"color": "#40916C", "thickness": 0.28},
                "bgcolor": "#EEF5EE",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "#FEE2E2"},
                    {"range": [30, 60], "color": "#FEF3C7"},
                    {"range": [60, 100], "color": "#D1FAE5"},
                ],
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", font={"family": "DM Sans"})
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown('<div class="section-label">📈 Prediction Result</div>', unsafe_allow_html=True)
        st.dataframe(prediction_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error during prediction: {e}")
