import psycopg2


def create_connection():
    try:
        conn = psycopg2.connect("dbname=huwebshop user=postgres password=roodwailord")
        cur = conn.cursor()
        return cur, conn

    except(Exception, psycopg2.DatabaseError):
        print(psycopg2.DatabaseError)
