from random import shuffle
import sys
import os

sys.path.insert(0,"../../lib")

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
print("Tests : Dim_Etudiant")

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]

print("File Loaded\n-----")
df_student = pd.read_csv(PATH)
cpt = 0

##Testing ID
if len(df_student["std_ID"].unique()) ==( max(df_student["std_ID"])+1):
    valtest = OK
    cpt+=1
else :
    valtest = ERROR

print("ID test : {}".format(valtest))

## Testing name

if(len(df_student[df_student["nom"] != ""]) ==   max(df_student["std_ID"])+1 ):
    valtest = OK
    cpt+=1
else:
    valtest = ERROR

print("Nom généré automatiquement test : {}".format(valtest))

## Testing surname

if(len(df_student[df_student["prenom"] != ""]) ==   max(df_student["std_ID"])+1 ):
    valtest = OK
    cpt+=1
else:
    valtest = ERROR

print("Prénom généré automatiquement test : {}".format(valtest))

## Etudiant ID

if(len(df_student["etudiantID"].unique()) ==( max(df_student["std_ID"])+1) ):
    valtest = OK
    cpt+=1
else:
    valtest = ERROR

print("Etudiant_ID généré automatiquement test : {}".format(valtest))

## Nombre total d'étudiant

if(515 ==( max(df_student["std_ID"])+1) ):
    valtest = OK
    cpt+=1
else:
    valtest = ERROR

print("Nombre total d'étudiant test : {}".format(valtest))


#Année promo exact
dic_true_sol = {
    0:2015,50:2015,100:2015,
    200:2016,250:2016,300:2016,
    400:2017,450:2017,500:2017
}
id_tests = [0,50,100,200,250,300,400,450,500]
for k in id_tests: 
    tmp = df_student[df_student["std_ID"] == k]["annee_actuelle"]
    ind = tmp.index[0]
    annee = tmp[ind]
    if(dic_true_sol[k] == annee):
        valtest = OK
    else:
        valtest = ERROR
        break
if(valtest != ERROR):
    cpt+=1

print("annee_actuelle est exact : {}\n ".format(valtest))
print(Style.BRIGHT+'Test passed : {}/6'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)

if(cpt == 6):
    sys.exit(1)
else:
    sys.exit(0)