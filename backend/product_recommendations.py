from connection import create_connection
from main import search_recommended
import csv

database = create_connection()

cursor = database[0]
connection = database[1]

file = 'csv/product_recommendations.csv'


def create_product_recommendations():
    query = """SELECT * FROM products LIMIT 5000"""
    cursor.execute(query)
    rows = cursor.fetchall()
    count = 0

    with open(file, 'w', newline='') as write_file:
        writer = csv.writer(write_file, delimiter=',')
        writer.writerow(['id', 'prod_id_1', 'prod_id_2', 'prod_id_3'])
        # for each product use recommendation functions
        for row in rows:
            r_list = search_recommended('products', ['category', 'subcategory'], row)
            # when done write to file
            writer.writerow(r_list)
            # count to check progress
            count += 1
            print(count)


create_product_recommendations()

cursor.close()
connection.close()