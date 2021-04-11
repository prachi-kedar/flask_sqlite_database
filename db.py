import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE students (id INT, occupancy INT)')

print("Table created successfully")
conn.close()