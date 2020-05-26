class Product():

    """class representing a product"""

    def __init__(self, sqlmng, id=None, data=None):
        self.id = id
        self.sqlmng = sqlmng
        self.data = data
