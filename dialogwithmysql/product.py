from parameters import CHOSENCATEGORIESNAME


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
            if column == "Categorie":
                valuestuple = (
                    valuestuple
                    + (CHOSENCATEGORIESNAME[self.data[columnliststr]],)
                )
            else:
                valuestuple = valuestuple + (self.data[column],)
        columnliststr = columnliststr[:-2]
        valuesstr = valuesstr[:-2]
        query = (
            f"INSERT INTO Products ({columnliststr})"
            f"VALUES ({valuesstr});"
        )
        cur = self.sqlmng.cnx.cursor()
        cur.execute(query, valuestuple)
        self.sqlmng.cnx.commit()
        self.id = cur.lastrowid

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
