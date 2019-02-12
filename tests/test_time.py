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
print("Tests : Dim_time")

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]

print("File Loaded\n-----")
df_time = pd.read_csv(PATH)
cpt = 0

##Testing ID
if len(df_time["temps_ID"].unique()) ==( max(df_time["temps_ID"])+1):
    valtest = OK
    cpt+=1
else :
    valtest = ERROR

print("ID test : {}".format(valtest))

#Testing if every semester is in there
semester = ["2015-S1","2015-S2","2016-S1","2016-S2","2017-S1","2017-S2"]
tmp_ser =df_time.apply(lambda line : str(line["annee"])+"-"+line["semestre"],axis = 1)

for k in tmp_ser:
    if k in semester:
        valtest = OK
    else:
        valtest = ERROR
        break

if(valtest == OK):
    cpt+=1

print("Each period of the three years is present : {}".format(valtest))

print(Style.BRIGHT+'Test passed : {}/2'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)
