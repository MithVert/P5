from parameters import CHOSENCATEGORIES, CHOSENCOLUMNS
from dialogwithMySQL import Sqldatabase
from dialogwithOFFAPI import getalldata
from interface import choice


def main():

    while True:

        print("Bienvenue sur notre application pour manger plus saînement")
        print("Souhaitez-vous")
        userchoice = choice(
            ["Réinitialiser les Bases de Données",
                "Continuer avec les données enregistrées",
                "Quitter"])

        if userchoice[1] == "Réinitialiser les Bases de Données":
            sqldatabase = Sqldatabase()
            sqldatabase.loaddata(getalldata())

        elif userchoice[1] == "Continuer avec les données enregistrées":
            sqldatabase = Sqldatabase()
            sqldatabase.connect()

        elif userchoice[1] == "Quitter":
            break

        userchoice = choice(
            ["Consulter mes substituts",
                "Chercher un nouveau substitut"])

        if userchoice[1] == "Consulter mes substituts":

            print("Consultation des substituts")
            substituts = sqldatabase.getsubstitutes()
            listsubstituts = [i["product_name"] for i in substituts]

            for j in range(len(listsubstituts)):
                if not listsubstituts[j]:
                    listsubstituts[j] = substituts[j]["generic_name"]

            subchoice = choice(listsubstituts+["Quitter"])
            if subchoice[1] == "Quitter":
                break
            sub = substituts[subchoice[0]]
            print("Consultation d'un Substituts")
            for i in CHOSENCOLUMNS:
                print(i+":\n\t"+sub[i])

            subkeep = choice(["Conserver", "Supprimer"])
            if subkeep[1] == "Conserver":
                pass
            else:
                sqldatabase.removesub(sub["id"])

        elif userchoice[1] == "Chercher un nouveau substitut":

            print(
                "Recherche d'un nouveau substitut: choix de la categorie")
            userchoicecategorie = choice(CHOSENCATEGORIES)
            print(
                "Recherche d'un nouveau substitut: choix de la sous-categorie")
            userchoicesubcategorie = choice(
                sqldatabase.getcategorielist(userchoicecategorie[1])
            )
            productlist = sqldatabase.getlistofproducts(
                userchoicecategorie[1],
                [userchoicesubcategorie[1]]
            )
            productlistname = []
            for j in productlist:
                i = sqldatabase.getproductinfo(j)
                if not i["product_name"]:
                    productlistname.append(i["generic_name"])
                else:
                    productlistname.append(i["product_name"])
            usersubstitutechoice = choice(productlistname)
            sqldatabase.insertsubstitute(productlist[usersubstitutechoice[0]])
            print("Produit ajouté à vos substituts")
    sqldatabase.disconnect()
    print("Au Revoir")


if __name__ == "__main__":
    main()
