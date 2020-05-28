
class Categorie():

    def __init__(self, sqlmng, idc=None, name=None):
        self.sqlmng = sqlmng
        self.id = idc
        self.name = name

    def update(self):
        query = (
            "SELECT id, Categorie FROM Categories "
            f"WHERE Categorie = '{self.name}'"
        )
        cur = self.sqlmng.cnx.cursor(dictionary=True)
        cur.execute(query)
        result = [row for row in cur]
        if not result:
            query = (
                "INSERT INTO Categories VALUES (%s)"
            )
            value = (self.name,)
            cur = self.sqlmng.cnx.cursor()
            cur.execute(query, value)
            self.sqlmng.cnx.commit()
            self.id = cur.lastrowid
        else:
            self.id = result[0]["id"]

    def updaterelation(self, product):
        query = (
            "INSERT INTO Relations VALUES (%s, %s)"
        )
        values = (product.id, self.id)
        cur = self.sqlmng.cnx.cursor()
        cur.execute(query, values)
        self.sqlmng.cnx.commit()

    def getproducts(self):
        pass
