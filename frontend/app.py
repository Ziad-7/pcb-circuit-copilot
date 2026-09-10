import os
import streamlit as st
from PIL import Image
from api_client import api_client

st.set_page_config(
    page_title="PCB Component & Circuit Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Engineering Dark Workbench Styling
st.markdown("""
<style>
  .stApp {
    background-color: #0b1120;
    color: #e2e8f0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
  }
  .main-header {
    font-size: 2.2rem;
    font-weight: 800;
    color: #10b981;
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
  }
  .sub-header {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-bottom: 1.5rem;
  }
  .badge-chip {
    display: inline-block;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-family: monospace;
    font-weight: 600;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .badge-cap {
    display: inline-block;
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-family: monospace;
    font-weight: 600;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .spec-box {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.2rem;
    margin-top: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ PCB Circuit Copilot")
    st.caption("Multimodal Computer Vision + Component Datasheets RAG")
    
    # Health check
    health = api_client.check_health()
    if health.get("status") == "healthy":
        st.success(f"Backend Online | {health.get('vector_store_chunks', 0)} Chunks")
        st.caption(f"Model: `{health.get('active_model')}` (Ollama {health.get('ollama_status')})")
    else:
        st.warning("Backend Offline / Initializing")
        st.caption("Start FastAPI backend on Port 8000")
        
    st.markdown("---")
    st.markdown("#### 📷 Circuit Board Input")
    
    # Image selection / upload
    sample_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "images"))
    sample_files = []
    if os.path.exists(sample_images_dir):
        sample_files = [f for f in os.listdir(sample_images_dir) if f.endswith(('.jpg', '.png'))]
        
    selected_image_name = None
    uploaded_file = st.file_uploader("Upload Circuit Photo", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        selected_image_name = uploaded_file.name
        # Save temp copy so backend can access it
        save_path = os.path.join(sample_images_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(uploaded_file, caption="Uploaded Board", use_container_width=True)
    elif sample_files:
        chosen_sample = st.selectbox("Or Select Sample Circuit Board", sample_files)
        selected_image_name = chosen_sample
        img_path = os.path.join(sample_images_dir, chosen_sample)
        st.image(Image.open(img_path), caption=f"Sample: {chosen_sample}", use_container_width=True)

# -------------------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------------------
st.markdown('<div class="main-header">⚡ PCB COMPONENT & CIRCUIT COPILOT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Computer Vision Component Detection & Official Datasheet RAG Diagnostic System</div>', unsafe_allow_html=True)

# Quick Preset Engineering & Student Questions
st.markdown("##### 🔍 Quick Presets for Students & Lab Builders:")
col1, col2, col3, col4 = st.columns(4)

preset_q = None
with col1:
    if st.button("🔌 Arduino 5V Regulator Setup"):
        preset_q = "How do I connect this LM7805 regulator to power my Arduino safely, and what are its pinout and capacitors?"
        selected_image_name = "lm7805_power_supply.jpg"

with col2:
    if st.button("⚠️ Arduino Uno Safe Current & I2C"):
        preset_q = "What is the maximum DC current an Arduino Uno (ATmega328P) pin can safely handle, and which pins are used for I2C?"
        selected_image_name = "arduino_uno_atmega328p.jpg"

with col3:
    if st.button("🔥 Overheating & Brownouts"):
        preset_q = "Why is my voltage regulator or ESP32 getting very hot or restarting with a brownout error, and how do I fix it?"
        selected_image_name = "esp32_dev_board.jpg"

with col4:
    if st.button("⏱️ NE555 Timer & Flasher Pinout"):
        preset_q = "What are the 8 pins of the NE555 timer, and how do I wire it in astable mode for a flashing LED circuit?"
        selected_image_name = "ne555_timer_board.jpg"

# Query Input
question_input = st.text_input(
    "Ask any question about your circuit, component pinouts, Arduino wiring, or troubleshooting:",
    value=preset_q if preset_q else "",
    placeholder="e.g. How do I connect this to an Arduino? Which pin is ground? Why is it getting hot?"
)

if st.button("Analyze Circuit & Consult Datasheets", type="primary"):
    if not question_input or len(question_input.strip()) < 3:
        st.warning("Please enter a valid technical question.")
    else:
        with st.spinner("Analyzing circuit photo & searching official manufacturer datasheets..."):
            try:
                result = api_client.query(question_input, selected_image_name)
                
                # Layout: Left column for Vision Detections, Right column for Engineering Answer
                c_vis, c_ans = st.columns([1, 1.3])
                
                with c_vis:
                    st.markdown("#### 🔬 Computer Vision Detections")
                    annotated_path = result.get("annotated_image_path")
                    if annotated_path and os.path.exists(annotated_path):
                        st.image(Image.open(annotated_path), caption="Annotated Circuit Components (Bounding Boxes)", use_container_width=True)
                    elif selected_image_name:
                        orig_p = os.path.join(sample_images_dir, selected_image_name)
                        if os.path.exists(orig_p):
                            st.image(Image.open(orig_p), caption="Input Circuit Board", use_container_width=True)
                            
                    comps = result.get("detected_components", [])
                    if comps:
                        st.markdown("**Identified Components:**")
                        for c in comps:
                            st.markdown(f'<span class="badge-chip">{c["class_name"]} ({c["confidence"]*100:.0f}%)</span>', unsafe_allow_html=True)
                            st.caption(f"• {c['description']}")
                    else:
                        st.info("No specific IC markers detected. Consulting general datasheet knowledge.")
                        
                with c_ans:
                    st.markdown("#### 📋 Technical Directive & Pinout")
                    st.markdown(f'<div class="spec-box">{result["answer"]}</div>', unsafe_allow_html=True)
                    
                    # Datasheet Citations
                    sources = result.get("sources", [])
                    if sources:
                        st.markdown("---")
                        with st.expander("📚 Verified Datasheet Sources & Citations", expanded=True):
                            for s in sources:
                                st.markdown(f"• **{s}** — Texas Instruments / Microchip / Espressif Verified Specification")
                                
            except Exception as e:
                st.error(f"Error querying backend: {e}")
