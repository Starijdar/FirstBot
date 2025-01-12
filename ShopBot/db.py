import sqlite3
from random import randint

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER
)
''')

# cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

# for i in range(20):
#     cursor.execute(" INSERT INTO Users (username, email, age) VALUES (?, ?, ?) ",
#     (f"newuser{i}", f"ex{i}@gmail.com", f"{randint(25, 38)}"))

# cursor.execute("UPDATE Users SET age = ? WHERE username = ?", (24, "newuser"))

# cursor.execute("DELETE FROM Users WHERE username = ?", ("newuser2",))

# cursor.execute("SELECT * FROM Users")

# cursor.execute("SELECT username, age FROM Users WHERE age < ? ORDER BY age", (29,))

cursor.execute("SELECT age, AVG(age) FROM Users GROUP BY age")

users = cursor.fetchall()
for user in users:
    print(user)

connection.commit()
connection.close()