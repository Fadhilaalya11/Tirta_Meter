import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Visualisasi Cluster", layout="wide")
st.title("Peta Visualisasi Klaster Pelanggan PDAM")

# ===== Tampilkan Tabel Data =====
df = pd.read_csv("assets/data_clustered_with_coords.csv")
st.subheader("Data Pelanggan")
st.dataframe(df)

# ===== Tampilkan Peta Folium (HTML) =====
st.subheader("Peta Klasterisasi")
with open("assets/map_clustered.html", 'r', encoding='utf-8') as f:
    map_html = f.read()
components.html(map_html, height=600)
