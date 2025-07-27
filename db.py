import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

# Load variabel dari .env
load_dotenv()

# Koneksi ke database Railway
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
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

# Ambil daftar nomor sambung dan nama pelanggan
def get_no_sambung():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT no_sambung, nama FROM pelanggan")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Ambil harga per kubik berdasarkan no_sambung
def get_harga_per_kubik(no_sambung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT harga_per_kubik FROM pelanggan WHERE no_sambung = %s", (no_sambung,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

# Simpan record hasil deteksi
def simpan_record(username, no_sambung, path_gambar, hasil, angka_meter, pemakaian, total_harga):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """
        INSERT INTO meteran_record (
            username, no_sambung, tanggal, path_gambar, hasil_angka,
            kubikasi, pemakaian, total_harga
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        username, no_sambung, now, path_gambar, hasil,
        angka_meter, pemakaian, total_harga
    ))
    conn.commit()
    cursor.close()
    conn.close()

# Ambil semua record dari meteran_record
def ambil_semua_record():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            id,
            username,
            no_sambung,
            tanggal,
            path_gambar,
            hasil_angka,
            kubikasi,
            pemakaian,
            total_harga
        FROM meteran_record
        ORDER BY tanggal DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # ambil nama kolom otomatis
    cursor.close()
    conn.close()
    return results, columns

# Ambil hasil deteksi terakhir untuk pelanggan tertentu
def get_last_detection(no_sambung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hasil_angka FROM meteran_record
        WHERE no_sambung = %s
        ORDER BY tanggal DESC
        LIMIT 1
    """, (no_sambung,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# Hitung jumlah admin
def count_admins():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

# Hitung jumlah pelanggan yang sudah diambil bulan ini
def count_sudah_diambil_bulan_ini():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(DISTINCT no_sambung)
        FROM meteran_record
        WHERE MONTH(tanggal) = MONTH(CURDATE())
          AND YEAR(tanggal) = YEAR(CURDATE())
    """)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

# Hitung jumlah pelanggan yang belum diambil bulan ini
def count_belum_diambil_bulan_ini():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM pelanggan
        WHERE no_sambung NOT IN (
            SELECT DISTINCT no_sambung
            FROM meteran_record
            WHERE MONTH(tanggal) = MONTH(CURDATE())
              AND YEAR(tanggal) = YEAR(CURDATE())
        )
    """)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

# (Opsional) Ambil daftar pelanggan yang belum diambil bulan ini
def get_daftar_belum_diambil_bulan_ini():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM pelanggan
        WHERE no_sambung NOT IN (
            SELECT DISTINCT no_sambung
            FROM meteran_record
            WHERE MONTH(tanggal) = MONTH(CURDATE())
              AND YEAR(tanggal) = YEAR(CURDATE())
        )
    """)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return results, columns

