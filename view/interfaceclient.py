from database.productmanager import Productmanager
from database.categoriemanager import Categoriemanager
from model.product import Product
from parameters import CHOSENCATEGORIESNAME


class Interfaceclient():

    """This class generates the interface for the app on a consol.
    Every method, apart from __init__, corresponds to a 'screen' of the app"""

    def __init__(self, sqlmng):
        self.sqlmng = sqlmng
        self.pdtmng = Productmanager(sqlmng)

    def welcome(self):
        result = self.menu(
            ["Réinitialiser la Base de Données",
                "Continuer avec les données enregistrées",
                "Quitter"],
            titre=(
                "Bienvenue sur notre application pour manger plus saînement \n"
                "Souhaitez-vous"
            )
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Continuer avec les données enregistrées":
            self.sqlmng.connect()
            self.home()
        else:
            self.sqlmng.reload()
            self.home()

    def home(self):
        result = self.menu(
            ["Consulter mes substituts",
                "Chercher un nouveau substitut",
                "Quitter"],
            titre=(
                "Menu Principal \n"
                "Souhaitez-vous"
            )
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Consulter mes substituts":
            self.consultsubs()
        else:
            self.lookformaincategorie()

    def consultsubs(self):
        substitutes = self.pdtmng.getsubstitutes()
        listofsubstitutes = (
            [i["product_name"]+", "+i["generic_name"] for i in substitutes]
        )
        result = self.menu(
            listofsubstitutes
            + ["Retour", "Quitter"],
            titre="Consultation des substituts"
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Retour":
            self.home()
        else:
            self.consultsub(substitutes[result[0]]["id"])

    def consultsub(self, sub):
        substitute = Product(self.sqlmng, idp=sub)
        substitute.loadproduct()
        subdata = substitute.getinfo()
        result = self.menu(
            [a for a in subdata]
            + ["Enlever de mes substituts"]
            + ["Retour", "Quitter"],
            titre=(
                "Consultation du substitut {}".format(subdata["product_name"])
            )
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Retour":
            self.home()
        elif result[1] == "Enlever de mes substituts":
            substitute.removefromsubstitutes()
            self.home()
        else:
            print(subdata[result[1]])
            self.consultsub(substitute.id)

    def lookformaincategorie(self):
        listmenu = [CHOSENCATEGORIESNAME[i] for i in CHOSENCATEGORIESNAME]
        result = self.menu(
            listmenu + ["Retour", "Quitter"],
            titre=(
                "Sélectionnez une catégorie "
                "dans laquelle chercher un substitut"
            )
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Retour":
            self.home()
        else:
            self.lookforcategories(result[1])

    def lookforcategories(self, categorie):
        catmng = Categoriemanager(self.sqlmng)
        categories = catmng.getcategories(categorie)
        listofcategories = [i["categorie"] for i in categories]
        result = self.menu(
            listofcategories + ["Retour", "Quitter"],
            titre=(
                "Sélectionnez une sous-catégorie "
                "dans laquelle chercher un substitut"
            )
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Retour":
            self.home()
        else:
            self.lookforproducts(categories[result[0]])

    def lookforproducts(self, categorie):
        pdtmng = Productmanager(self.sqlmng)
        products = pdtmng.getproductswithcategorie(categorie["id"])
        listofproducts = [i["product_name"] for i in products]
        result = self.menu(
            listofproducts + ["Retour", "Quitter"],
            titre=(
                "Sélectionnez un produit "
                "à ajouter comme substitut"
            )
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Retour":
            self.home()
        else:
            self.consultpotentialsub(products[result[0]]["id"])

    def consultpotentialsub(self, pdtid):
        substitute = Product(self.sqlmng, idp=pdtid)
        substitute.loadproduct()
        subdata = substitute.getinfo()
        result = self.menu(
            [a for a in subdata]
            + ["Ajouter en substitut"]
            + ["Retour", "Quitter"],
            titre=(
                "Consultation du produit {}".format(subdata["product_name"])
            )
        )
        if result[1] == "Quitter":
            self.goodbye()
        elif result[1] == "Retour":
            self.home()
        elif result[1] == "Ajouter en substitut":
            substitute.addtosubstitutes()
            self.home()
        else:
            print(subdata[result[1]])
            self.consultsub(substitute.id)

    def goodbye(self):
        print("Au Revoir")
        self.sqlmng.disconnect()

    def menu(self, listofchoices, titre=None):
        while True:
            if titre:
                print(titre)
            for i, choice in enumerate(listofchoices):
                print(f"\t[{i}] {choice}")
            userchoice = input("Votre choix: ")
            try:
                userchoice = int(userchoice)
                if userchoice < len(listofchoices):
                    return userchoice, listofchoices[userchoice]
                else:
                    self.err()
            except ValueError:
                self.err()

    def err(self):
        print("Merci de n'utiliser que les commandes précisées entre crochets")
