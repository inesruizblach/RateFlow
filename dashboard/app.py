import streamlit as st
import pandas as pd
import sqlite3
import altair as alt
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RateFlow Dashboard",
    page_icon="💱",
    layout="wide"
)

st.title("💱 RateFlow: Currency Exchange Dashboard")
st.caption("Visualizing live exchange rate trends powered by your ETL pipeline.")

# --- LOAD DATA ---
DB_PATH = "../data/exchange_rates.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM exchange_rates", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No data available yet. Run the ETL pipeline first.")
    st.stop()

# --- FILTERS ---
col1, col2 = st.columns(2)
base_currency = col1.selectbox("Base Currency", sorted(df["base"].unique()))
selected_date = col2.selectbox("Date", sorted(df["date"].unique(), reverse=True))

filtered_df = df[(df["base"] == base_currency) & (df["date"] == selected_date)]

# --- DISPLAY TABLE ---
st.subheader(f"Exchange Rates on {selected_date}")
st.dataframe(filtered_df, width='stretch')

# --- CHART ---
chart = (
    alt.Chart(filtered_df)
    .mark_bar(color="#2E86DE")
    .encode(
        x=alt.X("currency", sort=None, title="Currency"),
        y=alt.Y("rate", title=f"Exchange Rate vs {base_currency}"),
        tooltip=["currency", "rate"]
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)

# --- TIMESTAMP ---
last_updated = df["fetched_at"].max()
st.caption(f"Last updated: {last_updated}")
