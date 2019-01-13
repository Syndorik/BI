import pandas as pd
import numpy as np
import random as rd
pd.options.display.max_columns = 40
print('The pandas version is {}.'.format(pd.__version__))
import hashlib
import names

class Rdgen:

    def __init__(self, number):
        self.__number = number
        self.generation()
    
    def generation(self):
        a = rd.sample(range(self.__number),self.__number)
        rd_name = [names.get_full_name().split(" ") for x in range(self.__number)]

        self.__std_num = [hashlib.sha1(bytes(x)).hexdigest()[:4] for x in a]
        self.__std_firstname = [name[0] for name in rd_name]
        self.__std_name = [name[1] for name in rd_name]
    
    def get_number(self):
        return self.__number
    
    def get_firstname(self):
        return self.__std_firstname
    
    def get_lastname(self):
        return self.__std_name

    def get_std_num(self):
        return self.__std_num
