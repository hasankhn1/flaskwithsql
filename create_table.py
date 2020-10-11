import sqlite3

connection = sqlite3.connect('store.db')

cursor = connection.cursor()

create_table_query = 'Create table users (id integer primary key, username text, password text)'

cursor.execute(create_table_query)

create_item_table = 'Create table items (id integer not null primary key, name text not null unique, price float)'

cursor.execute(create_item_table)

connection.commit()

connection.close()
