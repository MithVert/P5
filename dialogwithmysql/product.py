from langdetect import detect, DetectorFactory
from parameters import CHOSENCOLUMNS

DetectorFactory.seed = 0

class Product():

    """class representing a product"""

    def __init__(self, dataasdict):
        self.dict = dataasdict
        self.iscleaned = False
        self.isusable = False
    
    def cleanup(self):
        
