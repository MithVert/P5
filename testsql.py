"""to be deleted"""

import mysql.connector

cnx = mysql.connector.connect(user='root')

DB_NAME = 'openfooddata'



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print("Succès")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

print(cnx)
create_database(cnx.database.cursor())

cnx.close()