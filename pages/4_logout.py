import streamlit as st

st.set_page_config(page_title="Logout", layout="centered", initial_sidebar_state="collapsed")

# Hapus session
st.session_state.clear()
st.success("Berhasil logout!")

# Sembunyikan sidebar dan nav
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("Redirecting to login...")
st.switch_page("login.py")
