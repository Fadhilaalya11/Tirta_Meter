import streamlit as st
from PIL import Image
import os
import datetime
from ultralytics import YOLO
from db import simpan_record, get_no_sambung, get_harga_per_kubik
import numpy as np

# CEK LOGIN
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu.")
    st.switch_page("login.py")
    st.stop()

# ISI HALAMAN UTAMA
st.title("🔢 Scan Meteran Air")

# Ambil data sambungan
list_sambung = get_no_sambung()
if not list_sambung:
    st.error("Belum ada nomor sambung di database.")
    st.stop()

# Pilih No Sambung
pilihan = st.selectbox("Pilih Nomor Sambung", [f"{s[0]} - {s[1]}" for s in list_sambung])
selected_no_sambung = pilihan.split(" - ")[0]

# Upload atau ambil foto
col1, col2 = st.columns(2)
uploaded_file = col1.file_uploader("Upload Foto", type=["jpg", "png"])
camera_photo = col2.camera_input("Ambil Foto dari Kamera")

# Gunakan salah satu
image_data = uploaded_file or camera_photo

if image_data:
    img = Image.open(image_data)
    st.image(img, caption="Gambar Terunggah", use_column_width=True)

    if st.button("Deteksi Angka"):
        with st.spinner("Memproses deteksi..."):
            bulan = datetime.datetime.now().month
            filename = f"{bulan}_{selected_no_sambung}.jpg"
            filepath = os.path.join("uploads", filename)
            with open(filepath, "wb") as f:
                f.write(image_data.getvalue())

            model = YOLO("Yolov8_Model\best.pt")
            results = model(filepath)
            # Ambil bounding box
            boxes = results[0].boxes
            if boxes is None or len(boxes) == 0:
                st.warning("⚠️ Tidak ada area angka yang terdeteksi. Silakan foto ulang.")
                st.stop()

            # Ambil nilai confidence tertinggi
            confidences = boxes.conf.cpu().numpy()
            max_conf = max(confidences)

            # Tampilkan gambar hasil deteksi
            det_img = results[0].plot()
            st.image(det_img, caption="Deteksi Angka", use_column_width=True)

            if max_conf < 0.8:
                st.error(f"❌ Deteksi tidak cukup yakin (confidence: {max_conf:.2f}). Silakan ambil foto ulang.")
                st.stop()
                det_img = results[0].plot()
                st.image(det_img, caption="Deteksi Angka", use_column_width=True)

            # Dummy OCR
            hasil_ocr = "12345678"
            kubik = 25.4
            harga = kubik * get_harga_per_kubik(selected_no_sambung)

            simpan_record(
                username=st.session_state.username,
                no_sambung=selected_no_sambung,
                path_gambar=filepath,
                hasil=hasil_ocr,
                kubikasi=kubik,
                harga=harga
            )

            st.success("✅ Data berhasil disimpan!")
            st.markdown(f"**📌 Angka Terdeteksi:** `{hasil_ocr}`")
            st.markdown(f"**📦 Penggunaan Kubikasi:** `{kubik} m³`")
            st.markdown(f"**💰 Total Harga:** `Rp {harga:,.0f}`")
