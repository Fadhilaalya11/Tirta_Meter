import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="Dashboard", layout="wide")

# Fungsi bantu untuk menampilkan logo di tengah
def image_to_base64(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return base64.b64encode(byte_im).decode()

# Cek apakah user sudah login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

# Sidebar
st.sidebar.title("Menu")
st.sidebar.markdown(f"Halo, **{st.session_state.username}** 👋")
menu = st.sidebar.radio("Navigasi", ["Record Data", "Logout"])

# Logo tengah + teks selamat datang
logo = Image.open("assets/logo.png")
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='assets/logo.png' width='100'>
        <h3 style='margin-top: 10px;'>TirtaWijaya Cilacap</h3>
        <h4 style='color: gray;'>Selamat Datang di Dashboard</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# Konten berdasarkan menu
if menu == "Record Data":
    st.write("📊 Di sini nanti kamu bisa melihat atau memasukkan data.")
elif menu == "Logout":
    st.session_state.logged_in = False
    st.rerun()
