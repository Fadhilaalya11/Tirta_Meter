import streamlit as st
from PIL import Image
from db import check_login

st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")

# Sembunyikan sidebar dan navigasi Streamlit
hide_streamlit_style = """
    <style>
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Logo
logo = Image.open("assets/logo.png")
st.image(logo, width=120)
st.markdown("<h3 style='text-align:center;'>TirtaWijaya Login</h3>", unsafe_allow_html=True)

# Session init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Form
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
