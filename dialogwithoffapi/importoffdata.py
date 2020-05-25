from parameters import CHOSENCATEGORIES
from dialogwithoffapi.extractfromrequest import Extractfromrequest


class Importoffdata():

    def __init__(self):
        pass

    def getdataset(self):

        """returns all the chosen data from OFF"""

        data = []
        for categorie in CHOSENCATEGORIES:
            a = Extractfromrequest(categorie).get()
            data = data + a
        return data
