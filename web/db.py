import sqlite3 as sql

def create_table():
    con = sql.connect("database/users.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT
        )""")

    con.commit()
    con.close()

def create_table_data():
    con = sql.connect("database/TotarData.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Plates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        latitude TEXT NOT NULL,
        longitude TEXT NOT NULL,
        coordinate TEXT NOT NULL,
        address TEXT NOT NULL
        )""")

    con.commit()
    con.close()

def Register(name, username, email, password):

    con = sql.connect("database/users.db")
    cursor = con.cursor()
    cursor.execute("""INSERT INTO Users(name, username, email, password) values (?, ?, ?, ?)""",(name, username, email, password))
    con.commit()
    con.close()


def CheckUser(username):
    con = sql.connect("database/users.db")
    cursor = con.cursor()
    cursor.execute("""SELECT * FROM Users WHERE username=?""", (username,))
    result = cursor.fetchone()
    return result
    
def CheckData():
    con = sql.connect("database/TotarData.db")
    cursor = con.cursor()
    maxid = cursor.execute("""SELECT * FROM Plates""")
    result = cursor.fetchall()

    return result[-1][6].split(",")

def CheckChartData():
    con = sql.connect("database/TotarData.db")
    cursor = con.cursor()
    chartdata = cursor.execute("""SELECT date FROM Plates""") #SELECT date FROM Plates GROUP BY date HAVING COUNT(*)
    result = cursor.fetchall()

    a = list(set(result))
    a.sort()
    Data = list()
    for i in range(len(a)):
        Data.append((a[i][0],result.count(a[i])))
    
    return Data


