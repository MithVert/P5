import time
from parameters import CHOSENCATEGORIES, CHOSENGRADES
from dialogwithoffapi.openfoodrequest import Openfoodrequest
from dialogwithoffapi.validproductdata import Validproductdata


class Importoffdata():

    """Class importing the data from every chosen categories"""

    def __init__(self):

        self.data = []

    def getdataset(self):

        """returns all the chosen data from OFF and saves it in self.data"""

        if self.data:
            self.data = []

        for categorie in CHOSENCATEGORIES:

            for grade in CHOSENGRADES:
                before = time.time()
                print(
                    "Importing data :\t"+categorie+" "+grade,
                    end="\n\t\t\t\t\t"
                )
                self.data = (
                    self.data
                    + Openfoodrequest(categorie, grade).get()
                )
                after = time.time()

                while after-before < 1:
                    after = time.time()

                print("Done")

        return self.data

    def cleanupdata(self):

        self.cleanedupdata = []

        if not(self.data):
            self.getdataset()
        print("Cleaning Dataset", end="\n\t\t\t\t\t")
        for product in self.data:
            isvalid, cleanproduct = Validproductdata(product).check()
            if isvalid:
                self.cleanedupdata.append(cleanproduct)
        print("Done")
        return self.cleanedupdata
