import psycopg2

def db():

    conn = psycopg2.connect(
        host="localhost",
        database="DB_ImageProductSearch",
        port="5432",
        user="postgres",
        password="123456789Zz.")

    cursor = conn.cursor()

    return cursor, conn