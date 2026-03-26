import streamlit as st
import pickle
import numpy as np

# ================= LOAD =================
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

# ================= PAGE =================
st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")

# ================= CSS =================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #020617, #1e293b);
    color: white;
}

/* ===== CENTER CONTENT ===== */
.block-container {
    max-width: 1000px;
    margin: auto;
    padding-top: 2rem;
}

/* ===== GLASS CARD ===== */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 25px;
}

/* ===== INPUT SPACING ===== */
.stSelectbox, .stSlider, .stNumberInput {
    margin-bottom: 15px;
}

/* ===== SECTION TITLE ===== */
.section-title {
    margin-top: 10px;
    margin-bottom: 15px;
    font-size: 18px;
    font-weight: 600;
}

/* ===== BUTTON ===== */
div.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    color: white;
    border-radius: 12px;
    height: 45px;
    width: 200px;
    display: block;
    margin: auto;
    border: none;
    font-size: 16px;
}

/* ===== RESULT ===== */
.result {
    margin-top: 30px;
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}

/* ===== CENTER TEXT ===== */
h1, p {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("<h1>💻 Laptop Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p>⚡ Smart AI-based Laptop Price Prediction System</p>", unsafe_allow_html=True)

st.markdown("---")

# ================= INPUT =================
#st.markdown("<div class='card'>", unsafe_allow_html=True)

# 🔹 BASIC INFO
st.markdown("<div class='section-title'>🔧 Basic Info</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    company = st.selectbox('Brand', df['Company'].unique())
with col2:
    type_name = st.selectbox('Type', df['TypeName'].unique())
with col3:
    ram = st.selectbox('RAM (GB)', [2,4,6,8,12,16,24,32,64])

# 🔹 HARDWARE
st.markdown("<div class='section-title'>⚙️ Hardware</div>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    weight = st.number_input('Weight (kg)', min_value=0.5)
with col5:
    touchscreen = st.selectbox('Touchscreen', ['No','Yes'])
with col6:
    ips = st.selectbox('IPS Display', ['No','Yes'])

# 🔹 DISPLAY
st.markdown("<div class='section-title'>🖥️ Display</div>", unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)
with col7:
    screen_size = st.slider('Screen Size (inches)', 10.0, 18.0, 13.0)
with col8:
    resolution = st.selectbox('Resolution', ['1920x1080','1366x768','1600x900','3840x2160'])
with col9:
    cpu = st.selectbox('CPU', df['Cpu brand'].unique())

# 🔹 STORAGE
st.markdown("<div class='section-title'>💾 Storage</div>", unsafe_allow_html=True)
col10, col11, col12 = st.columns(3)
with col10:
    hdd = st.selectbox('HDD (GB)', [0,128,256,512,1024,2048])
with col11:
    ssd = st.selectbox('SSD (GB)', [0,128,256,512,1024])
with col12:
    gpu = st.selectbox('GPU', df['Gpu brand'].unique())

# 🔹 OS
st.markdown("<div class='section-title'>💻 Operating System</div>", unsafe_allow_html=True)
os = st.selectbox('OS', df['os'].unique())

st.markdown("</div>", unsafe_allow_html=True)

# ================= BUTTON =================
st.markdown("<br>", unsafe_allow_html=True)

if st.button("💰 Predict Price"):

    touchscreen_val = 1 if touchscreen == 'Yes' else 0
    ips_val = 1 if ips == 'Yes' else 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])

    ppi = ((X_res**2 + Y_res**2) ** 0.5) / screen_size

    query = np.array([
        company, type_name, ram, weight,
        touchscreen_val, ips_val, ppi,
        cpu, hdd, ssd, gpu, os
    ]).reshape(1, 12)

    price = int(np.exp(pipe.predict(query)[0]))

    # ================= RESULT =================
    st.markdown(f"<div class='result'>💰 ₹ {price:,}</div>", unsafe_allow_html=True)

    if price < 40000:
        st.markdown("<p>🟢 Budget Laptop</p>", unsafe_allow_html=True)
    elif price < 80000:
        st.markdown("<p>🟡 Mid-range Laptop</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p>🔴 Premium Laptop</p>", unsafe_allow_html=True)

 # ================= DETAILS =================
    st.markdown("### 📊 Details")
    st.write(f"RAM: {ram}GB | CPU: {cpu} | SSD: {ssd}GB")

    # ================= FEATURE TAGS =================
    st.markdown("### 🏷️ Features")
    st.success(f"RAM: {ram}GB")
    st.info(f"CPU: {cpu}")
    st.warning(f"SSD: {ssd}GB")

 # ================= WHY PRICE =================
    
