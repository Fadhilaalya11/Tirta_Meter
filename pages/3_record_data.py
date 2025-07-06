import streamlit as st
import pandas as pd
import os
from db import ambil_semua_record

# CEK LOGIN
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu.")
    st.switch_page("login.py")
    st.stop()

# ISI HALAMAN
st.title("📋 Hasil Record Data Meteran")

# Ambil data dari database
data = ambil_semua_record()
if not data:
    st.info("Belum ada data yang tercatat.")
    st.stop()

# Konversi ke DataFrame
df = pd.DataFrame(data, columns=[
    "ID", "Username", "No Sambung", "Tanggal", "Path Gambar",
    "Hasil Deteksi", "Kubikasi", "Total Harga"
])

# Tampilkan tabel (tanpa Path Gambar biar rapi)
st.dataframe(df.drop(columns=["Path Gambar"]), use_container_width=True)

# Detail record
st.subheader("🖼️ Lihat Detail Record")
selected_id = st.selectbox("Pilih ID Record", df["ID"])
record = df[df["ID"] == selected_id].iloc[0]

st.markdown(f"**👤 Petugas:** `{record['Username']}`")
st.markdown(f"**🔢 No Sambung:** `{record['No Sambung']}`")
st.markdown(f"**🕒 Tanggal:** `{record['Tanggal']}`")
st.markdown(f"**📷 Hasil Deteksi:** `{record['Hasil Deteksi']}`")
st.markdown(f"**📦 Kubikasi:** `{record['Kubikasi']} m³`")
st.markdown(f"**💰 Total Harga:** `Rp {record['Total Harga']:,.0f}`")

# Tampilkan gambar kalau tersedia
if pd.notna(record["Path Gambar"]) and os.path.exists(record["Path Gambar"]):
    st.image(record["Path Gambar"], caption="Foto Meteran", use_column_width=True)
else:
    st.warning("⚠️ Gambar tidak ditemukan di folder uploads.")
