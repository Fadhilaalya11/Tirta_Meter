import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # kosong jika XAMPP tanpa password
        database="tirtawijaya"
    )

def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None
