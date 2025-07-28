import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def app():
    st.title("Peta Visualisasi Klaster Pelanggan PDAM")

    csv_path = "assets/hasil_kmeans_pelanggan (1).csv"
    html_path = "assets/peta_cluster_pelanggan (1).html"

    try:
        df = pd.read_csv(csv_path)
        st.subheader("📄 Data Pelanggan")
        st.dataframe(df)
    except FileNotFoundError:
        st.error(f"Gagal menemukan file CSV di path: {csv_path}")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")

    st.subheader("🗺️ Peta Klasterisasi")
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            map_html = f.read()
        components.html(map_html, height=600)
    except FileNotFoundError:
        st.error(f"Gagal menemukan file HTML di path: {html_path}")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menampilkan peta: {e}")
