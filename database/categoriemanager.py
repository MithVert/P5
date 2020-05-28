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
        pass
