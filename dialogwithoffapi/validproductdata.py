from langdetect import detect, DetectorFactory
from parameters import VARCHARLENGHT

DetectorFactory.seed = 0


class Validproductdata():

    def __init__(self, product):
        self.product = product

    def validatename(self):

        """Making sure the product do have a name
        and that it is stored in product_name"""

        name = ""
        try:
            name = self.product["product_name"]
        except KeyError:
            try:
                name = self.product["generic_name"]
            except KeyError:
                self.product["generic_name"] = ""
        if name:
            if name != self.product["product_name"]:
                self.product["product_name"] = name
            return True
        else:
            return False

    def validatecategories(self):

        """Making sure the categories field is filled in French
        and making a proper list of categories out of a string"""

        hasbeencut = False
        if len(self.product["categories"]) == VARCHARLENGHT:
            hasbeencut = True

        listofcategories = self.product["categories"].split(",")

        if hasbeencut:
            listofcategories = listofcategories[:-1]

        listofvalidcategories = []

        for categorie in listofcategories:
            if ":" in categorie:
                pass
                # ":" indicates it is labelled as another language than french
            elif not(detect(categorie) == "fr"):
                pass
                # even when not labelled, it can still be in another language
            else:
                # removing spaces at beginning and ending of categorie name
                categorietemp = categorie
                while categorietemp[0] == " ":
                    categorietemp = categorietemp[1:]
                while categorietemp[-1] == " ":
                    categorietemp = categorietemp[:-1]
                listofvalidcategories.append(categorietemp)
        if listofvalidcategories:
            self.product["categories"] = listofvalidcategories
            return True, self.product
        else:
            return False, None

    def check(self):

        """only method supposed to be called outside of the class,
        returns bool, product
        where bool indicate wether the product is valid
        where product is the product with the right modifications done"""

        if self.validatename():
            return self.validatecategories()
        else:
            return False, self.product
