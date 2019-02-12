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
print("Tests : Dim_lieu")

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]

print("File Loaded\n-----")
df_cs = pd.read_csv(PATH)
cpt = 0

##Testing ID
if len(df_cs["cs_ID"].unique()) ==( max(df_cs["cs_ID"])+1):
    valtest = OK
    cpt+=1
else :
    valtest = ERROR

print("ID test : {}".format(valtest))

#Testing if cs is OK

sols = ["IGA--2015--S2--IGA : Pratique de l'ingénierie--GOSSIAUX Pol Bernard",
        "intraA--2015--S1--intraA : La personne face à elle-même--MONY Loïc",
        "intraA--2015--S2--intraA : La personne face à elle-même--MONY Loïc",
        "intraA--2016--S1--intraA : La personne face à elle-même--MONY Loïc",
        "intraA--2016--S2--intraA : La personne face à elle-même--MONY Loïc",
        "STA--2015--S1--STA : Connaissance et savoir--LEMOULT Bernard ; TABIOU Safouana ; DEBRUYNE Romuald ; SUBRENAT Albert ; THERS Dominique ; GOSSIAUX Pol Bernard ; DEVIGNE Michel ; ROUSSEAU Patricia",
        "STA--2015--S2--STA : Connaissance et savoir--LEMOULT Bernard ; TABIOU Safouana ; DOUENCE Remi ; YAGOUBI Mohamed ; DEVIGNE Michel ; BATIGNE Guillaume ; ROUSSEAU Patricia",
        "STA--2016--S1--STA : Connaissance et savoir--DEVIGNE Michel ; DOUENCE Remi ; GOSSIAUX Pol Bernard ; LEMOULT Bernard ; ROUSSEAU Patricia ; SUBRENAT Albert ; TABIOU Safouana ; THERS Dominique ; CHABERT Gilles",
        "STA--2016--S2--STA : Connaissance et savoir--BATIGNE Guillaume ; DEVIGNE Michel ; LEMOULT Bernard ; ROUSSEAU Patricia ; TABIOU Safouana ; YAGOUBI Mohamed ; DEBRUYNE Romuald",
        "STA--2017--S1--STA : Connaissance et savoir--LEMOULT Bernard ; TABIOU Safouana ; DOUENCE Remi ; SUBRENAT Albert ; THERS Dominique ; GOSSIAUX Pol Bernard ; DEVIGNE Michel ; ROUSSEAU Patricia ; CHABERT Gilles",
        "STA--2017--S2--STA : Connaissance et savoir--LEMOULT Bernard ; TABIOU Safouana ; DEBRUYNE Romuald ; YAGOUBI Mohamed ; DEVIGNE Michel ; BATIGNE Guillaume ; ROUSSEAU Patricia"
]

tmp = df_cs[(df_cs["code_cs"] == "IGA") | (df_cs["code_cs"] == "intraA") | (df_cs["code_cs"] == "STA")]\
        .apply(lambda line : line["code_cs"]+"--"+str(line["annee"])+"--"+line["semestre"]+"--"+line["nom_cs"]+"--"+line["respo_cs"],axis = 1)

for k in tmp:
    if k in sols:
        valtest = OK
    else:
        valtest = ERROR
        break

if(valtest == OK):
    cpt+=1

print("cs information test : {}".format(valtest))

#Testing if jacq is correct

jacq_dic = {"2015" : { "S1" : 
                      {"STA" : 12,
                       "STB" : 12,
                       "STC" : 4}, 
                      "S2" : 
                      {"STA" : 16,
                       "STB" : 4,
                       "STC" : 12, 
                       "IGA" : 4,
                       "IGB" : 4}
                     },
            "2016" : { "S1" : 
                      {"STA" : 12,
                       "STB" : 12,
                       "STC" : 4}, 
                      "S2" : 
                      {"STA" : 12,
                       "STB" : 4,
                       "STC" : 12}
                     },
            "2017" : { "S1" : 
                      {"STA" : 8,
                       "STB" : 8,
                       "STC" : 4}, 
                      "S2" : 
                      {"STA" : 8,
                       "STB" : 8,
                       "STC" : 4}
                     }
            
           }

#Testing for IGA
tmp = df_cs[df_cs["code_cs"] == "IGA"]["jacq"]
ind = tmp.index[0]
jac = tmp.loc[ind]

if jac == jacq_dic["2015"]["S2"]["IGA"]:
    valtest = OK
    cpt+=1
else:
    valtest = ERROR

print("jacq for IGA : {}".format(valtest))

#Testing for STA
tmpp = df_cs[df_cs["code_cs"] == "STA"]

for k in tmpp.index:
    tmp = tmpp.loc[k]
    jac = tmp["jacq"]
    ind_tps = tmp["annee"]
    ind_semestre = tmp["semestre"]
    ind_cs = tmp["code_cs"]

    if jac == jacq_dic[str(ind_tps)][ind_semestre][ind_cs]:
        valtest = OK
    else:
        valtest = ERROR

if(valtest == OK):
    cpt+=1

print("jacq for STA : {}".format(valtest))

#Testing for intraA
tmpp = df_cs[df_cs["code_cs"] == "intraA"]

for k in tmpp.index:
    tmp = tmpp.loc[k]
    jac = tmp["jacq"]
    if jac == 4:
        valtest = OK
    else:
        valtest = ERROR

if(valtest == OK):
    cpt+=1

print("jacq for intrA : {}".format(valtest))

print(Style.BRIGHT+'Test passed : {}/5'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)
