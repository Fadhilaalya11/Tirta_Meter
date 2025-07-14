import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Dashboard Pemakaian Air Pelanggan")

# ===== Load data =====
data_cleaned = pd.read_csv("assets/data_clustered_with_coords.csv")

# ===== Hitung total pemakaian per pelanggan =====
top10 = data_cleaned.groupby('nsb')['pakai'].sum().sort_values(ascending=False).head(10)
top10_df = top10.reset_index().rename(columns={'nsb': 'NSB', 'pakai': 'Total Pemakaian'})
top10_df['NSB'] = top10_df['NSB'].astype(str)  # pastikan tidak diubah jadi notasi M

# ===== Plot interaktif =====
fig = px.bar(
    top10_df,
    x="Total Pemakaian",
    y="NSB",
    orientation="h",
    color="Total Pemakaian",
    color_continuous_scale="Blues",
    title="10 Pelanggan dengan Total Pemakaian Tertinggi"
)
fig.update_layout(yaxis=dict(autorange="reversed"))

# ===== Tampilkan di Streamlit =====
st.plotly_chart(fig, use_container_width=True)

