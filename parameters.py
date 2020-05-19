"""changing the constants here will affect the program as a whole"""

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Every vague categorie we use to fill our dataset with relevant products
# Any categorie from OFF can be added
# You can use a get request at https://fr.openfoodfacts.org/categories.json
# to see every categorie OFF provides

CHOSENCATEGORIES = (
    "boissons", "plats-prepares", "biscuits-et-gateaux",
    "produits-a-tartiner-sucres", "sauces"
)

# product_name, generic_name, categories, categorie
# MUST be part of CHOSENCOLUMNS,
# any other column which correspond to some OFF data can be added or removed

CHOSENCOLUMNS = (
    "product_name", "generic_name", "nutrition_grade_fr", "url",
    "categories", "categorie", "stores"
)

# We ensure that every substitutes we provide
# have a good nutritionnal grade

CHOSENGRADES = "a", "b"

DATABASENAME = "openfooddata"

# credentials.json is the json file storing the value for
# "host", "user" and "password" in a dictionnary to access MySQL Database
# with privilege granted to {databasename}.*

CREDENTIALSPATH = f"{dir_path}/credentials.json"

VARCHARLENGHT = 200

# N is the number of products we get
# from the API for each request we send

N = 50
