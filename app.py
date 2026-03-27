import streamlit as st
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .main { background-color: #f0f4f8; }

        .title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a1a2e;
        }

        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1rem;
        }

        .bmi-score {
            text-align: center;
            font-size: 4rem;
            font-weight: 700;
            margin: 0;
        }

        .bmi-category {
            text-align: center;
            font-size: 1.3rem;
            font-weight: 600;
        }

        .advice-box {
            background: #ffffff;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
            font-size: 0.95rem;
        }

        .stButton > button {
            background-color: #1a1a2e;
            color: white;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            border-radius: 10px;
            border: none;
        }

        .stButton > button:hover {
            background-color: #e94560;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="title">⚖️ BMI Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Check your Body Mass Index instantly</p>', unsafe_allow_html=True)
st.divider()

# Unit toggle
unit = st.radio("Select unit system:", ["Metric (kg, cm)", "Imperial (lbs, ft)"], horizontal=True)
st.divider()

# Inputs
if unit == "Metric (kg, cm)":
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
    with col2:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
    height_m = height / 100
else:
    col1, col2 = st.columns(2)
    with col1:
        weight_lbs = st.number_input("Weight (lbs)", min_value=1.0, max_value=660.0, value=154.0, step=1.0)
    with col2:
        height_ft = st.number_input("Height (ft)", min_value=1.0, max_value=8.0, value=5.0, step=0.1)
    weight = weight_lbs * 0.453592
    height_m = height_ft * 0.3048

# Calculate
if st.button("Calculate BMI", use_container_width=True):
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category, color, advice = "Underweight", "#3b82f6", "Consider eating more nutritious meals and consult a doctor."
    elif bmi < 25:
        category, color, advice = "Normal Weight ✅", "#22c55e", "Great! Keep maintaining a healthy diet and active lifestyle."
    elif bmi < 30:
        category, color, advice = "Overweight", "#f97316", "Consider a balanced diet and regular physical activity."
    else:
        category, color, advice = "Obese", "#ef4444", "Please consult a healthcare professional for guidance."

    st.divider()

    # Score
    st.markdown(f'<p class="bmi-score" style="color:{color}">{bmi:.1f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="bmi-category" style="color:{color}">{category}</p>', unsafe_allow_html=True)

    # Advice
    st.markdown(f"""
        <div class="advice-box" style="border-left: 5px solid {color}">
            💡 {advice}
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        number={'suffix': " BMI", 'font': {'size': 28, 'family': 'Poppins'}},
        gauge={
            'axis': {'range': [10, 40]},
            'bar': {'color': color, 'thickness': 0.25},
            'steps': [
                {'range': [10, 18.5], 'color': "#bfdbfe"},
                {'range': [18.5, 25], 'color': "#bbf7d0"},
                {'range': [25, 30],   'color': "#fed7aa"},
                {'range': [30, 40],   'color': "#fecaca"},
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))

    fig.update_layout(
        margin=dict(t=30, b=10, l=30, r=30),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': 'Poppins'}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Reference metrics
    st.subheader("📊 BMI Reference")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Underweight", "< 18.5")
    c2.metric("Normal", "18.5–24.9")
    c3.metric("Overweight", "25–29.9")
    c4.metric("Obese", "≥ 30")

st.divider()
st.caption("⚠️ BMI is a general indicator and does not account for muscle mass, age, or other health factors.")
