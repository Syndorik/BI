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
print("Tests : table_de_fait_Rstcs")

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]
PATH_TEST = ".\\csv_true\\ft_csnote\\"

cpt = 0
ft_csnote = pd.read_csv(PATH)

print("File Loaded\n-----")
numbers = [0,4,17,117,182,200,208,222,342,400,403,500]

for k in numbers: 
    tmp = pd.read_csv(PATH_TEST+"std_{}.csv".format(k))
    tocompareto = ft_csnote[ft_csnote["std_ID"] == k].reset_index().drop("index",axis=1)
    if(tocompareto.equals(tmp)):
        valtest = OK
        print("Test on std_ID = {}: {}".format(k,valtest))
        cpt += 1
    else:
        valtest = ERROR
        print("Test on std_ID = {}: {}".format(k,valtest))


unique = ft_csnote["std_ID"].unique()
goodlen = True
for k in unique:
    if len(ft_csnote[ft_csnote["std_ID"] == k]) != 10:
        print(k)
        goodlen = False
goodlen

if(goodlen):
    valtest = OK
    print("Test on missing lines : {}".format(valtest))
    cpt += 1
else:
    valtest = ERROR
    print("Test on missing lines : {}".format(valtest))

print(Style.BRIGHT+'Test passed : {}/13'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)

if(cpt == 13):
    sys.exit(1)
else:
    sys.exit(0)
