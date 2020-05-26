import mysql.connector
import json
from parameters import CREDENTIALSPATH, DATABASENAME, CHOSENCOLUMNS
from product import Product


class Sqldatabasemanager():

    def __init__(self):

        self.credentials = json.load(open(CREDENTIALSPATH, "r"))

    def connect(self):

        """Connect to self.database
        If self.database doesn't exist, create it before connecting"""

        try:
            self.cnx = mysql.connector.connect(
                **self.credentials, database=DATABASENAME)

        except mysql.connector.errors.DatabaseError:
            self.cnx = mysql.connector.connect(**self.credentials)
            self.createdatabase()

    def createdatabase(self):

        """Create the database DATABASENAME and connect to it
        Should only be called by <self.connect>"""

        query = f"CREATE DATABASE `{DATABASENAME}`"
        cur = self.cnx.cursor()
        cur.execute(query)
        self.cnx.commit()

        query = (
            "CREATE TABLE `Products` ( `id` SMALLINT AUTO_INCREMENT, "
        )
        self.cnx.close()
        self.connect()

    def createtableproduct(self):

        """Create the table Products"""

        query = "CREATE TABLE `Products` ( `id` SMALLINT AUTO_INCREMENT, "
        for column in CHOSENCOLUMNS:
            if query:  # to be deleted
                pass
            # work to be done

    def disconnect(self):

        self.cnx.close()

    def drop(self):

        """Delete the local database <self.database>
        Should only be called by self.load()"""

        if self.cnx:
            pass
        else:
            self.connect()

        cur = self.cnx.cursor()
        query = f"DROP DATABASE {DATABASENAME}"
        cur.execute(query)

    def load(self, data):

        """load all the data to the MySQL Database"""

        self.drop()
        self.connect()

        print("Saving data to MySQL :\t", end="\n\t\t\t\t\t")

        for productdata in data:
            product = Product(productdata, self)
            product.insertintable()

        print("Done")
