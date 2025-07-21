# 🔍 LogBERT-Based Anomaly Detection on System Logs Using AI

## 📁 Folder Structure

```
log-anomaly-detector/
├── main.py
├── logbert/
│   ├── __init__.py
│   └── logbert.py
├── parser/
│   ├── __init__.py
│   └── drain.py
├── sample_logs/
│   └── dummy.log
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## 🚀 Overview

LogBERT is a Transformer-based model designed for log anomaly detection. This project simulates its behavior and provides a ready-to-extend structure with a Streamlit dashboard.

## 💡 Features

- Simulated LogBERT anomaly detection engine
- Custom Drain parser for logs
- Real-time log scoring and labeling
- Dashboard with anomaly pie chart and log views

## ⚙️ Tech Stack

- Python 3.10+
- Streamlit
- PyTorch (for mock LogBERT)
- Pandas & Matplotlib

## 🧪 Sample Flow

```
[Log File] → [DrainParser] → [LogBERT Engine] → [Anomaly Score] → [Dashboard]
```

## 🛠️ How to Run

1. Clone this repo:
```bash
git clone https://github.com/your-username/log-anomaly-detector.git
cd log-anomaly-detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run main.py
```

## 📄 License

This project is licensed under the MIT License.
