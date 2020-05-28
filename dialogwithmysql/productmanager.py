from dialogwithmysql.product import Product
from dialogwithmysql.categoriemanager import Categoriemanager


class Productmanager():

    def __init__(self, sqlmng):
        self.sqlmng = sqlmng

    def insertproducts(self, data):
        for rawproduct in data:
            product = Product(self.sqlmng, data=rawproduct)
            product.insertproduct()
            catmng = Categoriemanager(self.sqlmng)
            catmng.updatecategoriesfromproductdata(product)
