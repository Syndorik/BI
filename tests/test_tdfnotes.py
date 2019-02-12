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
parser.add_argument('dir', metavar='d', nargs=5,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]
PATH_UV =  myparser.dir[1]
PATH_CS =  myparser.dir[2]
PATH_std =  myparser.dir[3]
PATH_temps =  myparser.dir[4]


ft_notes = pd.read_csv(PATH)
df_uv = pd.read_csv(PATH_UV)
df_cs = pd.read_csv(PATH_CS)
df_std = pd.read_csv(PATH_std)
df_tps = pd.read_csv(PATH_temps)
print("File Loaded\n-----")


list_df_std = []
list_df_UV = []


list_ID_totest = [0,50,100,200,250,300,400,450,500]
list_UV= ["PRIME","SSG","Info"]

for k in list_UV:
    l = list(df_uv[df_uv["nom_UV"] ==k]["uv_ID"])
    list_df_UV.append(l)

list_df_UV = [item for sublist in list_df_UV for item in sublist]
print(list_df_UV)


for k in list_ID_totest:
    list_df_std.append(ft_notes[ft_notes["std_ID"] == k])

print(list_df_std)







cpt = 0




print("UV information test : {}".format(valtest))


print(Style.BRIGHT+'Test passed : {}/2'.format(cpt)+color.END)
print(Style.BRIGHT+"------------------------ END OF TEST ------------------------"+color.END)
