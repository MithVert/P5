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
