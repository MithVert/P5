"""changing the parameters here will affect the program as a whole"""

chosencategories = ("boissons","plats-prepares","biscuits-et-gateaux","produits-a-tartiner-sucres","sauces")
chosencolumns = ["product_name","generic_name","nutrition_grade_fr","stores","url","categories","categorie"]
chosengrades = ("a","b")
databasename = "openfooddata"
#credentialspath is the json file storing the value for "host", "user" and "password" to access MySQL Database with privilege granted to {databasename}.*
credentialspath = "/home/gery/Documents/OC/P5Global/credentials.json"
varchar_length = 200
#n is the number of products we get from the API for each request we send
n = 50