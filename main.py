import streamlit as st

st.set_page_config(page_title="TirtaWijaya App", layout="wide")

# Cek login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")

# Sidebar Navigasi HANYA ADA DI SINI
st.sidebar.title("Menu")
st.sidebar.markdown(f"Halo, **{st.session_state.username}** 👋")
menu = st.sidebar.radio("Navigasi", ["Home", "Prediksi Data", "Record Data", "Logout"])

if menu == "Home":
    st.switch_page("pages/1_home.py")
elif menu == "Prediksi Data":
    st.switch_page("pages/2_prediksi_data.py")
elif menu == "Record Data":
    st.switch_page("pages/3_record_data.py")
elif menu == "Logout":
    st.session_state.logged_in = False
    st.switch_page("login.py")
