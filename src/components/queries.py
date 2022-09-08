import os

database = os.environ['AWS_DATABASE_NAME']
table = os.environ['AWS_DATABASE_TABLE']

""" Mysql Setup Related queries  """
CREATE_DATABASE = f"""CREATE DATABASE IF NOT EXISTS {database};"""

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {database}.{table} 
                    (ID int AUTO_INCREMENT PRIMARY KEY, 
                    Label varchar(255) NOT NULL UNIQUE);"""

""" APP queries """

FETCH_LABELS = f"select Label from {database}.{table};"
ADD_LABEL = f"""INSERT INTO {database}.{table} (ID ,Label) VALUES (NULL ,'{0}');"""
