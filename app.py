import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# ── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="CargoTrack | Premium Sales Analytics",
    layout="wide",
    page_icon="🛳️",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for Premium Look ──────────────────────────────────
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Header Container */
    .main-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        text-align: center;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: transform 0.3s ease, background 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.07);
        border-color: #7F77DD;
    }

    /* Animations */
    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 12, 41, 0.9) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    db_path = "data/sales.db"
    if not os.path.exists(db_path):
        return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

df = load_data()

if df.empty:
    st.error("No data found! Please run 'setup_db.py' first.")
    st.stop()

# ── Sidebar Filter System ───────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/cargo-ship.png", width=100)
    st.title("🎛️ Control Center")
    st.markdown("---")
    
    year_list = sorted(df['Year'].unique())
    year = st.multiselect("📅 Select Years", year_list, default=year_list)
    
    region_list = df['Region'].unique()
    region = st.multiselect("🌏 Select Regions", region_list, default=region_list)
    
    category_list = df['Category'].unique()
    category = st.multiselect("📦 Select Categories", category_list, default=category_list)
    
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit & Plotly")

# Filtered Data
filtered = df[
    df['Year'].isin(year) &
    df['Region'].isin(region) &
    df['Category'].isin(category)
]

# ── Header ─────────────────────────────────────────────────
st.markdown('<div class="main-header"><h1>📊 CARGOTRACK ANALYTICS</h1><p style="color: #AFA9EC;">End-to-End Enterprise Sales Intelligence Dashboard</p></div>', unsafe_allow_html=True)

# ── KPI Row ─────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

def kpi_card(col, title, value, prefix="", suffix=""):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <p style="color: #AFA9EC; font-size: 0.9rem; margin-bottom: 0.2rem;">{title}</p>
            <h2 style="margin: 0;">{prefix}{value}{suffix}</h2>
        </div>
        """, unsafe_allow_html=True)

kpi_card(k1, "Total Revenue", f"{filtered['Sales'].sum():,.0f}", prefix="$")
kpi_card(k2, "Total Profit", f"{filtered['Profit'].sum():,.0f}", prefix="$")
kpi_card(k3, "Total Orders", f"{filtered['Order_ID'].nunique():,}")
margin = (filtered['Profit'].sum()/filtered['Sales'].sum()*100) if filtered['Sales'].sum() != 0 else 0
kpi_card(k4, "Profit Margin", f"{margin:.1f}", suffix="%")

st.markdown("<br>", unsafe_allow_html=True)

# ── Main Analytics Section ─────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Monthly Revenue Trend")
    monthly = filtered.groupby('YearMonth')['Sales'].sum().reset_index()
    fig = px.line(monthly, x='YearMonth', y='Sales', markers=True,
                  template="plotly_dark")
    fig.update_traces(line_color='#7F77DD', line_width=3, marker_size=8)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45,
        margin=dict(l=20, r=20, t=20, b=20),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🥧 Revenue by Category")
    cat_rev = filtered.groupby('Category')['Sales'].sum().reset_index()
    fig2 = px.pie(cat_rev, values='Sales', names='Category', hole=0.5,
                  template="plotly_dark",
                  color_discrete_sequence=['#7F77DD','#1D9E75','#E85D24'])
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        showlegend=True
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Secondary Analytics Section ───────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("🗺️ Regional Performance")
    reg = filtered.groupby('Region').agg(
        Revenue=('Sales','sum'), Profit=('Profit','sum')
    ).reset_index().sort_values('Revenue', ascending=False)
    
    fig3 = px.bar(reg, x='Region', y='Revenue', color='Profit',
                  template="plotly_dark",
                  color_continuous_scale='Purples')
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📉 Profitability by Sub-Category")
    sub = filtered.groupby('Sub_Category').agg(
        Profit=('Profit','sum')
    ).reset_index().sort_values('Profit')
    
    fig4 = px.bar(sub, x='Profit', y='Sub_Category', orientation='h',
                  template="plotly_dark",
                  color='Profit',
                  color_continuous_scale='RdYlGn')
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── Data Intelligence Table ─────────────────────────────────
st.markdown("---")
with st.expander("🔍 Explore Deep Data Records"):
    st.dataframe(
        filtered[['Order_ID','Order_Date','Region','Category',
                  'Sub_Category','Sales','Profit','Discount']]
        .sort_values('Sales', ascending=False)
        .head(100),
        use_container_width=True
    )

st.markdown("""
<div style="text-align: center; color: #AFA9EC; padding: 2rem;">
    <p>© 2026 CargoTrack Intelligence - Powered by AI</p>
</div>
""", unsafe_allow_html=True)
