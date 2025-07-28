import streamlit as st
from PIL import Image
from db import check_login
import base64
import importlib.util
import os

# ========== KONFIGURASI HALAMAN ========== #
st.set_page_config(page_title="TirtaWijaya App", layout="wide", initial_sidebar_state="collapsed")

# ========== SEMBUNYIKAN SIDEBAR STREAMLIT DEFAULT ========== #
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] > div:first-child { display: none; }
    </style>
""", unsafe_allow_html=True)

# ========== INISIALISASI SESSION ========== #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"  # default halaman

# ========== FUNGSI UTILITY ========== #
def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def load_module_from_file(filepath):
    if not os.path.exists(filepath):
        st.error(f"Halaman `{filepath}` tidak ditemukan.")
        return None
    spec = importlib.util.spec_from_file_location("dynamic_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# ========== LOGIN PAGE ========== #
if not st.session_state.logged_in:
    bg_image = get_base64_of_bin_file("assets/Background.jpg")
    st.markdown(f"""
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
            background-color: rgba(255,255,255,0.3);
            backdrop-filter: blur(1px);
            padding: 2rem;
            border-radius: 12px;
        }}
        .block-container {{
            background-color: transparent !important;
        }}
        [data-testid="stSidebar"] {{display: none !important;}}
        </style>
    """, unsafe_allow_html=True)

    logo = Image.open("assets/logo.png")
    st.image(logo, width=120)
    st.markdown("<h3 style='text-align:center;'>TirtaWijaya Login</h3>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Username atau password salah.")
    st.stop()

# ========== MENU ========== #
st.sidebar.title("Menu")
st.sidebar.markdown(f"Halo, **{st.session_state.username}** 👋")

menu = st.sidebar.radio("Navigasi", [
    "Dashboard",
    "Scan Watermeter",
    "Visualisasi Cluster",
    "Logout"
], index=["Dashboard", "Scan Watermeter", "Visualisasi Cluster", "Logout"].index(st.session_state.page))

st.session_state.page = menu

# ========== PANGGIL HALAMAN ========== #
if menu == "Dashboard":
    mod = load_module_from_file("pages/0_dashboard.py")
    if mod: mod.app()

elif menu == "Scan Watermeter":
    mod = load_module_from_file("pages/1_scan_watermeter.py")
    if mod: mod.app()

elif menu == "Visualisasi Cluster":
    mod = load_module_from_file("pages/2_visualisasi_cluster.py")
    if mod: mod.app()

elif menu == "Logout":
    st.session_state.clear()
    st.success("Berhasil logout!")
    st.rerun()
