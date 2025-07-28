import streamlit as st
from PIL import Image
import os
import datetime
import pandas as pd
from ultralytics import YOLO
from db import simpan_record, get_no_sambung, get_harga_per_kubik, get_connection, ambil_semua_record
import numpy as np
from paddleocr import PaddleOCR

def app():
    # ============ INIT ============ #
    ocr_model = PaddleOCR(
        use_angle_cls=False,
        det=False,
        rec=True,
        rec_model_dir='inference_rec_ppocr_v4',
        use_gpu=False
    )

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("main.py")
        st.stop()
        
    with st.expander("📷 Panduan Mengambil Foto Meteran"):
        st.markdown("""
        **Berikut tips agar angka pada meteran terdeteksi dengan baik:**
        1. **Ambil gambar dari jarak dekat**, fokus pada bagian angka.
        2. **Pastikan pencahayaan cukup** – hindari bayangan atau pantulan cahaya.
        3. **Posisikan kamera sejajar** dengan angka, tidak miring.
        4. Gunakan fitur **kamera** jika memungkinkan daripada upload.
        5. Pastikan angka **tidak buram** dan tidak terhalang.
        """)

    st.title("🔢 Scan Meteran Air")

    # ============ SELECT PELANGGAN ============ #
    list_sambung = get_no_sambung()
    if not list_sambung:
        st.error("Belum ada nomor sambung di database.")
        st.stop()

    pilihan = st.selectbox("Pilih Nomor Sambung", [f"{s[0]} - {s[1]}" for s in list_sambung])
    selected_no_sambung = pilihan.split(" - ")[0]

    # ============ UPLOAD GAMBAR ============ #
    col1, col2 = st.columns(2)
    uploaded_file = col1.file_uploader("Upload Foto", type=["jpg", "png"])
    camera_photo = col2.camera_input("Ambil Foto dari Kamera")
    image_data = uploaded_file or camera_photo

    # ============ DETEKSI ANGKA ============ #
    if image_data:
        img = Image.open(image_data).convert("RGB")
        st.image(img, caption="Gambar Terunggah", use_column_width=True)

        if st.button("Deteksi Angka"):
            with st.spinner("Memproses deteksi..."):
                try:
                    model = YOLO("Yolov8_Model/best.pt")
                    results = model(img)
                    boxes = results[0].boxes

                    if boxes is None or len(boxes) == 0:
                        st.warning("⚠️ Tidak ada area angka yang terdeteksi.")
                        st.stop()

                    confidences = boxes.conf.cpu().numpy()
                    if max(confidences) < 0.85:
                        st.error(f"❌ Deteksi tidak cukup yakin (confidence: {max(confidences):.2f})")
                        st.stop()

                    best_idx = np.argmax(confidences)
                    x1, y1, x2, y2 = boxes.xyxy[best_idx].cpu().numpy().astype(int)
                    cropped_img = img.crop((x1, y1, x2, y2))
                    st.image(cropped_img, caption="Area Angka Terdeteksi", use_column_width=False)

                    cropped_np = np.array(cropped_img)
                    ocr_result = ocr_model.ocr(cropped_np, cls=False)
                    hasil_ocr = ''.join([r[1][0] for r in ocr_result[0]]) if ocr_result else ""

                    if not hasil_ocr:
                        st.error("❌ Gagal membaca angka. Silahkan mengambil ulang gambar")
                        st.stop()

                    st.session_state.hasil_ocr = hasil_ocr
                    st.session_state.image = img
                    st.markdown(f"**📌 Angka Terdeteksi (OCR):** `{hasil_ocr}`")

                except Exception as e:
                    st.error(f"Gagal mendeteksi: {e}")

    # ============ SIMPAN DATA ============ #
    def get_angka_sebelumnya(no_sambung):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hasil_angka FROM meteran_record
            WHERE no_sambung = %s
            ORDER BY tanggal DESC LIMIT 1
        """, (no_sambung,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return int(str(result[0])[:4]) if result else 0

    if "hasil_ocr" in st.session_state and st.button("Simpan ke Database"):
        try:
            angka_now = int(st.session_state.hasil_ocr[:4].lstrip("0") or "0")
            angka_sebelumnya = get_angka_sebelumnya(selected_no_sambung)
            pemakaian = max(angka_now - angka_sebelumnya, 0)
            harga_per_kubik = get_harga_per_kubik(selected_no_sambung)
            total_harga = pemakaian * harga_per_kubik

            os.makedirs("uploads", exist_ok=True)
            filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{selected_no_sambung}.jpg"
            filepath = os.path.join("uploads", filename)
            st.session_state.image.save(filepath)

            simpan_record(
                username=st.session_state.username,
                no_sambung=selected_no_sambung,
                path_gambar=filepath,
                hasil=st.session_state.hasil_ocr,
                angka_meter=angka_now,
                pemakaian=pemakaian,
                total_harga=total_harga
            )

            st.success("✅ Data berhasil disimpan!")
            st.markdown(f"📦 **Pemakaian:** `{pemakaian} m³`")
            st.markdown(f"💰 **Total Harga:** `Rp {total_harga:,.0f}`")
            del st.session_state.hasil_ocr
            del st.session_state.image

        except Exception as e:
            st.error(f"❌ Gagal menyimpan ke database: {e}")

    # ===================== TAMPILKAN HASIL RECORD ===================== #
    st.title("📋 Hasil Record Data Meteran")
    data, columns = ambil_semua_record()

    if not data or len(data) == 0:
        st.info("Belum ada data yang tercatat.")
    else:
        df = pd.DataFrame(data, columns=columns)
        st.success(f"Jumlah data tercatat: {len(df)} record")

        st.markdown("### 🔍 Filter Berdasarkan Nomor Sambung")
        selected_nosambung = st.selectbox("Pilih No Sambung", df["no_sambung"].unique())
        filtered_df = df[df["no_sambung"] == selected_nosambung]
        st.markdown(f"### 🧾 Record untuk No Sambung: `{selected_nosambung}`")
        st.dataframe(filtered_df.drop(columns=["path_gambar", "id"]), use_container_width=True)
