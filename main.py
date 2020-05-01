#! /usr/bin/env python3
# coding: utf-8

from parameters import *
from dialogwithMySQL import *
from dialogwithOFFAPI import *
from interface import *

if __name__=="__main__":

    while True:

        print("Bienvenue sur notre application pour manger plus saînement")
        print("Souhaitez-vous")
        userchoice = choice(["Réinitialiser les Bases de Données", "Continuer avec les données enregistrées", "Quitter"])

        if userchoice[0] == 0:
            sqldatabase = Sqldatabase()
            sqldatabase.loaddata(getalldata())
        
        elif userchoice[0] == 1:
            sqldatabase = Sqldatabase()
            sqldatabase.connect()
        
        elif userchoice[1] == "Quitter":
            break

        userchoice = choice(["Consulter mes substituts","Chercher un nouveau substitut"])

        if userchoice[0] == 0:

            listidsubstitutes = sqldatabase.getsubstituteaslist()
            listsubstitutes = []

            for i in listidsubstitutes:

                listsubstitutes.append(sqldatabase.getproductinfo(int(i)))

            listsubstitutesname = []

            for i in listsubstitutes:

                if i[1] == "":
                    listsubstitutesname.append(i[2])
                else:
                    listsubstitutesname.append(i[1])
            
            print("Liste de vos substituts, sélectionnez celui que vous souhaitez consulter")

            userchoice_sub = choice(listsubstitutesname+["Quitter"])

            if userchoice_sub[1] == "Quitter":

                break

            substitut = listsubstitutes[userchoice_sub[0]]

            print(userchoice_sub[1])
            userchoice_sub_col = choice(chosencolumns)

            if substitut[userchoice_sub_col[1]] == "":
                print("Information manquante")
            else:
                print(substitut[userchoice_sub_col[1]])

        elif userchoice[0] == 1:

            print("Recherche d'un nouveau substitut : choix de la categorie")
            userchoicecategorie = choice(chosencategories)
            print("Recherche d'un nouveau substitut : choix de la sous-categorie")
            userchoicesubcategorie = choice(sqldatabase.getcategorielist(userchoicecategorie[1]))
            productlist = sqldatabase.getlistofproducts(userchoicecategorie[1],userchoicesubcategorie[1])
            productlistname = []
            for j in productlist:
                i = sqldatabase.getproductinfo(j)
                if i[1] == "":
                    productlistname.append(i[2])
                else:
                    productlistname.append(i[1])
            usersubstitutechoice = choice(productlistname)
            sqldatabase.insertsubstitute(productlist[usersubstitutechoice[0]])
            print("Produit ajouté à vos substituts")

    print("Au Revoir")
