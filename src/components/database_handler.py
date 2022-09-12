import os
import sys

import mysql.connector

from src.components.queries import CREATE_DATABASE, CREATE_TABLE
from src.Exception.exception import CustomException


class MysqlConnection:
    """ Mysql Helper Class to Perform CRUD Operation"""

    def __init__(self):
        self.cursor = None
        self.mydb = None
        self.create_connection()
        self.setup_database()

    def create_connection(self):
        """
        Create Connection with remote mysql database.
        """
        try:
            self.mydb = mysql.connector.connect(
                host=os.environ["AWS_DATABASE_HOST"],
                user=os.environ["AWS_DATABASE_USERNAME"],
                password=os.environ["AWS_DATABASE_PASSWORD"],
            )
            return True
        except Exception as e:
            message = CustomException(e, sys)
            raise message.error_message

    def setup_database(self):
        """
        Setup Database with tables if not present.
        """
        try:
            self.cursor = self.mydb.cursor()
            self.cursor.execute(CREATE_DATABASE)
            self.cursor.execute(CREATE_TABLE)
            return True
        except Exception as e:
            message = CustomException(e, sys)
            raise e

    def insert(self, statement):
        """ Method to Execute Insert Statement"""
        try:
            print(statement)
            self.cursor.execute(statement)
            self.mydb.commit()
            return True, None
        except Exception as e:
            message = CustomException(e, sys)
            return False, e.__class__.__name__

    def fetchall(self, statement):
        """ Method to Execute Fetch Statement"""
        try:
            self.cursor.execute(statement)
            result = self.cursor.fetchall()
            self.mydb.commit()
            return True, result
        except Exception as e:
            return False, e.__class__.__name__
