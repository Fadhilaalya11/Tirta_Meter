import streamlit as st
from PIL import Image
from db import check_login
import base64

# Konfigurasi halaman utama
st.set_page_config(page_title="TirtaWijaya App", layout="wide")

# Inisialisasi session_state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Fungsi: encode gambar untuk background
def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ======== LOGIN SECTION ========
if not st.session_state.logged_in:
    # Background & CSS Styling
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
        background-color: rgba(255,255,255,0.3);
        backdrop-filter: blur(1px);
        padding: 2rem;
        border-radius: 12px;
    }}
    .block-container {{
        background-color: transparent !important;
    }}
    [data-testid="stSidebar"] {{display: none !important;}}
    [data-testid="stSidebarNav"] {{display: none !important;}}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Logo dan judul login
    logo = Image.open("assets/logo.png")
    st.image(logo, width=120)
    st.markdown("<h3 style='text-align:center;'>TirtaWijaya Login</h3>", unsafe_allow_html=True)

    # Form login
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

# ======== MENU SECTION (Setelah Login) ========
# Sidebar navigasi
st.sidebar.title("Menu")
st.sidebar.markdown(f"Halo, **{st.session_state.username}** 👋")

menu = st.sidebar.radio("Navigasi", [
    "Dashboard",
    "Scan Watermeter",
    "Visualisasi Cluster",
    "Logout"
])

# Navigasi ke halaman
if menu == "Dashboard":
    st.switch_page("pages/0_dashboard.py")
elif menu == "Scan Watermeter":
    st.switch_page("pages/1_scan_watermeter.py")
elif menu == "Visualisasi Cluster":
    st.switch_page("pages/2_visualisasi_cluster.py")
elif menu == "Logout":
    st.session_state.logged_in = False
    st.rerun()
