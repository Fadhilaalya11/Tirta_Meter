import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os

# Konfigurasi halaman
st.set_page_config(page_title="Visualisasi Cluster", layout="wide")
st.title("Peta Visualisasi Klaster Pelanggan PDAM")

# ===== Path ke file (gunakan raw string atau os.path.join) =====
csv_path = r"C:\PDAM-TIRTAWIJAYA\Tirta_Meter\assets\hasil_kmeans_pelanggan (1).csv"
html_path = r"C:\PDAM-TIRTAWIJAYA\Tirta_Meter\assets\peta_cluster_pelanggan (1).html"

# ===== Tampilkan Tabel Data Pelanggan =====
try:
    df = pd.read_csv(csv_path)
    st.subheader("📄 Data Pelanggan")
    st.dataframe(df)
except FileNotFoundError:
    st.error(f"Gagal menemukan file CSV di path: {csv_path}")
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")

# ===== Tampilkan Peta HTML dari Folium =====
st.subheader("🗺️ Peta Klasterisasi")
try:
    with open(html_path, 'r', encoding='utf-8') as f:
        map_html = f.read()
    components.html(map_html, height=600)
except FileNotFoundError:
    st.error(f"Gagal menemukan file HTML di path: {html_path}")
except Exception as e:
    st.error(f"Terjadi kesalahan saat menampilkan peta: {e}")
