import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="stocks_db",
        user="mihavana",
        password="password123",
        host="localhost",
        port="5432"
    )