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
        self.df = pd.read_excel('../table/2014/BDN_interpA-A1-S1_2014.xlsx')
        self.num_col = pd.to_numeric(self.df["Unnamed: 0"].loc[11:])
        self.max_num = self.num_col.max()
        self.ind_max = self.num_col[self.num_col == self.max_num].index[0]
        self.num_col = self.num_col.loc[:self.ind_max].apply(int)
        self.number_std = len(self.num_col)
    
    def generate_value(self):
        rd_val = self.__rdgen
        self.firstname_col = rd_val.get_firstname()
        self.lastname_col = rd_val.get_lastname()
        self.std_num_col = rd_val.get_std_num()  

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

    def preproces(self):
        # Empty columns
        col_todrop = list(self.df.loc[:,"Unnamed: 24":].columns)

        #UV name and Code UV
        self.Uv_name = list(self.df.loc[9,"Unnamed: 8":"Unnamed: 17"])
        self.code_UV = list(self.df.loc[8,"Unnamed: 8":"Unnamed: 17"])

        for k in range(len(self.Uv_name)):
            if(self.Uv_name[k] == "Niveau-Situation"):
                self.Uv_name[k] = "Niveau-Situation{}".format(k)
            if(self.code_UV[k] == "Code UV"):
                self.code_UV[k] = "Code UV{}".format(k)

        #drop empty columns
        self.df.drop(col_todrop,axis=1,inplace=True)

        #New data frame (without all the columns above)
        self.df = self.df.iloc[10:]

        #list of old columns
        self.df_col = list(self.df.iloc[0])

        #list of columns with diffrentiable name
        self.df_col = self.df_col[0:8]+self.Uv_name+self.df_col[18:]
        self.df.columns = self.df_col

        #Reseting the index, and droping useless columns
        self.df.drop(10,inplace = True)
        self.df.reset_index(inplace=True)
        self.df.drop(['IDOPUSER','IDOPSESSION',"index","Groupe","Intervenant"], axis =1, inplace= True)
        
        #Droping useless lines
        self.df = self.df.iloc[:self.number_std]
    
    def modify(self):

        #Adding generated informations
        self.df["N° Etudiant"]= self.std_num_col
        self.df["Nom"] = self.lastname_col
        self.df["Prénom"]= self.firstname_col
        UV = self.df.loc[:,"Prénom":"Moyenne"].drop(["Prénom","Moyenne"],axis = 1)

        UV.isna().apply(lambda var : self.drop_na_line(var),axis=1)
        self.df.isna().apply(lambda var : self.drop_na_col(var),axis=0)

        self.df["code_UE"] = self.code_UE
        self.df["libelle_UE"] = self.libelle_UE
        self.df["responsable_UE"] = self.responsable_UE
        self.df["annee"] = self.annee

        self.Uv_name = list(self.df.loc[:,"Prénom":"Moyenne"])
        self.Uv_name.pop(0)
        self.Uv_name.pop(-1)

        dict_uv = {}
        for k in range(len(self.Uv_name)):
            dict_uv["{}\t{}".format(self.Uv_name[k],self.code_UV[k])] = self.df[self.Uv_name[k]]
        
        nom = []
        code = []
        note = []
        for k in dict_uv:
            nom+=[k.split("\t")[0]]*len(self.df)
            code+= [k.split("\t")[1]]*len(self.df)
            note+= list(dict_uv[k])
        
        self.__new_df = pd.concat(
            [self.df for k in range(len(self.Uv_name))]).reset_index().drop(["index","N°"],
            axis =1
            )

        self.__new_df["nom_UV"] = nom
        self.__new_df["code_UV"] = code
        self.__new_df["note"] = note
        self.__new_df.drop(self.Uv_name, axis = 1)



    def drop_na_line(self,var):
        if(list(var) == [True, True, True, True, True, True, True, True, True, True]):
            self.df.drop(var.name,inplace=True)
        return

    def drop_na_col(self,var):
        tocompare = [True]*len(self.df)
        if(list(var) == tocompare):
            self.df.drop(var.name,inplace = True, axis = 1)

    def create_file(self):
        self.preproces()
        self.modify()
    
    def get_file(self):
        return self.__new_df
    

if __name__ == "__main__":
    fff = f_create('../table/2015/BDN_interpA-A1-S2-2015.xlsx',Rdgen(195))
    fff.create_file()
    fff.get_file().to_csv("example.csv",encoding = 'utf-8-sig')