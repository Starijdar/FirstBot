import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL, 
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute("INSERT OR REPLACE INTO Users(id, username, email, age, balance) VALUES(?, ?,?,?,?)",
                   (f"{i}",f"User{i}", f"examgple{i}@gmail.com", f"{i*10}", f"1000"))

for i in range(1, 11, 2):
    cursor.execute("UPDATE Users SET balance = ? WHERE id = ? ",
                   (500, i))

for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE id = ?",
                   (i,))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))

users = cursor.fetchall()
for user in users:
    print(f'Имя:{user[0]}, Мыло:{user[1]}, Возраст:{user[2]}, Баланс:{user[3]}')

connection.commit()
connection.close()