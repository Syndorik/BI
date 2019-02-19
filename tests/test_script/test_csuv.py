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
print("Tests : table_de_fait_csuv")

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]
PATH_TEST = ".\\csv_true\\csuv\\"

cpt = 0
ft_csuv = pd.read_csv(PATH)

print("File Loaded\n-----")


if(len(ft_csuv) == 78 ):
    valtest = OK
    print("Test on length : {}".format(valtest))
    cpt += 1
else:
    valtest = ERROR
    print("Test on length : {}".format(valtest))

if(ft_csuv["nb_jetons"].unique() == 4 ):
    valtest = OK
    print("Test on length : {}".format(valtest))
    cpt += 1
else:
    valtest = ERROR
    print("Test on length : {}".format(valtest))


print(Style.BRIGHT+'Test passed : {}/2'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)

if(cpt == 2):
    sys.exit(1)
else:
    sys.exit(0)