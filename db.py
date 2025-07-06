import mysql.connector
from datetime import datetime

# Ganti dengan konfigurasi MySQL kamu
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="tirtawijaya"       
    )

# Login Check
def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

# Ambil data nomor sambung
def get_no_sambung():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT no_sambung, nama FROM pelanggan")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Ambil harga per kubik
def get_harga_per_kubik(no_sambung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT harga_per_kubik FROM pelanggan WHERE no_sambung = %s", (no_sambung,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

# Simpan record ke database
def simpan_record(username, no_sambung, path_gambar, hasil, kubikasi, harga):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """
        INSERT INTO meteran_record (username, no_sambung, tanggal, path_gambar, hasil_angka, kubikasi, total_harga)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (username, no_sambung, now, path_gambar, hasil, kubikasi, harga))
    conn.commit()
    cursor.close()
    conn.close()

# Ambil semua record
def ambil_semua_record():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, username, no_sambung, tanggal, path_gambar, hasil_angka, kubikasi, total_harga
        FROM meteran_record
        ORDER BY tanggal DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
