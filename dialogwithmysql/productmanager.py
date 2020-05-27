from dialogwithmysql.product import Product


class Productmanager():

    def __init__(self, sqlmng):
        self.sqlmng = sqlmng

    def insertproducts(self, data):
        for rawproduct in data:
            product = Product(self.sqlmng, data=data)
            product.insertproduct()
