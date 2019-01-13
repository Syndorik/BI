#Creating a cleaned file

import pandas as pd
import numpy as np
import random as rd
pd.options.display.max_columns = 400
print('The pandas version is {}.'.format(pd.__version__))
import hashlib
from rdgeneration import Rdgen
pd.options.mode.chained_assignment = None 


class f_create:

    def __init__(self, file, rdgen):
        self.__file = file
        self.__rdgen = rdgen
        self.getinfo()
        self.general_value()
        self.generate_value()

    def getinfo(self):
        self.df = pd.read_excel('./table/2015/BDN_interpA-A1-S2-2015.xlsx')
        self.num_col = pd.to_numeric(self.df["Unnamed: 0"].loc[11:])
        self.max_num = self.num_col.max()
        self.ind_max = self.num_col[self.num_col == self.max_num].index[0]
        self.num_col = self.num_col.loc[:self.ind_max].apply(int)
        self.number_std = len(self.__num_col)
    
    def generate_value(self):
        self.firstname_col = self.__rd_val.get_firstname()
        self.lastname_col = self.__rd_val.get_lastname()
        self.std_num_col = self.__rd_val.get_std_num()  

    def general_value(self):
        self.code_UE = self.df["Relevé de notes"].iloc[3]
        self.libelle_UE = self.df["Relevé de notes"].iloc[4]
        self.responsable_UE = self.df["Relevé de notes"].iloc[5]
        self.annee = self.df["Relevé de notes"].iloc[1]
    
    ### Dealing with UV columns
    #    - nom_cours
    #    - note_cours
    #    - moyenne
    #    - grade_atteint
    #    - grade_ects

    def prepare_dataset(self):
        col_todrop = list(self.df.loc[:,"Unnamed: 24":].columns)
        Uv_name = list(df.loc[9,"Unnamed: 8":"Unnamed: 17"])
        for k in range(len(Uv_name)):
        if(Uv_name[k] == "Niveau-Situation"):
            Uv_name[k] = "Niveau-Situation{}".format(k)
            
        df.drop(col_todrop,axis=1,inplace=True)



    



    def create_file(self):
        pass