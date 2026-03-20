# 🚢 CargoTrack: Enterprise Sales Intelligence

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://your-app.streamlit.app)
[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CargoTrack** is a high-performance sales analytics platform that transforms raw retail logistics data into actionable executive insights. Built with a full-stack data science workflow: from SQL-relational modeling to a high-end interactive Streamlit dashboard.

---

## 🚀 Key Features

- **Automated ELT Pipeline**: Seamless extraction from CSV to a queryable SQLite data warehouse.
- **Advanced SQL Analytics**: Leveraging Window Functions (`RANK`, `PARTITION BY`, `SUM OVER`) to identify market trends.
- **Micro-Animation Dashboard**: A premium UI experience with glassmorphism and real-time Plotly visualizations.
- **Strategic Intelligence**: Automated detection of high-discount loss zones and regional profit drivers.

## 🛠️ Tech Stack

- **Engine**: Python, SQL (SQLite)
- **Analytics**: Pandas, NumPy
- **Visuals**: Plotly, Seaborn, Matplotlib
- **App Framework**: Streamlit (Premium UI with Custom CSS)
- **Data Source**: US Superstore Dataset (9,994 Orders)

## 📊 Business Insights Extracted

1. **The Discount Paradox**: Products with >40% discounts account for the majority of the bottom-line burn.
2. **Category Performance**: *Technology* yields the highest margin (~17%), while *Furniture* leads in volume but lags in profitability.
3. **Regional Hotspots**: The **West** region is the high-growth engine of the business.
4. **Q4 Seasonality**: Significant revenue spike in October-December (Festive effect).

## 🏃 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Database Initialization
```bash
python setup_db.py
```

### 3. Launch Analysis Notebook
```bash
jupyter notebook sales_analysis.ipynb
```

### 4. Deploy Dashboard
```bash
streamlit run app.py
```

## 📂 Project Structure

```text
CargoTrack/
├── data/
│   ├── superstore.csv   # Raw Order Data
│   └── sales.db         # Cultivated SQLite Warehouse
├── app.py               # Streamlit Dashboard (Premium UI)
├── sales_analysis.ipynb # Deep-dive SQL & EDA Notebook
├── setup_db.py          # Database Build Script
├── generate_notebook.py # Meta-generator for Analysis
└── requirements.txt     # Dependency Resolution
```

---
*Developed by [Your Name]*  
*Built for the Modern Data Scientist*
