import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS readings(id real PRIMARY KEY, t NUMERIC,V NUMERIC,s NUMERIC,TP NUMERIC,RF NUMERIC,Wz NUMERIC,sum NUMERIC,Ga NUMERIC,GWi NUMERIC,GWi1000 NUMERIC, GWz1000 NUMERIC)"

cursor.execute(create_table)

# create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
# cursor.execute(create_table)

cursor.execute("INSERT INTO items VALUES(1, 2,3,4,5,6,7,8,9,10,11,12)")


connection.commit()

connection.close()
