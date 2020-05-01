from parameters import *
from dialogwithMySQL import *
from dialogwithOFFAPI import *
from interface import *

if __name__=="__main__":

    while True:

        print("Bienvenue sur notre application pour manger plus saînement")
        print("Souhaitez-vous")
        userchoice = choice(["Réinitialiser les Bases de Données", "Continuer avec les données enregistrées", "Quitter"])

        if userchoice[1] == "Réinitialiser les Bases de Données":
            sqldatabase = Sqldatabase()
            sqldatabase.loaddata(getalldata())
        
        elif userchoice[1] == "Continuer avec les données enregistrées":
            sqldatabase = Sqldatabase()
            sqldatabase.connect()
        
        elif userchoice[1] == "Quitter":
            break

        userchoice = choice(["Consulter mes substituts","Chercher un nouveau substitut"])

        if userchoice[1] == "Consulter mes substituts":
            #there is still work to be done for the people who are still alive
            pass

        elif userchoice[1] == "Chercher un nouveau substitut":

            print("Recherche d'un nouveau substitut : choix de la categorie")
            userchoicecategorie = choice(chosencategories)
            print("Recherche d'un nouveau substitut : choix de la sous-categorie")
            userchoicesubcategorie = choice(sqldatabase.getcategorielist(userchoicecategorie[1]))
            productlist = sqldatabase.getlistofproducts(userchoicecategorie[1],userchoicesubcategorie[1])
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

    print("Au Revoir")
