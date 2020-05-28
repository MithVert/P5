from model.product import Product
from database.categoriemanager import Categoriemanager


class Productmanager():

    def __init__(self, sqlmng):
        self.sqlmng = sqlmng

    def insertproducts(self, data):
        print("Saving data", end="\n\t\t\t\t\t")
        for rawproduct in data:
            product = Product(self.sqlmng, data=rawproduct)
            product.insertproduct()
            catmng = Categoriemanager(self.sqlmng)
            catmng.updatecategoriesfromproductdata(product)
        print("Done")

    def getsubstitutes(self):

        query = (
            "SELECT DISTINCT id, product_name, generic_name FROM Products "
            " INNER JOIN Substitutes ON Products.id = Substitutes.idp"
        )
        cur = self.sqlmng.cnx.cursor(dictionary=True)
        cur.execute(query)
        return [row for row in cur]

    def getproductswithcategorie(self, categorieid):

        query = (
            "SELECT id, product_name FROM Products "
            "INNER JOIN Relations "
            "ON Products.id = Relations.idp "
            f"WHERE Relations.idc = {categorieid}"
        )
        cur = self.sqlmng.cnx.cursor(dictionary=True)
        cur.execute(query)
        return [row for row in cur]
