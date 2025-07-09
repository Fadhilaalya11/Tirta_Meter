import streamlit as st
from PIL import Image
from db import check_login
import base64

# Fungsi untuk encode gambar ke base64
def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Konfigurasi halaman
st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")

# Tambahkan background image dari file assets
bg_image = get_base64_of_bin_file("assets/Background.jpg")
page_bg_img = f"""
<style>
body {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    height: 100vh;
}}

html, body, .stApp {{
    height: 100%;
}}

.stApp {{
    background-color: rgba(255,255,255,0.3); /* transparansi form */
    backdrop-filter: blur(1px);
    padding: 2rem;
    border-radius: 12px;
}}

.block-container {{
    background-color: transparent !important;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Sembunyikan sidebar dan nav
hide_streamlit_style = """
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Tampilkan logo
logo = Image.open("assets/logo.png")
st.image(logo, width=120)
st.markdown("<h3 style='text-align:center;'>TirtaWijaya Login</h3>", unsafe_allow_html=True)

# Inisialisasi session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Form login
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if check_login(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Login berhasil!")
        st.switch_page("pages/1_home.py")
    else:
        st.error("Username atau password salah.")
