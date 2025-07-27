import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def app():
    st.title("Peta Visualisasi Klaster Pelanggan PDAM")

    # ===== Tampilkan Tabel Data =====
    try:
        df = pd.read_csv("assets/data_clustered_with_coords.csv")
        st.subheader("📊 Data Pelanggan Terklaster")
        st.dataframe(df, use_container_width=True)
    except FileNotFoundError:
        st.error("❌ File `data_clustered_with_coords.csv` tidak ditemukan.")
        return

    # ===== Tampilkan Peta Folium (HTML) =====
    st.subheader("🗺️ Peta Klasterisasi Pelanggan")
    try:
        with open("assets/map_clustered.html", 'r', encoding='utf-8') as f:
            map_html = f.read()
        components.html(map_html, height=600)
    except FileNotFoundError:
        st.error("❌ File `map_clustered.html` tidak ditemukan.")
