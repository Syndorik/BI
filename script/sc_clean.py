from random import shuffle
import sys
import os

sys.path.insert(0,"../lib")

import argparse
import pandas as pd

from file_creation import f_create
from rdgeneration import Rdgen


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()



### Getting argument
parser = argparse.ArgumentParser(description='Cleaning files')
parser.add_argument('dir', metavar='d', nargs=1,
                    help='The directory of files')

myparser = parser.parse_args()
PATH = myparser.dir[0]
####### HIERARCHY OF PATH #######
#  table
#   |------>Year1
#             |------>file1.xls
#             |------>file2.xls
#             |------>file3.xls
#   |------>Year2
#             |------>file1.xls
#             |------>file2.xls
#             |------>file3.xls
#   |------>Year3
#             |------>file1.xls
#             |------>file2.xls
#             |------>file3.xls
#   .
#   .
#   |------>YearN
#             |------>file1.xls
#             |------>file2.xls
#             |------>file3.xls
#
####### HIERARCHY OF PATH #######

dir = {}
for k in os.listdir(PATH):
    dir[k] = ["..\\table\\"+k+'\\'+l for l in os.listdir(PATH + k)]

tot=0
for k in dir:
    tot+= len(dir[k])
count = 0


dir_file = []
for annee in dir :
    number = Rdgen(f_create(dir[annee][0],Rdgen(1)).get_numrgen())
    for file in dir[annee]:
        temp = f_create(file,number)
        temp.create_file()
        dir_file.append(temp)
        count+=1
        printProgressBar(count,tot,prefix=" Status progression")
        #temp.save_file("../results/"+annee)

mycsv = pd.concat([k.get_file() for k in dir_file]).reset_index().drop(["index"],axis =1)
mycsv.to_csv("../results/final_res.csv",encoding = 'utf-8-sig')





#### Cleaning files

