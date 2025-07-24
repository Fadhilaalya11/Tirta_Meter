import streamlit as st
import pandas as pd
import plotly.express as px
from db import count_admins, count_sudah_diambil_bulan_ini, count_belum_diambil_bulan_ini, get_daftar_belum_diambil_bulan_ini

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Dashboard Pemakaian Air Pelanggan")

# ===== Bagian Informasi Singkat =====
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(f"""
        <div style="background-color:#f8d7da; padding:20px; border-radius:10px; box-shadow: 2px 2px 5px #aaa;">
            <h5 style="color:#721c24; font-weight:bold; margin-bottom:10px;">👨‍💼 DATA ADMIN</h5>
            <h1 style="color:#721c24; text-align:center;">{count_admins()}</h1>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="background-color:#d4edda; padding:20px; border-radius:10px; box-shadow: 2px 2px 5px #aaa;">
            <h5 style="color:#155724; font-weight:bold; margin-bottom:10px;">✅ SUDAH DIAMBIL</h5>
            <h1 style="color:#155724; text-align:center;">{count_sudah_diambil_bulan_ini()}</h1>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="background-color:#fff3cd; padding:20px; border-radius:10px; box-shadow: 2px 2px 5px #aaa;">
            <h5 style="color:#856404; font-weight:bold; margin-bottom:10px;">❌ BELUM DIAMBIL</h5>
            <h1 style="color:#856404; text-align:center;">{count_belum_diambil_bulan_ini()}</h1>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ===== TABEL: PELANGGAN BELUM DIAMBIL =====
belum_data, belum_cols = get_daftar_belum_diambil_bulan_ini()
df_belum = pd.DataFrame(belum_data, columns=belum_cols)

st.markdown("### 📋 Daftar Pelanggan yang Belum Diambil Bulan Ini")
if df_belum.empty:
    st.success("Semua pelanggan sudah dideteksi bulan ini 🎉")
else:
    st.dataframe(df_belum, use_container_width=True)

# ===== Visualisasi Data Pemakaian Air Tertinggi =====
st.markdown("---")
st.subheader("📊 10 Pelanggan dengan Total Pemakaian Tertinggi")

# Load data (data cluster hasil analisis sebelumnya)
data_cleaned = pd.read_csv("assets/data_clustered_with_coords.csv")

# Hitung total pemakaian
top10 = data_cleaned.groupby('nsb')['pakai'].sum().sort_values(ascending=False).head(10)
top10_df = top10.reset_index().rename(columns={'nsb': 'NSB', 'pakai': 'Total Pemakaian'})
top10_df['NSB'] = top10_df['NSB'].astype(str)

# Plot bar
fig = px.bar(
    top10_df,
    x="Total Pemakaian",
    y="NSB",
    orientation="h",
    color="Total Pemakaian",
    color_continuous_scale="Blues",
)
fig.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig, use_container_width=True)
