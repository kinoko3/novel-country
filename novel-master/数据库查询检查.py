import sqlite3
conn = sqlite3.connect('tittle.db')
cursor = conn.cursor()

values = cursor.execute('''select * from title''')
for row in values:
    print("ID = ", row[0])
    print("name = ", row[1])
    print("url = ", row[2])
cursor.close()
conn.close()
