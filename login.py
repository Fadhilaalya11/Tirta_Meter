import streamlit as st
from PIL import Image
from db import check_login

st.set_page_config(page_title="Login", layout="centered")

# Tampilkan logo
logo = Image.open("assets/logo.png")
st.image(logo, width=100)
st.markdown("<h4 style='text-align: center;'>TirtaWijaya Cilacap</h4>", unsafe_allow_html=True)

# Form login
st.subheader("LOGIN")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.button("Login"):
    if check_login(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Login berhasil! Mengarahkan ke dashboard...")
        st.rerun()
    else:
        st.error("Username atau password salah.")

# Jika sudah login, pindah ke home
if st.session_state.logged_in:
    st.switch_page("pages/home.py")


