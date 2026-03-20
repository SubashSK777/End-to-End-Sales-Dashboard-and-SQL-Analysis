import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
import requests
from streamlit_lottie import st_lottie

# ── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard + SQL Analysis",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ── Animation Loader ──────────────────────────────────────────
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Dynamic Lottie Assets (Fallback managed)
lottie_ship = load_lottieurl("https://lottie.host/7604506c-897c-4740-9e0c-8d13e3164478/9vV4K6U8R8.json")
lottie_stats = load_lottieurl("https://lottie.host/38316ce3-8902-45e0-94e8-8b9cbd38515c/o6j8zI50yT.json")
lottie_success = load_lottieurl("https://lottie.host/8816ce33-c902-45e0-94e8-8b9cbd38515c/success.json") # Generic success path

# ── Custom CSS for Ultra-Premium Look ──────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container with subtle mesh gradient */
    .stApp {
        background-color: #0c0b1a;
        background-image: 
            radial-gradient(at 0% 0%, hsla(245, 90%, 15%, 1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(220, 80%, 10%, 1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(260, 70%, 15%, 1) 0, transparent 50%);
        color: #ffffff;
    }
    
    /* Premium Glassmorphism Header */
    .premium-header {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 3rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        animation: slideInDown 1s cubic-bezier(0.19, 1, 0.22, 1);
    }
    
    .premium-header h1 {
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #AFA9EC, #ffffff, #7F77DD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem;
    }

    /* Animated KPI Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        padding: 1.8rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: left;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        background: rgba(255, 255, 255, 0.06);
        border-color: #7F77DD;
        box-shadow: 0 15px 45px rgba(127, 119, 221, 0.2);
    }

    .metric-card::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(127, 119, 221, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s;
    }

    .metric-card:hover::after {
        opacity: 1;
    }

    /* Section Highlighters */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-left: 1rem;
        border-left: 5px solid #7F77DD;
    }

    /* Large Super-Cool Neon Custom Cursor */
    html, body, .stApp {
        cursor: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 32 32' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='16' cy='16' r='14' stroke='%237F77DD' stroke-width='1.5' stroke-opacity='0.4' /%3E%3Ccircle cx='16' cy='16' r='9' stroke='%23AFA9EC' stroke-width='2' /%3E%3Ccircle cx='16' cy='16' r='2.5' fill='white' /%3E%3C/svg%3E") 16 16, auto !important;
    }

    /* Standard Interactive Hover Glows */
    button, [data-testid="stSidebarNav"] div, .metric-card {
        transition: all 0.3s ease-in-out !important;
    }
    
    a:hover, button:hover {
        text-shadow: 0 0 10px rgba(127, 119, 221, 0.5);
        color: #AFA9EC !important;
    }

    /* Animations */
    @keyframes slideInDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .fade-in {
        animation: fadeIn 1.5s ease-in;
    }

    /* Filter Icons Labeling */
    .filter-label {
        font-weight: 600;
        color: #AFA9EC;
        margin-top: 1rem;
    }

    /* Chart Containers */
    .chart-box {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 24px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    /* Remove default Streamlit padding for edge-to-edge feel */
    .main .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    [data-testid="stSidebarNav"] {
        padding-top: 0rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 0rem !important;
        gap: 0.5rem !important;
    }

    .stMultiSelect div[role="listbox"] {
        background: rgba(255,255,255,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Data Core ─────────────────────────────────────────────
@st.cache_data
def load_data():
    db_path = "data/sales.db"
    csv_path = "data/superstore.csv"

    # FORCE REBUILD if DB column naming needs update (KeyError fix)
    force_rebuild = False
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            test_df = pd.read_sql("SELECT * FROM sales LIMIT 1", conn)
            conn.close()
            if 'Sub_Category' not in test_df.columns:
                force_rebuild = True
        except:
            force_rebuild = True

    if force_rebuild and os.path.exists(db_path):
        os.remove(db_path)

    # Auto-generate Database from CSV
    if not os.path.exists(db_path) and os.path.exists(csv_path):
        df_raw = pd.read_csv(csv_path, encoding='latin-1')
        df_raw['Order Date'] = pd.to_datetime(df_raw['Order Date'])
        df_raw['Ship Date']  = pd.to_datetime(df_raw['Ship Date'])
        df_raw['Year']          = df_raw['Order Date'].dt.year
        df_raw['Month']         = df_raw['Order Date'].dt.month
        df_raw['Month_Name']    = df_raw['Order Date'].dt.strftime('%b')
        df_raw['Quarter']       = df_raw['Order Date'].dt.quarter
        df_raw['YearMonth']     = df_raw['Order Date'].dt.to_period('M').astype(str)
        df_raw['Days_to_Ship']  = (df_raw['Ship Date'] - df_raw['Order Date']).dt.days
        
        # Clean columns: handle both Space and Hyphen
        df_raw.columns = (df_raw.columns.str.strip()
                         .str.replace(' ', '_', regex=False)
                         .str.replace('-', '_', regex=False))
        
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(db_path)
        df_raw.to_sql("sales", conn, if_exists="replace", index=False)
        conn.close()

    if not os.path.exists(db_path):
        return pd.DataFrame()

    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()
    
    if not df.empty and 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

df = load_data()

if df.empty:
    st.error("Intelligence assets (CSV/DB) missing from 'data/' directory.")
    if lottie_stats:
        st_lottie(lottie_stats, height=200)
    st.stop()

# ── Sidebar Intelligence Panel ──────────────────────────────────
with st.sidebar:
    st.markdown('<h2 style="font-weight:800; margin-bottom:0;">SALES DASHBOARD</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#7F77DD; font-size:0.8rem;">SQL ANALYTICS ENGINE</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<p class="filter-label">📅 TEMPORAL RADAR</p>', unsafe_allow_html=True)
    year_list = sorted(df['Year'].unique())
    year = st.multiselect("Select Target Years", year_list, default=year_list)
    
    st.markdown('<p class="filter-label">🌏 GEOSPATIAL SCOPE</p>', unsafe_allow_html=True)
    region_list = df['Region'].unique()
    region = st.multiselect("Select Operations Focus", region_list, default=region_list)
    
    st.markdown('<p class="filter-label">📦 CATEGORY DEPTH</p>', unsafe_allow_html=True)
    category_list = df['Category'].unique()
    category = st.multiselect("Select Logistics Sectors", category_list, default=category_list)
    
    st.markdown("---")
    st.info("💡 Pro-Tip: Filter specific high-discount months to isolate low-margin root causes.")

# Filtering logic
filtered = df[
    df['Year'].isin(year) &
    df['Region'].isin(region) &
    df['Category'].isin(category)
]

# ── Hero Section ─────────────────────────────────────────────────
st.markdown("""
<div class="premium-header">
    <h1>SALES DASHBOARD + SQL ANALYSIS</h1>
    <p style="color: #AFA9EC; font-size: 1.2rem; font-weight: 300; letter-spacing: 2px;">
        TRANSFORMING RETAIL DATA INTO ACTIONABLE BUSINESS INTELLIGENCE
    </p>
</div>
""", unsafe_allow_html=True)

# ── Metric Grid ─────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

def styled_metric(col, label, value, prefix="", suffix="", delta=None):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #AFA9EC; font-size: 0.8rem; margin-bottom: 0.2rem; font-weight:600;">{label.upper()}</p>
            <h2 style="margin: 0; font-weight: 800; font-size: 2.2rem;">{prefix}{value}{suffix}</h2>
        </div>
        """, unsafe_allow_html=True)

styled_metric(m1, "Gross Volume", f"{filtered['Sales'].sum():,.0f}", prefix="$")
styled_metric(m2, "Net Intelligence", f"{filtered['Profit'].sum():,.0f}", prefix="$")
styled_metric(m3, "Order Velocity", f"{filtered['Order_ID'].nunique():,}")
margin = (filtered['Profit'].sum()/filtered['Sales'].sum()*100) if filtered['Sales'].sum() != 0 else 0
styled_metric(m4, "Capital Efficiency", f"{margin:.1f}", suffix="%")

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Trend Analysis Row ──────────────────────────────────────────
st.markdown('<p class="section-title">📉 MARKET VELOCITY & SECTOR SHARE</p>', unsafe_allow_html=True)
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    with st.container():
        monthly = filtered.groupby('YearMonth')['Sales'].sum().reset_index()
        fig_trend = px.area(monthly, x='YearMonth', y='Sales', markers=True,
                           template="plotly_dark",
                           title=None)
        fig_trend.update_traces(line_color='#7F77DD', fillcolor='rgba(127, 119, 221, 0.1)', 
                                 line_width=4, marker=dict(size=8, color='#ffffff'))
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45,
            margin=dict(l=0, r=0, t=10, b=0),
            height=450,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig_trend, use_container_width=True)

with row1_col2:
    cat_rev = filtered.groupby('Category')['Sales'].sum().reset_index()
    fig_pie = px.pie(cat_rev, values='Sales', names='Category', hole=0.7,
                    template="plotly_dark",
                    color_discrete_sequence=['#7F77DD','#534AB7','#AFA9EC'])
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=450,
        showlegend=False
    )
    # Center text for donut
    fig_pie.add_annotation(text="SECTOR<br>SPLIT", showarrow=False,
                          font=dict(size=20, color="#ffffff", family="Inter"))
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Comparison Row ──────────────────────────────────────────────
st.markdown('<p class="section-title">📊 GEOGRAPHIC & SEGMENT INTELLIGENCE</p>', unsafe_allow_html=True)
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    reg = filtered.groupby('Region').agg(
        Revenue=('Sales','sum'), Profit=('Profit','sum')
    ).reset_index().sort_values('Revenue', ascending=True)
    
    fig_bar = px.bar(reg, y='Region', x='Revenue', color='Profit',
                    orientation='h',
                    template="plotly_dark",
                    color_continuous_scale='Purples',
                    title=None)
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with row2_col2:
    sub = filtered.groupby('Sub_Category').agg(
        Profit=('Profit','sum')
    ).reset_index().sort_values('Profit', ascending=True)
    
    fig_sub = px.bar(sub, x='Profit', y='Sub_Category', orientation='h',
                    template="plotly_dark",
                    color='Profit',
                    color_continuous_scale='RdYlGn')
    fig_sub.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_sub, use_container_width=True)

# ── Data Expander ──────────────────────────────────────────────
st.markdown("---")
with st.expander("📡 RAW ASSET EXPLORER"):
    st.markdown('<p style="color:#AFA9EC;">Real-time access to filtered low-level logistics records.</p>', unsafe_allow_html=True)
    st.dataframe(
        filtered[['Order_ID','Order_Date','Region','Category',
                  'Sub_Category','Sales','Profit','Discount']]
        .sort_values('Sales', ascending=False)
        .head(100),
        use_container_width=True
    )

# ── Footer ─────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    if lottie_success:
        st_lottie(lottie_success, height=150, key="success_check")
    st.markdown("""
    <div style="text-align: center; color: #AFA9EC; opacity: 0.7;">
        <p>© 2026 SALES DASHBOARD + SQL ANALYSIS</p>
        <p style="font-size: 0.7rem;">RETAIL DATA ARCHITECTURE SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
