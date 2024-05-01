import sqlite3

class User:
    def __init__(self, username, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def to_db(self): #Benutzer in die Datenbank schreiben
        connection = sqlite3.connect("Projekt-Datenbank.db") # Muss vorher angelegt werden.
        cursor = connection.cursor()
        sql = f"INSERT INTO users(username, firstname, lastname) VALUES ('{self.username}', '{self.firstname}', '{self.lastname}')"
        cursor.execute(sql)
        connection.commit()
        connection.close()

    @classmethod #aus der Datenbank Daten auslesen
    def from_db(cls, username):
        connection = sqlite3.connect("Projekt-Datenbank.db")
        cursor = connection.cursor()
        sql = f"SELECT username, firstname, lastname FROM users WHERE username = '{username}'"
        cursor.execute(sql)
        row = cursor.fetchone()
        connection.close()
        return User(row[0], row[1], row[2])

#user = User.from_db("testuser")
#print(user.username, user.firstname, user.lastname)

#user = User("tony", "Tony", "Stark")
#user.to_db()