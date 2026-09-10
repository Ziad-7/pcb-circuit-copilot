import os
import streamlit as st
from PIL import Image
from api_client import api_client

st.set_page_config(
    page_title="Circuit & PCB Lab Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# ULTRA-MODERN PREMIUM DARK UI THEME & DESIGN TOKENS
# -------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
  /* Base App Theme */
  .stApp {
    background: radial-gradient(circle at 50% 0%, #111827 0%, #080c14 100%);
    color: #e2e8f0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
  }
  
  /* Top Hero Header */
  .hero-container {
    padding: 1.2rem 0 1.8rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  .hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #34D399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
  }
  .hero-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    font-weight: 400;
  }

  /* Glassmorphic Cards */
  .glass-card {
    background: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    margin-bottom: 1.5rem;
  }

  .card-header-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* Component Badge Chips */
  .comp-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 0.3rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
  }
  .comp-badge:hover {
    background: rgba(56, 189, 248, 0.2);
    border-color: #38bdf8;
  }

  .source-chip {
    display: inline-flex;
    align-items: center;
    background: rgba(52, 211, 153, 0.1);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.3);
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
  }

  /* Topic Pill Buttons */
  div[data-testid="stHorizontalBlock"] button {
    border-radius: 9999px !important;
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #cbd5e1 !important;
    font-size: 0.85rem !important;
    padding: 0.35rem 0.9rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  }
  div[data-testid="stHorizontalBlock"] button:hover {
    border-color: #38bdf8 !important;
    color: #f8fafc !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
  }

  /* Status Indicator */
  .status-pill-green {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16, 185, 129, 0.12);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
  }
  .status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #34d399;
    box-shadow: 0 0 8px #34d399;
  }

  /* Input fields */
  .stTextInput > div > div > input {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
  }

  /* Primary Button */
  div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.35) !important;
    transition: all 0.2s ease !important;
  }
  div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.55) !important;
    transform: translateY(-1px);
  }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR CONTROLS & SYSTEM HEALTH
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Hardware Copilot")
    st.caption("Multimodal Visual Detection & Datasheet RAG")

    # Backend Connection Indicator
    health = api_client.check_health()
    if health.get("status") == "healthy":
        st.markdown(f"""
        <div class="status-pill-green">
          <span class="status-dot"></span> System Online ({health.get('vector_store_chunks', 0)} Specs)
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"🧠 Engine: `{health.get('active_model')}`")
    else:
        st.warning("⚠️ Backend Offline — Start FastAPI on Port 8000")

    st.markdown("---")
    st.markdown("#### 📷 Board Photo Input")

    sample_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "images"))
    sample_files = []
    if os.path.exists(sample_images_dir):
        sample_files = [f for f in os.listdir(sample_images_dir) if f.endswith(('.jpg', '.png'))]

    selected_image_name = None
    uploaded_file = st.file_uploader("Upload Breadboard / PCB Photo", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        selected_image_name = uploaded_file.name
        save_path = os.path.join(sample_images_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(uploaded_file, caption="Uploaded Circuit Image", use_container_width=True)
    elif sample_files:
        chosen_sample = st.selectbox("Or Pick a Sample Circuit Board", sample_files)
        selected_image_name = chosen_sample
        img_path = os.path.join(sample_images_dir, chosen_sample)
        st.image(Image.open(img_path), caption=f"Selected: {chosen_sample}", use_container_width=True)

    st.markdown("---")
    with st.expander("📚 Indexed Component Datasheets", expanded=False):
        st.caption("Official technical documentation indexed in vector memory:")
        st.markdown("""
        - **LM7805**: 5V Linear Voltage Regulator
        - **ATmega328P**: Arduino Uno AVR Microcontroller
        - **ESP32-WROOM-32**: Wi-Fi & Bluetooth MCU
        - **NE555**: Precision Timer IC
        - **L298N**: Dual Full-Bridge Motor Driver
        - **Passives Guide**: Diodes, Capacitors, Resistors
        - **Breadboard Guide**: LEDs, Motors, Pull-up Resistors
        """)

# -------------------------------------------------------------
# MAIN VIEWPORT
# -------------------------------------------------------------
st.markdown("""
<div class="hero-container">
  <div class="hero-title">CIRCUIT & PCB LAB COPILOT</div>
  <div class="hero-subtitle">Upload your circuit board or breadboard, detect components visually with YOLO, and get verified connection guides & electrical limits directly from official manufacturer datasheets.</div>
</div>
""", unsafe_allow_html=True)

# Clean Topic Starters
st.markdown("<div style='font-size:0.85rem; color:#94a3b8; margin-bottom:0.4rem; font-weight:500;'>QUICK TOPIC STARTERS:</div>", unsafe_allow_html=True)
pill_c1, pill_c2, pill_c3, pill_c4 = st.columns(4)

suggested_q = None
with pill_c1:
    if st.button("💡 LED & Resistor Math"):
        suggested_q = "How do I connect an LED to an Arduino pin, and what resistor value should I use?"
with pill_c2:
    if st.button("🔌 Arduino 5V Regulator Setup"):
        suggested_q = "How do I connect an LM7805 voltage regulator to power an Arduino safely?"
with pill_c3:
    if st.button("🔄 Motors & Flyback Protection"):
        suggested_q = "Why shouldn't I connect a DC motor directly to an Arduino pin, and what diode do I need?"
with pill_c4:
    if st.button("⚠️ Safe Current & Voltage Limits"):
        suggested_q = "What is the maximum safe current per Arduino Uno GPIO pin and how much can it supply in total?"

# Main Query Command Bar
query_col, btn_col = st.columns([4, 1])

with query_col:
    user_query = st.text_input(
        "Ask anything about wiring, pinouts, resistors, motors, or component specs:",
        value=suggested_q if suggested_q else "",
        placeholder="e.g. How do I wire this component? Which pin is ground? What resistor do I use?",
        label_visibility="collapsed"
    )

with btn_col:
    execute_search = st.button("Analyze Circuit", type="primary", use_container_width=True)

# Handle Query Execution
if execute_search:
    if not user_query or len(user_query.strip()) < 3:
        st.warning("Please enter a technical question or select a topic above.")
    else:
        with st.spinner("Analyzing circuit photo & retrieving official datasheet specifications..."):
            try:
                result = api_client.query(user_query, selected_image_name)

                # Two-Column Presentation Layout
                col_canvas, col_report = st.columns([1, 1.25])

                # Left: Hardware Vision Canvas
                with col_canvas:
                    st.markdown("""
                    <div class="glass-card">
                      <div class="card-header-title">🔍 Visual Inspection Canvas</div>
                    """, unsafe_allow_html=True)

                    annotated_path = result.get("annotated_image_path")
                    if annotated_path and os.path.exists(annotated_path):
                        st.image(Image.open(annotated_path), caption="Computer Vision Detection & Bounding Boxes", use_container_width=True)
                    elif selected_image_name:
                        orig_p = os.path.join(sample_images_dir, selected_image_name)
                        if os.path.exists(orig_p):
                            st.image(Image.open(orig_p), caption="Input Circuit Board", use_container_width=True)

                    comps = result.get("detected_components", [])
                    if comps:
                        st.markdown("<div style='margin-top:0.8rem; font-size:0.9rem; font-weight:600; color:#cbd5e1;'>Detected Components:</div>", unsafe_allow_html=True)
                        for c in comps:
                            st.markdown(f'<span class="comp-badge">{c["class_name"]} ({c["confidence"]*100:.0f}%)</span>', unsafe_allow_html=True)
                            st.caption(f"• {c['description']}")
                    else:
                        st.info("No specific IC markers detected. Consulting general datasheet knowledge.")

                    st.markdown("</div>", unsafe_allow_html=True)

                # Right: Technical Lab Report
                with col_report:
                    st.markdown("""
                    <div class="glass-card">
                      <div class="card-header-title">📋 Engineering & Wiring Report</div>
                    """, unsafe_allow_html=True)

                    st.markdown(result["answer"])

                    # Citations
                    sources = result.get("sources", [])
                    if sources:
                        st.markdown("<div style='margin-top:1.2rem; border-top:1px solid rgba(255,255,255,0.08); padding-top:0.8rem;'></div>", unsafe_allow_html=True)
                        st.markdown("<div style='font-size:0.85rem; font-weight:600; color:#94a3b8; margin-bottom:0.4rem;'>VERIFIED DATASHEET CITATIONS:</div>", unsafe_allow_html=True)
                        for s in sources:
                            st.markdown(f'<span class="source-chip">📄 {s}</span>', unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error communicating with backend: {e}")
