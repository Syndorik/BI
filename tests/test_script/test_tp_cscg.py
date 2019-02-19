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
print("Tests : table_de_fait_cscg")

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]
PATH_TEST = ".\\csv_true\\ft_cscg\\"

cpt = 0
ft_cscg = pd.read_csv(PATH)

print("File Loaded\n-----")
numbers = [0,1,18,19,31,6,23,24,5,10,15,35,36,25]

for k in numbers: 
    tmp = pd.read_csv(PATH_TEST+"cs_{}.csv".format(k))
    tocompareto = ft_cscg[ft_cscg["cs_ID"] == k].reset_index().drop("index",axis=1)
    if(tocompareto.equals(tmp)):
        valtest = OK
        print("Test on std_ID = {}: {}".format(k,valtest))
        cpt += 1
    else:
        valtest = ERROR
        print("Test on std_ID = {}: {}".format(k,valtest))


print(Style.BRIGHT+'Test passed : {}/14'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)

if(cpt == 14):
    sys.exit(1)
else:
    sys.exit(0)