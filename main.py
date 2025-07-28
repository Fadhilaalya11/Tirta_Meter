import streamlit as st
from PIL import Image
from db import check_login
import base64
import importlib.util

st.set_page_config(page_title="TirtaWijaya App", layout="wide")

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Fungsi encode gambar
def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# ========== LOGIN PAGE ==========
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
        .stApp {{
            background-color: rgba(255,255,255,0.3);
            backdrop-filter: blur(1px);
            padding: 2rem;
            border-radius: 12px;
        }}
        [data-testid="stSidebar"] {{display: none !important;}}
        </style>
    """, unsafe_allow_html=True)

    st.image(Image.open("assets/logo.png"), width=120)
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

# ========== SETELAH LOGIN ==========
st.sidebar.markdown(f"Halo, **{st.session_state.username}** 👋")

menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Scan Watermeter",
    "Visualisasi Cluster",
    "Logout"
], index=["Dashboard", "Scan Watermeter", "Visualisasi Cluster", "Logout"].index(st.session_state.page))

st.session_state.page = menu

# Load file modul dinamis
def load_module_from_file(filepath):
    spec = importlib.util.spec_from_file_location("dynamic_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if menu == "Dashboard":
    mod = load_module_from_file("modules/0_dashboard.py")
    mod.app()

elif menu == "Scan Watermeter":
    mod = load_module_from_file("modules/1_scan_watermeter.py")
    mod.app()

elif menu == "Visualisasi Cluster":
    mod = load_module_from_file("modules/2_visualisasi_cluster.py")
    mod.app()

elif menu == "Logout":
    st.session_state.clear()
    st.rerun()
