from random import shuffle
import sys
import os

sys.path.insert(0,"../lib")

import argparse
import pandas as pd
import numpy as np

from colors import color
from colorama import init
from colorama import Fore, Style

init()


OK = Fore.GREEN+"OK"+color.END
ERROR = Fore.RED+"ERROR"+color.END
valtest = 0

print(Style.BRIGHT+"------------------------ STARTING TEST ------------------------"+color.END)
print("Tests : Dim_CG")

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]

print("File Loaded\n-----")
df_cg = pd.read_csv(PATH)
cpt = 0

##Testing ID
if len(df_cg["cg_ID"].unique()) ==( max(df_cg["cg_ID"])+1):
    valtest = OK
    cpt+=1
else :
    valtest = ERROR

print("ID test : {}".format(valtest))

#Test des compétences
nom_present = ["Compétences en ingénierie","Compétences interpersonnelles","Compétences intra-personnelles","Compétences scientifiques et techniques"]

for k in df_cg["nom_cg"]: 
    if k in nom_present:
        valtest = OK
    else :
        valtest = ERROR
        break

if valtest == OK:
    cpt+=1


print("Nom de compétences présent : {}".format(valtest))


#Test des codeCG
rel_CG_nom = {"IG": "Compétences en ingénierie",
             "interp": "Compétences interpersonnelles",
             "intra" : "Compétences intra-personnelles",
             "ST" : "Compétences scientifiques et techniques"}

#Test des codeCG
for k in df_cg["nom_cg"]: 
    tmp =df_cg[df_cg["nom_cg"] == k]["code_cg"]
    ind = tmp.index[0]
    code_cg = tmp.loc[ind]
    if code_cg in rel_CG_nom:
        valtest = OK
    else :
        valtest = ERROR
        break

if valtest == OK:
    cpt+=1

print("Code cg présent et conforme : {}".format(valtest))



#Test des codeCG associé au bon nom
for k in df_cg["nom_cg"]: 
    tmp =df_cg[df_cg["nom_cg"] == k]["code_cg"]
    ind = tmp.index[0]
    code_cg = tmp.loc[ind]
    if rel_CG_nom[code_cg] == k:
        valtest = OK
    else :
        valtest = ERROR
        break

if valtest == OK:
    cpt+=1

print("Code cg associé au bon nom : {}".format(valtest))




print(Style.BRIGHT+'Test passed : {}/4'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)
