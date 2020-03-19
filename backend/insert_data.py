from connection import create_connection

database = create_connection()

cursor = database[0]
connection = database[1]

file = 'csv/product_recommendations.csv'


def write_to_table():
    with open(file) as prod_r:
        cursor.copy_expert("COPY products_recommendations FROM STDIN WITH CSV HEADER", prod_r)
