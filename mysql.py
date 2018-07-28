import MySQLdb
import os
import datetime


class mysql:
    def __init__(self, config):
        self.hostname = config["hostname"]
        self.database = config["database"]
        self.username = config["username"]
        self.password = config["password"]
        self.port = config["port"]
        self.con = False
        self.connect()

    def connect(self):
        # con = MySQLdb.connect(self)
        self.con = MySQLdb.connect(
            host=self.hostname,
            user=self.username,
            passwd=str(self.password),
            db=self.database,
            port=self.port
        )

    def backup(self):
        cur = self.con.cursor()
        cur.execute("SHOW TABLES")
        data = ""
        tables = []
        for table in cur.fetchall():
            tables.append(table[0])

        for table in tables:
            data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

            cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
            data += "\n" + str(cur.fetchone()[1]) + ";\n\n"

            cur.execute("SELECT * FROM `" + str(table) + "`;")
            for row in cur.fetchall():
                data += "INSERT INTO `" + str(table) + "` VALUES("
                first = True
                for field in row:
                    if not first:
                        data += ', '
                    data += '"' + str(field) + '"'
                    first = False

                data += ");\n"
            data += "\n\n"

        return data

    def query(self, query):
        statements = query.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cur = self.con.cursor()
                cur.execute(statement+';')

        self.con.commit()
