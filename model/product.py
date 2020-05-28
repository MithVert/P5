from parameters import CHOSENCATEGORIESNAME, VARCHARLENGHT
import mysql.connector


class Product():

    """class representing a product"""

    def __init__(self, sqlmng, idp=None, data=None):
        self.id = idp
        self.sqlmng = sqlmng
        self.data = data

    def insertproduct(self):

        columnliststr = ""
        valuestuple = ()
        valuesstr = ""
        for column in self.data:
            columnliststr = columnliststr + column + ", "
            valuesstr = valuesstr + "%s, "
            if column == "categorie":
                valuestuple = (
                    valuestuple
                    + (CHOSENCATEGORIESNAME[self.data[column]],)
                )
            elif column == "categories":
                valuetemp = str(self.data[column])[1:-1]
                if len(valuetemp) > VARCHARLENGHT:
                    valuetemp = valuetemp[:VARCHARLENGHT]
                valuestuple = valuestuple + (valuetemp,)
            else:
                valuestuple = valuestuple + (self.data[column],)
        columnliststr = columnliststr[:-2]
        valuesstr = valuesstr[:-2]
        valuesstr
        query = (
            f"INSERT INTO Products ({columnliststr})"
            f"VALUES ({valuesstr});"
        )
        cur = self.sqlmng.cnx.cursor()
        try:
            cur.execute(query, valuestuple)
            self.sqlmng.cnx.commit()
            self.id = cur.lastrowid
        except mysql.connector.errors.ProgrammingError:
            # sometimes data have characters which interfere with MySQL Syntax
            # as for every product which isn't well configured, we just ignore
            # them
            pass

    def loadproduct(self):

        """retrieves product data from MySQL in self.data as dict"""

        query = (
            "SELECT * FROM Products "
            f"WHERE id = {self.id}"
        )
        cur = self.sqlmng.cnx.cursor(dictionary=True)
        cur.execute(query)
        self.data = [row for row in cur][0]

    def addtosubstitutes(self):

        query = (
            "INSERT INTO Substitutes (idp)"
            "VALUES (%s);"
        )
        cur = self.sqlmng.cnx.cursor()
        cur.execute(query, (self.id,))
        self.sqlmng.cnx.commit()

    def removefromsubstitutes(self):

        query = f"DELETE FROM Substitutes WHERE idp = {self.id};"
        cur = self.sqlmng.cnx.cursor()
        cur.execute(query)
        self.sqlmng.cnx.commit()

    def getinfo(self):

        return self.data
