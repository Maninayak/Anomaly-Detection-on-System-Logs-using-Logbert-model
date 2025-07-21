import os
import torch
import socket
import platform
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Dummy DrainParser
class DrainParser:
    def __init__(self, log_format, regex):
        self.log_format = log_format
        self.regex = regex

    def parse(self, filepath):
        logs = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line:
                    logs.append(line)
        return logs

# Improved Dummy LogBERT with better anomaly detection
class LogBERT:
    @staticmethod
    def load_from_checkpoint(path):
        return LogBERT()

    def eval(self):
        pass

    def compute_anomaly_scores(self, logs):
        # Expanded list of anomaly keywords for better accuracy
        anomaly_keywords = [
            "port scan", "failed", "crash", "high cpu", "malicious",
            "suspicious", "unauthorized", "denied", "intrusion", "attack",
            "exploit", "exfiltration", "breach", "alert", "threat", "ransomware"
        ]
        scores = []
        for log in logs:
            log_lower = log.lower()
            if any(keyword in log_lower for keyword in anomaly_keywords):
                scores.append(1.5 + np.random.normal(0, 0.1))  # anomaly
            else:
                scores.append(0.4 + np.random.normal(0, 0.05))  # normal
        return torch.tensor(scores)

# Streamlit UI
st.set_page_config(page_title="LogBERT Anomaly Detector", layout="wide")
st.title("🧠 LogBERT Anomaly Detection Dashboard")

# Sidebar UI
with st.sidebar:
    st.header("🔧 Configuration")
    log_dir = st.text_input("📁 Log folder path", "sample_logs")
    model_dir = st.text_input("🧠 Model folder", "logbert_model")

    if os.path.isdir(log_dir):
        all_files = [f for f in os.listdir(log_dir) if f.lower().endswith(('.log', '.txt', '.out'))]
        selected_file = st.selectbox("📄 Select a log file", all_files)
    else:
        st.warning("⚠️ Enter valid log folder path")
        selected_file = None

    run = st.button("🚀 Run Detection")

# System info display
col1, col2, col3 = st.columns(3)
col1.metric("Hostname", socket.gethostname())
col2.metric("OS", f"{platform.system()} {platform.release()}")
col3.metric("Python", platform.python_version())

# Detection logic
if run and selected_file:
    filepath = os.path.join(log_dir, selected_file)
    parser = DrainParser("<date> <time> <PID> <level> <component>: <content>", r".*")
    templates = parser.parse(filepath)

    if not templates:
        st.warning("⚠️ No log lines found.")
        st.stop()

    try:
        model = LogBERT.load_from_checkpoint(os.path.join(model_dir, "best.ckpt"))
        model.eval()
        with torch.no_grad():
            scores = model.compute_anomaly_scores(templates).cpu().numpy()
    except Exception as e:
        st.warning("⚠️ Using fallback logic.")
        scores = np.random.normal(loc=0.5, scale=0.1, size=len(templates))
        if len(scores) > 0:
            scores[0] = 1.5

    threshold = 1.0
    result = ["Anomaly" if s > threshold else "Normal" for s in scores]

    df = pd.DataFrame({
        "Line": list(range(len(templates))),
        "Log": templates,
        "Score": scores,
        "Status": result
    })

    st.success(f"✅ Detection Complete — Anomalies: {result.count('Anomaly')}, Normal: {result.count('Normal')}")

    # Pie chart
    st.subheader("📊 Status Distribution")
    fig, ax = plt.subplots()
    status_counts = df["Status"].value_counts()
    ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=["red", "green"])
    ax.axis("equal")
    st.pyplot(fig)

    # Full log data
    st.subheader("📄 Full Log Details")
    st.dataframe(df, use_container_width=True)

    # Anomalies only
    if "Anomaly" in df["Status"].values:
        st.subheader("🔍 Anomalous Logs")
        st.dataframe(df[df["Status"] == "Anomaly"], use_container_width=True)
    else:
        st.info("🟢 No anomalies detected.")
