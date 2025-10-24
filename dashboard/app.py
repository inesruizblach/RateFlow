import os
import subprocess
import streamlit as st
import pandas as pd
import sqlite3
import altair as alt
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RateFlow Dashboard",
    page_icon="💱",
    layout="wide"
)

st.title("💱 RateFlow: Currency Exchange Dashboard")
st.caption("Visualizing live exchange rate trends powered by your ETL pipeline.")

# --- REFRESH BUTTON ---
if st.button("🔄 Refresh Data"):
    with st.spinner("Fetching latest exchange rates..."):
        subprocess.run(["python", "../etl/load.py"])
        time.sleep(1)
        st.success("Data refreshed successfully!")
        st.cache_data.clear()
        st.rerun()

# --- LOAD DATA ---
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/exchange_rates.db")

@st.cache_data
def load_data():
    # If DB doesn't exist, return empty DataFrame with expected columns
    if not os.path.exists(DB_PATH):
        st.warning(
            "Database not found! The ETL pipeline hasn't run yet. "
            "Click the '🔄 Refresh Data' button to fetch the first dataset."
        )
        return pd.DataFrame(columns=["currency", "rate", "base", "date", "fetched_at"])

    # If DB exists, connect and fetch data
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
st.dataframe(filtered_df, use_container_width='stretch')

# --- TOP MOVERS ---
st.subheader("📊 Top Movers Since Last Day")

# Sort by date to get previous day comparison
dates_sorted = sorted(df["date"].unique())
if len(dates_sorted) >= 2:
    latest_date = dates_sorted[-1]
    prev_date = dates_sorted[-2]

    latest = df[df["date"] == latest_date][["currency", "rate"]]
    prev = df[df["date"] == prev_date][["currency", "rate"]]
    merged = pd.merge(latest, prev, on="currency", suffixes=("_latest", "_prev"))
    merged["change_%"] = ((merged["rate_latest"] - merged["rate_prev"]) / merged["rate_prev"]) * 100

    top_movers = merged.sort_values("change_%", key=abs, ascending=False).head(5)
    st.dataframe(top_movers[["currency", "rate_latest", "change_%"]].rename(
        columns={"rate_latest": "Current Rate", "change_%": "% Change"}
    ), width="stretch")

else:
    st.info("Not enough data yet for Top Movers. Refresh on another day to build history.")

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

# --- TRENDS OVER TIME ---
st.markdown("---")
st.subheader("📈 Trends Over Time")

# Convert date column to datetime for plotting
df["date"] = pd.to_datetime(df["date"])

# Group by date and currency to get average rate (useful when multiple fetches per day)
trend_df = df.groupby(["date", "currency"], as_index=False)["rate"].mean()

# Let user pick currencies to compare
selected_currencies = st.multiselect(
    "Select currencies to visualize",
    sorted(trend_df["currency"].unique()),
    default=["EUR", "GBP", "JPY"]
)

if selected_currencies:
    trend_filtered = trend_df[trend_df["currency"].isin(selected_currencies)]

    line_chart = (
        alt.Chart(trend_filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("rate:Q", title=f"Exchange Rate vs {base_currency}"),
            color="currency:N",
            tooltip=["date", "currency", "rate"]
        )
        .properties(height=400)
    )

    st.altair_chart(line_chart, use_container_width=True)
else:
    st.info("Select at least one currency to see trends.")

st.markdown("---")
st.subheader("💰 Currency Converter")

currencies = sorted(df["currency"].unique())

col1, col2, col3 = st.columns(3)
amount = col1.number_input("Amount in USD", min_value=0.0, value=100.0)
target_currency = col2.selectbox("Convert to:", currencies)
latest_rate = df[df["currency"] == target_currency]["rate"].iloc[-1]
converted = amount * latest_rate
col3.metric(f"{amount} USD in {target_currency}", f"{converted:.2f} {target_currency}")
