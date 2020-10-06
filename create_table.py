import sqlite3

connection = sqlite3.connect('users.db')

cursor = connection.cursor()

create_table_query = 'Create table users (id integer primary key, username text, password text)'

cursor.execute(create_table_query)

connection.commit()

connection.close()
