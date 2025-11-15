import streamlit as st
from deadlock_detector import DeadlockDetection
from rag_visualizer import build_rag, draw_and_save_rag
import joblib
import numpy as np
import os

# Page configuration
st.set_page_config(page_title="AI-Powered Deadlock Detection", layout="wide")
st.title("🛠 AI-Powered Deadlock Detection System")
st.markdown("Detect, visualize, and analyze deadlocks in multi-process systems.")

# Sidebar configuration
st.sidebar.header("System Configuration")
num_processes = st.sidebar.number_input("Number of Processes", min_value=1, max_value=8, value=3)
num_resources = st.sidebar.number_input("Number of Resources", min_value=1, max_value=8, value=3)

st.sidebar.markdown("**Available Resources:**")
available = []
for i in range(num_resources):
    val = st.sidebar.number_input(f"R{i+1}", min_value=0, value=1)
    available.append(val)

st.sidebar.markdown("---")
st.sidebar.info("Adjust number of processes, resources, and available units.")

# Input matrices
st.subheader("Input Matrices")
col1, col2 = st.columns(2)

alloc_default = [[0]*num_resources for _ in range(num_processes)]
max_default = [[2]*num_resources for _ in range(num_processes)]

with col1:
    st.markdown("### Allocation Matrix")
    alloc_text = st.text_area(
        "Comma separated, one row per line",
        value="\n".join([",".join(map(str,row)) for row in alloc_default]),
        height=150
    )

with col2:
    st.markdown("### Maximum Need Matrix")
    max_text = st.text_area(
        "Comma separated, one row per line",
        value="\n".join([",".join(map(str,row)) for row in max_default]),
        height=150
    )

# Helper: parse text into matrix
def parse_matrix(text, rows, cols):
    try:
        mat = []
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if len(lines) != rows:
            st.warning(f"Expected {rows} rows, got {len(lines)}")
            return None
        for ln in lines:
            nums = [int(x.strip()) for x in ln.split(",")]
            if len(nums) != cols:
                st.warning(f"Expected {cols} columns, got {len(nums)}")
                return None
            mat.append(nums)
        return mat
    except Exception as e:
        st.error(f"Error parsing matrix: {e}")
        return None

allocation = parse_matrix(alloc_text, num_processes, num_resources)
maximum_need = parse_matrix(max_text, num_processes, num_resources)

# Deadlock detection
detector = DeadlockDetection()

if st.button("🚀 Run Deadlock Detection") and allocation and maximum_need:
    safe_seq, deadlocked, final_avail, need_matrix = detector.detect_deadlock(
        num_processes, num_resources, allocation, maximum_need, available
    )

    col1, col2 = st.columns(2)

    with col1:
        # RAG visualization
        st.subheader("📊 Resource Allocation Graph")
        G = build_rag(num_processes, num_resources, allocation, need_matrix)
        draw_and_save_rag(G, deadlocked)
        st.image("static/rag.png", caption="Resource Allocation Graph", use_column_width=True)

    with col2:
        # Results
        if deadlocked:
            st.error(f"⚠️ Deadlock Detected! Processes: {[f'P{i+1}' for i in deadlocked]}")
        else:
            st.success(f"✅ No Deadlock! Safe Sequence: {[f'P{i+1}' for i in safe_seq]}")

# --- AI Predictor ---
st.markdown("---")
st.subheader("🤖 AI Deadlock Predictor")

try:
    model = joblib.load("ai_model.joblib")
except FileNotFoundError:
    st.warning("AI model not found. Deadlock predictor will not work.")
    model = None

if allocation and maximum_need and model:
    features = []
    for row in allocation:
        features.extend(row)
    for row in maximum_need:
        features.extend(row)
    features.extend(available)

    predicted_risk = int(model.predict_proba([features])[0][1] * 100)
    st.info(f"Predicted Deadlock Risk: {predicted_risk}%")
else:
    st.info("Provide matrices and AI model to see prediction.")

