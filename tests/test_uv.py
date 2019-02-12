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
df_uv = pd.read_csv(PATH)
cpt = 0

##Testing ID
if len(df_uv["uv_ID"].unique()) ==( max(df_uv["uv_ID"])+1):
    valtest = OK
    cpt+=1
else :
    valtest = ERROR
print("ID test : {}".format(valtest))


## Testing 

sols = [
    "PRIME--2015--S2--1A-S2-PRI",
    "PRIME--2015--S2--1A-S2-PRIME",
    "SSG--2015--S1--Code UV2",
    "SSG--2015--S2--Code UV1",
    "SSG--2015--S2--Code UV0",
    "SSG--2015--S1--Code UV3",
    "SSG--2016--S2--Code UV0",
    "SSG--2016--S2--Code UV2",
    "Info--2015--S1--Code UV0",
    "Info--2015--S2--1A-S2-INF",
    "Info--2016--S1--A1-S1-INF",
    "info--2015--S1--Code UV0",
    "Informatique--2017--S1--Code UV0"
]

tmp = df_uv[(df_uv["nom_UV"] == "PRIME") | (df_uv["nom_UV"] == "SSG") | (df_uv["nom_UV"] =="Info") | (df_uv["nom_UV"] =="info") | (df_uv["nom_UV"] =="Informatique")]\
        .apply(lambda line: line["nom_UV"]+"--"+str(line["annee"])+"--"+line["semestre"]+"--"+line["code_UV"],axis=1)

for k in tmp:
    if k in sols:
        valtest = OK
    else:
        print(k)
        valtest = ERROR
        break

if(valtest == OK):
    cpt+=1
print("UV information test : {}".format(valtest))


print(Style.BRIGHT+'Test passed : {}/2'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)
