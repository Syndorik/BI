from random import shuffle
import sys
import os

sys.path.insert(0,"../lib")
sys.path.insert(0,"./test_script")

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

parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of tables')

myparser = parser.parse_args()
PATH = myparser.dir[0]

PATH = "..\\"+PATH


os.chdir("test_script")

list_files = {'dim_CG.csv' : "test_cg.py",
            'dim_CS.csv' : "test_cs.py",
            'dim_etudiant.csv' : "test_std.py",
            'dim_lieu.csv' : "test_lieu.py",
            'dim_temps.csv' : "test_time.py",
            'dim_UV.csv' : "test_uv.py",
            'table_de_fait_csuv.csv' : "test_csuv.py",
            'table_de_fait_notes.csv' : "test_tdfnotes.py",
            'table_de_fait_NvCgNA.csv' : "test_tdf_NvCgNA.py",
            'table_de_fait_NvCsNA.csv' : "test_tdf_NvCsNA.py",
            'table_de_fait_RstCg.csv' : "test_tdf_RstCg.py",
            'table_de_fait_RstCs.csv' : "test_tdf_RstCs.py",
            'table_passerelle_cscg.csv' : "test_tp_cscg.py"}

cpt = 0
for k in list_files:
    l = os.system("python .\\{} {}\\{}".format(list_files[k],PATH,k))
    if(l == 1):
        cpt+=1

print("###############################################################")
print("--------------------------- RESULTS ---------------------------")

if(cpt == 13):  
    print("{}{}/13{} test passed !".format(Fore.GREEN,cpt,color.END))
else:
    print("{}{}/13{} test passed !".format(Fore.RED,cpt,color.END))
