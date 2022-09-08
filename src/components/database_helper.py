import mysql.connector
import sys


class MysqlConnection:
    def __init__(self):
        self.cursor = None
        self.mydb = None
        self.host = "localhost"
        self.user = "root"
        self.password = "123456"
        self.database = "ImageSearch"
        self.table = "datacollection"

    def create_connection(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            return True
        except Exception as e:
            raise e

    def setup_database(self):
        try:
            self.cursor = self.mydb.cursor()
            self.cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {self.database};""")
            self.cursor.execute(f""" CREATE TABLE IF NOT EXISTS {self.database}.{self.table} (ID int AUTO_INCREMENT 
            PRIMARY KEY, Label varchar(255) NOT NULL UNIQUE); """)
            return True
        except Exception as e:
            raise e

    def insert(self, statement):
        try:
            print(statement)
            self.cursor.execute(statement)
            self.mydb.commit()
            return True, None
        except Exception as e:
            return False, e.__class__.__name__

    def fetchall(self, statement):
        try:
            print(statement)
            self.cursor.execute(statement)
            result = self.cursor.fetchall()
            self.mydb.commit()
            return result
        except Exception as e:
            print(e.__class__.__name__)

if __name__ == "__main__":
    mysql_helper = MysqlConnection()
    mysql_helper.create_connection()
    if mysql_helper.setup_database():
        # sql = f"INSERT INTO ImageSearch.datacollection (ID ,Label) VALUES (NULL ,'label4');"
        sql = "select Label from ImageSearch.datacollection;"
        print(mysql_helper.fetchall(sql))
