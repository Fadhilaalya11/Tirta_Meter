import streamlit as st

st.set_page_config(page_title="TirtaWijaya App", layout="wide")

# Cek login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")

# Sidebar Navigasi
st.sidebar.title("Menu")
st.sidebar.markdown(f"Halo, **{st.session_state.username}** 👋")

menu = st.sidebar.radio("Navigasi", [
    "Dashboard",
    "Scan Watermeter",
    "Visualisasi Cluster",
    "Prediksi Data",
    "Record Data",
    "Logout"
])

# Navigasi berdasarkan label
if menu == "Dashboard":
    st.switch_page("pages/0_dashboard.py")
elif menu == "Scan Watermeter":
    st.switch_page("pages/1_scan_watermeter.py")
elif menu == "Visualisasi Cluster":
    st.switch_page("pages/2_visualisasi_cluster.py")
elif menu == "Prediksi Data":
    st.switch_page("pages/3_prediksi_data.py")
elif menu == "Record Data":
    st.switch_page("pages/4_record_data.py")
elif menu == "Logout":
    st.session_state.logged_in = False
    st.switch_page("login.py")
