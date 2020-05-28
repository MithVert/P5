from model.categorie import Categorie


class Categoriemanager():

    def __init__(self, sqlmng):
        self.sqlmng = sqlmng

    def updatecategoriesfromproductdata(self, product):
        for categoriename in product.data["categories"]:
            categorie = Categorie(self.sqlmng, name=categoriename)
            categorie.update()
            if categorie.valid:
                categorie.updaterelation(product)

    def getcategories(self, maincategorie):

        query = (
            "SELECT DISTINCT Categories.id, "
            "Categories.categorie FROM Categories "
            "INNER JOIN Relations "
            "ON Categories.id = Relations.idc "
            "INNER JOIN Products "
            "ON Products.id = Relations.idp "
            f"WHERE Products.categorie = '{maincategorie}'"
        )

        cur = self.sqlmng.cnx.cursor(dictionary=True)
        cur.execute(query)

        return [row for row in cur]
