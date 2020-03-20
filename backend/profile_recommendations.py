from connection import create_connection
from main import search_recommended
import csv

database = create_connection()

cursor = database[0]
connection = database[1]
file = 'csv/profile_recommendations.csv'


def search_profiles(r_list):
    query = """SELECT profid FROM sessions WHERE id = %s"""
    p_list = []

    for item in r_list:
        cursor.execute(query, (item, ))
        row = cursor.fetchone()
        p_list.append(row)

    return p_list


def search_products(profiles):
    query = """SELECT prodid FROM profiles_previously_viewed WHERE profid = %s LIMIT 2"""

    recommended_list = []
    prof_id = ''.join(profiles[0])
    recommended_list.append(prof_id)

    for i in range(1, len(profiles)):
        cursor.execute(query, (profiles[i], ))
        row = cursor.fetchone()
        if row is None and len(recommended_list) < 4:
            recommended_list.append(row)
        elif row not in recommended_list and len(recommended_list) < 4:
            row = ''.join(row)
            recommended_list.append(row)
        else:
            continue

    return recommended_list


def session_comparison():
    query = """SELECT * FROM sessions LIMIT 5000"""
    cursor.execute(query)
    rows = cursor.fetchall()
    count = 0

    with open(file, 'w', newline='') as write_file:
        writer = csv.writer(write_file, delimiter=',')
        writer.writerow(['profid', 'prod_id_1', 'prod_id_2', 'prod_id_3'])
        for row in rows:
            r_list = search_recommended('sessions', ['os', 'devicetype'], row)
            profiles = search_profiles(r_list)
            products = search_products(profiles)
            writer.writerow(products)
            count += 1
            print(count)


session_comparison()
