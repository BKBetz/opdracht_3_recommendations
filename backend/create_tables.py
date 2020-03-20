from connection import create_connection

database = create_connection()

cursor = database[0]
connection = database[1]

# create tables when u run this file

cursor.execute("DROP TABLE IF EXISTS product_recommendations CASCADE")
cursor.execute("""CREATE TABLE product_recommendations(
                    id VARCHAR PRIMARY KEY,
                    prod_id_1 VARCHAR ,
                    prod_id_2 VARCHAR ,
                    prod_id_3 VARCHAR ,
                    FOREIGN KEY (prod_id_1) REFERENCES products (id),
                    FOREIGN KEY (prod_id_2) REFERENCES products (id),
                    FOREIGN KEY (prod_id_3) REFERENCES products (id)    
                ); """)

cursor.execute("DROP TABLE IF EXISTS profile_recommendations CASCADE")
cursor.execute("""CREATE TABLE profile_recommendations(
                    profid VARCHAR PRIMARY KEY,
                    prod_id_1 VARCHAR ,
                    prod_id_2 VARCHAR ,
                    prod_id_3 VARCHAR ,
                    FOREIGN KEY (prod_id_1) REFERENCES products (id),
                    FOREIGN KEY (prod_id_2) REFERENCES products (id),
                    FOREIGN KEY (prod_id_3) REFERENCES products (id)    
                ); """)

connection.commit()
cursor.close()
connection.close()

