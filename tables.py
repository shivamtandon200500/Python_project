import sqlite3

conn = sqlite3.connect('banking_system.db') 
cursor = conn.cursor()

print("Accounts : ")

cursor.execute("SELECT * FROM 'accounts';")
tables = cursor.fetchall()
for table in tables:
    print(table)

print(" ")
print("Transactions : ")

cursor.execute("SELECT * FROM 'transactions';")
tables = cursor.fetchall()
for table in tables:
    print(table)

conn.close()
