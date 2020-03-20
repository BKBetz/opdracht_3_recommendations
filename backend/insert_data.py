from connection import create_connection

database = create_connection()

cursor = database[0]
connection = database[1]

files = ['product_recommendations', 'profile_recommendations']

# this function runs the csv files u put in the array files


def write_to_table():
    for file in files:
        with open('csv/'+file+'.csv') as filename:
            cursor.copy_expert("COPY "+file+" FROM STDIN WITH CSV HEADER", filename)
            connection.commit()


write_to_table()

connection.commit()
cursor.close()
connection.close()
