import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="portfolio_db",
        user="user",
        password="password",
        host="localhost",
        port="5432"
    )