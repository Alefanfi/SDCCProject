from datetime import datetime, timedelta
import mysql.connector as mysql


class Dao:
    def __init__(self, host, user, passwd, db_name, tb_name):
        self.db = None
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.tb_name = tb_name
        self.createDB()

    # Creates the database and the table
    def createDB(self):

        self.db = mysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
        )

        mycursor = self.db.cursor()

        sql = "CREATE DATABASE IF NOT EXISTS mydatabase"
        mycursor.execute(sql)
        sql = "USE mydatabase"
        mycursor.execute(sql)
        sql = "CREATE TABLE IF NOT EXISTS sensors (sensor VARCHAR(255), num VARCHAR(255), date DATETIME)"
        mycursor.execute(sql)

    # Inserts new values taken from a dictionary
    def insertValue(self, values):
        dbcursor = self.db.cursor()

        sql = "INSERT INTO sensors (sensor, num, date) VALUES (%s, %s, NOW())"
        for k in values:
            val = (k, values[k])

            dbcursor.execute(sql, val)

        self.db.commit()

    # Creates a dictionary with the statistics with the last 24 hours
    def getLast24h(self):
        h24 = dict()
        dbcursor = self.db.cursor()
        date = datetime.now()

        for i in range(1, 25):

            date = date - timedelta(hours=1)
            str_start = date.strftime("%Y-%m-%d %H:00:00")
            str_end = date.strftime("%Y-%m-%d %H:59:59")

            hour = date.hour
            old = 0
            h24.update({hour: old})

            val = (str_start, str_end)
            sql = "SELECT * FROM sensors WHERE date BETWEEN %s AND %s"
            dbcursor.execute(sql, val)

            for row in dbcursor.fetchall():
                new = old + int(row[1])
                h24.update({hour: new})

        dbcursor.close()

        return h24
