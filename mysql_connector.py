import mysql.connector as mysql
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
connection = mysql.connect(user='root',
                           password='1234',
                           host='127.0.0.1', port="3306")

curser = connection.cursor()
curser.execute("CREATE DATABASE embeddings DEFAULT CHARACTER SET 'utf8'")
curser.close()