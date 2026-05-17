import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIGURATION & STYLING
# ============================================================================
st.set_page_config(
    page_title="Smart PM2.5 Prediction Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main_app():
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

        /* ── Result cards ── */
        .result-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1.2rem 0;
        }

        .result-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 1.4rem 1.2rem;
            text-align: center;
            border: 1px solid #D8ECD8;
            box-shadow: 0 2px 8px rgba(26,58,42,0.06);
            transition: transform 0.2s;
        }

        .result-card:hover { transform: translateY(-2px); }

        .rc-label {
            font-size: 0.72em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #6B8F71;
            margin-bottom: 0.5rem;
        }

        .rc-value {
            font-size: 2.4em;
            font-weight: 700;
            color: #1A3A2A;
            line-height: 1;
            font-family: 'DM Mono', monospace;
        }

        .rc-unit {
            font-size: 0.8em;
            color: #9BB59B;
            margin-top: 0.2rem;
            font-weight: 500;
        }

        /* ── Status pill ── */
        .status-pill {
            display: inline-block;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.9em;
            margin-top: 0.6rem;
        }
        .pill-good      { background:#D1FAE5; color:#065F46; }
        .pill-moderate  { background:#FEF3C7; color:#92400E; }
        .pill-sensitive { background:#FFEDD5; color:#9A3412; }
        .pill-unhealthy { background:#FEE2E2; color:#991B1B; }
        .pill-hazardous { background:#F3E8FF; color:#6B21A8; }

        /* ── Rec boxes ── */
        .rec-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            margin: 0.7rem 0;
            border: 1px solid #D8ECD8;
            box-shadow: 0 1px 4px rgba(26,58,42,0.05);
            display: flex;
            gap: 0.9rem;
            align-items: flex-start;
        }

        .rec-icon {
            font-size: 1.4em;
            flex-shrink: 0;
            margin-top: 0.1rem;
        }

        .rec-title {
            font-size: 0.78em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #40916C;
            margin-bottom: 0.3rem;
        }

        .rec-text {
            font-size: 0.93em;
            color: #2C4A35;
            line-height: 1.55;
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

        .scale-row {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.22rem 0;
            font-size: 0.85em;
            color: #2C4A35;
        }

        .scale-dot {
            width: 10px; height: 10px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        /* ── Divider ── */
        hr { border-color: #C8DFC8 !important; }

        /* ── Footer ── */
        .footer {
            text-align: center;
            color: #7A9E7A;
            font-size: 0.82em;
            padding: 1.5rem 0 0;
            border-top: 1px solid #C8DFC8;
            margin-top: 2rem;
        }

        /* label overrides */
        label { color: #1A3A2A !important; font-weight: 500 !important; }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # ============================================================================
    # SIDEBAR
    # ============================================================================
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="sb-card"><div class="sb-title">ℹ️ About</div><div class="sb-body">PM2.5 Prediction System — AI-powered air quality forecasting using <strong>Random Forest Regression</strong> with 10 environmental indicators.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-card"><div class="sb-title">📊 Model Info</div><div class="sb-body"><b>Algorithm:</b> Random Forest<br><b>Features:</b> 10 indicators<br><b>Output:</b> PM2.5 (µg/m³)</div></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="sb-card">
          <div class="sb-title">📈 PM2.5 Scale</div>
          <div class="scale-row"><div class="scale-dot" style="background:#10B981"></div> Good — 0–12 µg/m³</div>
          <div class="scale-row"><div class="scale-dot" style="background:#F59E0B"></div> Moderate — 12–35</div>
          <div class="scale-row"><div class="scale-dot" style="background:#F97316"></div> Sensitive — 35–55</div>
          <div class="scale-row"><div class="scale-dot" style="background:#EF4444"></div> Unhealthy — 55–150</div>
          <div class="scale-row"><div class="scale-dot" style="background:#8B5CF6"></div> Hazardous — 150+</div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================================
    # HERO HEADER
    # ============================================================================
    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-title">🌿 Smart PM2.5 Prediction Dashboard</div>
      <p class="hero-sub">Predict PM2.5 pollution levels using Machine Learning · Random Forest Regression</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================================
    # LOAD MODEL
    # ============================================================================
    @st.cache_resource
    def load_model():
        return joblib.load("../../Models/pm25_model_pollution.pkl")

    model = load_model()

    # ============================================================================
    # INPUT FORM
    # ============================================================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-label">📍 Location</div>', unsafe_allow_html=True)
        City = st.selectbox(
            "City", ["Cairo", "Dubai", "London", "New York", "Tokyo", "Paris", "Nairobi"],
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="section-label">🌤️ Season</div>', unsafe_allow_html=True)
        Season = st.selectbox(
            "Season", ["Winter", "Spring", "Summer", "Autumn"],
            label_visibility="collapsed"
        )

    st.markdown('<div class="section-label">💨 Pollution Indicators</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: PM10 = st.number_input("PM10", value=50.0, min_value=0.0, max_value=500.0, step=1.0)
    with c2: NO2  = st.number_input("NO2",  value=20.0, min_value=0.0, max_value=300.0, step=0.5)
    with c3: CO   = st.number_input("CO",   value=1.0,  min_value=0.0, max_value=50.0,  step=0.1)
    with c4: SO2  = st.number_input("SO2",  value=10.0, min_value=0.0, max_value=300.0, step=0.5)

    st.markdown('<div class="section-label">🌡️ Weather Conditions</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: Temperature_mean = st.number_input("Temperature (°C)", value=25.0, min_value=-50.0, max_value=60.0, step=0.5)
    with c2: Humidity         = st.number_input("Humidity (%)",     value=60.0, min_value=0.0,   max_value=100.0, step=1.0)
    with c3: Wind_speed       = st.number_input("Wind Speed (km/h)", value=5.0, min_value=0.0,   max_value=100.0, step=0.5)
    with c4: st.empty()

    st.markdown('<div class="section-label">🌳 Environmental Factors</div>', unsafe_allow_html=True)
    Green_Space = st.number_input("Green Space Coverage (%)", value=40.0, min_value=0.0, max_value=100.0, step=1.0)

    # ============================================================================
    # PREDICT BUTTON
    # ============================================================================
    st.markdown("---")
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        predict_button = st.button("🔮  Predict PM2.5 Level", use_container_width=True)

    # ============================================================================
    # PREDICTION RESULTS
    # ============================================================================
    if predict_button:
        input_data = pd.DataFrame({
            'PM10': [PM10], 'NO2': [NO2], 'CO': [CO], 'SO2': [SO2],
            'Green_Space': [Green_Space], 'Temperature_mean': [Temperature_mean],
            'Humidity': [Humidity], 'Wind_speed': [Wind_speed],
            'City': [City], 'Season': [Season]
        })

        prediction = model.predict(input_data)[0]

        # Category logic (unchanged)
        if prediction <= 12:
            category, emoji, pill_cls = "Good", "🟢", "pill-good"
            health_rec = "Air quality is satisfactory. Outdoor activities are safe for everyone."
            activity   = "✅ Safe for outdoor exercise"
            bar_color  = "#10B981"
        elif prediction <= 35:
            category, emoji, pill_cls = "Moderate", "🟡", "pill-moderate"
            health_rec = "Air quality is acceptable. Sensitive groups may limit prolonged outdoor exposure."
            activity   = "⚠️ Sensitive individuals should limit outdoor activities"
            bar_color  = "#F59E0B"
        elif prediction <= 55:
            category, emoji, pill_cls = "Unhealthy for Sensitive Groups", "🟠", "pill-sensitive"
            health_rec = "Sensitive groups should reduce outdoor activities."
            activity   = "🚫 Sensitive groups should avoid strenuous outdoor activities"
            bar_color  = "#F97316"
        elif prediction <= 150:
            category, emoji, pill_cls = "Unhealthy", "🔴", "pill-unhealthy"
            health_rec = "Everyone should limit outdoor activities. Use N95 masks if going outside."
            activity   = "🏠 Minimize outdoor activities; use air purifiers"
            bar_color  = "#EF4444"
        else:
            category, emoji, pill_cls = "Hazardous", "☠️", "pill-hazardous"
            health_rec = "Avoid all outdoor activities. Stay indoors with filtered air."
            activity   = "🏠 Stay indoors; use air purifiers and filters"
            bar_color  = "#8B5CF6"

        st.markdown('<div class="section-label">📈 Results</div>', unsafe_allow_html=True)

        # ── Metric cards ──
        st.markdown(f"""
        <div class="result-grid">
          <div class="result-card">
            <div class="rc-label">PM2.5 Level</div>
            <div class="rc-value">{prediction:.1f}</div>
            <div class="rc-unit">µg/m³</div>
          </div>
          <div class="result-card">
            <div class="rc-label">Air Quality Status</div>
            <div style="margin-top:0.5rem">
              <span class="status-pill {pill_cls}">{emoji} {category}</span>
            </div>
          </div>
          <div class="result-card">
            <div class="rc-label">Location</div>
            <div class="rc-value" style="font-size:1.6em">{City}</div>
            <div class="rc-unit">{Season}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Gauge + Bar chart ──
        st.markdown('<div class="section-label">📊 Visual Analysis</div>', unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            # Gauge chart
            gauge_max = max(200, prediction * 1.3)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(prediction, 1),
                title={"text": "PM2.5 (µg/m³)", "font": {"size": 14, "color": "#1A3A2A", "family": "DM Sans"}},
                number={"font": {"size": 36, "color": "#1A3A2A", "family": "DM Mono"}, "suffix": " µg/m³"},
                gauge={
                    "axis": {"range": [0, gauge_max], "tickwidth": 1, "tickcolor": "#9BB59B",
                             "tickfont": {"size": 10, "color": "#6B8F71"}},
                    "bar": {"color": bar_color, "thickness": 0.28},
                    "bgcolor": "#EEF5EE",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0,   12],  "color": "#D1FAE5"},
                        {"range": [12,  35],  "color": "#FEF3C7"},
                        {"range": [35,  55],  "color": "#FFEDD5"},
                        {"range": [55,  150], "color": "#FEE2E2"},
                        {"range": [150, gauge_max], "color": "#EDE9FE"},
                    ],
                    "threshold": {
                        "line": {"color": "#1A3A2A", "width": 3},
                        "thickness": 0.8,
                        "value": prediction
                    },
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=260,
                margin=dict(t=30, b=10, l=20, r=20),
                font={"family": "DM Sans"}
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with chart_col2:
            # Horizontal pollutant bar chart
            pollutants   = ["PM2.5 (pred)", "PM10", "NO2", "SO2", "CO×10"]
            values       = [round(prediction, 1), PM10, NO2, SO2, CO * 10]
            bar_colors   = [bar_color, "#40916C", "#52B788", "#74C69D", "#95D5B2"]

            fig_bar = go.Figure(go.Bar(
                x=values,
                y=pollutants,
                orientation='h',
                marker=dict(color=bar_colors, line=dict(width=0)),
                text=[f"{v:.1f}" for v in values],
                textposition="outside",
                textfont=dict(size=11, color="#1A3A2A", family="DM Mono"),
            ))
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=260,
                margin=dict(t=20, b=10, l=10, r=60),
                xaxis=dict(showgrid=True, gridcolor="#D8ECD8", zeroline=False,
                           tickfont=dict(size=10, color="#6B8F71"), title=""),
                yaxis=dict(showgrid=False, tickfont=dict(size=11, color="#1A3A2A", family="DM Sans")),
                title=dict(text="Pollutant Comparison", font=dict(size=13, color="#1A3A2A", family="DM Sans"),
                           x=0.02, y=0.98),
                font={"family": "DM Sans"},
                bargap=0.35,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # ── Recommendations ──
        st.markdown('<div class="section-label">💡 Recommendations</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="rec-card">
          <div class="rec-icon">🩺</div>
          <div>
            <div class="rec-title">Health</div>
            <div class="rec-text">{health_rec}</div>
          </div>
        </div>
        <div class="rec-card">
          <div class="rec-icon">🏃</div>
          <div>
            <div class="rec-title">Activity</div>
            <div class="rec-text">{activity}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Environmental insights
        insights = []
        if Green_Space >= 50:
            insights.append("✦ Excellent green space coverage supports better air quality")
        elif Green_Space >= 30:
            insights.append("✦ Good green space presence helps mitigate pollution")
        else:
            insights.append("⚠ Limited green space; more vegetation needed")

        if Wind_speed >= 8:
            insights.append("✦ Strong winds effectively disperse pollutants")
        elif Wind_speed >= 3:
            insights.append("✦ Moderate winds support natural pollutant dispersion")
        else:
            insights.append("⚠ Low wind speed may allow pollutant accumulation")

        st.markdown(f"""
        <div class="rec-card">
          <div class="rec-icon">🌍</div>
          <div>
            <div class="rec-title">Environmental Insights</div>
            <div class="rec-text">{'<br>'.join(insights)}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Input summary expander
        with st.expander("📋 View Input Parameters"):
            summary_data = pd.DataFrame({
                'Parameter': ['PM10','NO2','CO','SO2','Green Space','Temperature','Humidity','Wind Speed','City','Season'],
                'Value':     [f"{PM10:.1f}", f"{NO2:.1f}", f"{CO:.1f}", f"{SO2:.1f}",
                              f"{Green_Space:.1f}%", f"{Temperature_mean:.1f}°C",
                              f"{Humidity:.1f}%", f"{Wind_speed:.1f}", City, Season]
            })
            st.dataframe(summary_data, use_container_width=True, hide_index=True)

    # ============================================================================
    # FOOTER
    # ============================================================================
    st.markdown("""
    <div class="footer">
      🌿 <strong>Air Quality Prediction Dashboard</strong> &nbsp;·&nbsp;
      Machine Learning &amp; Streamlit &nbsp;·&nbsp; Random Forest Regression
    </div>
    """, unsafe_allow_html=True)
pg = st.navigation([st.Page(main_app, title='Smart PM2.5 Prediction Dashboard', icon='🌿'), st.Page('Humidity_model_App.py', title='Humidity Cluster Prediction System', icon='💧')])
pg.run()
