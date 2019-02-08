from random import shuffle
import sys
import os

sys.path.insert(0,"../lib")

import argparse
import pandas as pd
import numpy as np

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

count = 0
tot = 0
def maj(reset = False, tot = tot):
        global count
        if reset == True:
                count =0
                printProgressBar(count,tot,prefix=" Status progression")
                count+=1
        else:
                printProgressBar(count,tot,prefix=" Status progression")
                count+=1


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

maj(reset = True, tot = tot)

dir_file = []
for annee in dir :
    number = Rdgen(f_create(dir[annee][0],Rdgen(1)).get_numrgen())
    for file in dir[annee]:
        temp = f_create(file,number)
        temp.create_file()
        dir_file.append(temp)
        maj(tot = tot)
        #temp.save_file("../results/"+annee)

mycsv = pd.concat([k.get_file() for k in dir_file]).reset_index().drop(["index"],axis =1)
mycsv.to_csv("../results/final_res.csv",encoding = 'utf-8-sig')

print("CREATING TABLES")

df = pd.read_csv("../results/final_res.csv")

tot = 12
maj(reset=True, tot = tot)

#Preparation
def get_ind(var,strr,dic,unique,printed):
    if((var[printed] in unique) and (var[printed] not in dic) ):
        dic[var[printed]] = var[strr]

df["time_year"] = df["N° Etudiant"].apply(lambda var: var.split("_")[0])
df["codeCS"] = df["code_UE"].apply(lambda var : var.split('-')[0])
df["idcss"] = df.loc[:,["responsable_UE","codeCS"]].apply(lambda var : var["codeCS"] + "-" +var["responsable_UE"], axis=1)
df["semestre"] = df["code_UE"].apply(lambda var : var.split("-")[2])
df["unicite"] = df.loc[:,["time_year","semestre"]].apply(lambda var : var["time_year"]+"-"+var["semestre"],axis = 1)


df.drop("Unnamed: 0", inplace=True, axis=1)
df.reset_index(inplace= True)
maj(tot = tot)

#Definition des jetons

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


#Dim Temps
df_tps = df.loc[:,["index","time_year","semestre"]]
df_tps["unicite"] = df.loc[:,["time_year","semestre"]].apply(lambda var : var["time_year"]+"-"+var["semestre"],axis = 1)
unique_tps = df_tps["unicite"].unique()
dic_tps = {}

l =df_tps.loc[:,["index","unicite"]].apply(lambda var: get_ind(var,"index",dic_tps,unique_tps,"unicite"),axis =1)
list_ind = [dic_tps[k] for k in dic_tps]
df_tps = df_tps.iloc[list_ind]

df_tps.drop("index",axis=1,inplace=True)
df_tps.reset_index(inplace=True)
df_tps.drop("index",axis=1,inplace=True)
df_tps.reset_index(inplace=True)

col = ['time_id', 'annee', 'semestre', 'unicite']
df_tps.columns = col

dic_tpsdid = {}
df_tps.loc[:,["time_id","unicite"]].apply(lambda var: get_ind(var,"time_id",dic_tpsdid,unique_tps,"unicite"),axis =1)
df["time_id"] = df["unicite"].apply(lambda var : dic_tpsdid[var])

df_tps.drop("unicite",inplace= True,axis=1)

maj(tot = tot)

#Dim Etudiant

df_student = df.loc[:,["index","N° Etudiant","Nom","Prénom","time_id"]]
unique_std = df_student["N° Etudiant"].unique()
dic_ind = {}

l =df_student.loc[:,:"N° Etudiant"].apply(lambda var: get_ind(var,"index",dic_ind,unique_std,"N° Etudiant"),axis =1)
list_ind = [dic_ind[k] for k in dic_ind]

df_student = df_student.iloc[list_ind]
df_student.drop("index",axis=1,inplace=True)
df_student.reset_index(inplace=True)
df_student.drop("index",axis=1,inplace=True)
df_student.reset_index(inplace=True)
col = list(df_student.columns)
col[0] = "std ID"
df_student.columns = col
dic_stdid = {}
df_student.loc[:,["std ID","N° Etudiant"]].apply(lambda var: get_ind(var,"std ID",dic_stdid,unique_std,"N° Etudiant"),axis =1)

df["std ID"] = df["N° Etudiant"].apply(lambda var : dic_stdid[var])

maj(tot = tot)


#Dim UV

df_UV = df.loc[:,["index","nom_UV","code_UV","time_year","semestre"]]

unique_uv = df_UV["nom_UV"].unique()
dic_uv = {}

l =df_UV.loc[:,["index","nom_UV"]].apply(lambda var: get_ind(var,"index",dic_uv,unique_uv,"nom_UV"),axis =1)
list_ind = [dic_uv[k] for k in dic_uv]
df_UV = df_UV.iloc[list_ind]

df_UV.drop("index",axis=1,inplace=True)
df_UV.reset_index(inplace=True)
df_UV.drop("index",axis=1,inplace=True)
df_UV.reset_index(inplace=True)

col = list(df_UV.columns)
col[0] = "uv ID"
df_UV.columns = col

dic_uvdid = {}
df_UV.loc[:,["uv ID","nom_UV"]].apply(lambda var: get_ind(var,"uv ID",dic_uvdid,unique_uv,"nom_UV"),axis =1)
df_UV.head()
df["UV ID"] = df["nom_UV"].apply(lambda var : dic_uvdid[var])

maj(tot = tot)

#Dim CS

df_cs = df.loc[:,["index","idcss","responsable_UE","libelle_UE","codeCS","semestre","time_year"]]

unique_cs = df_cs["idcss"].unique()
dic_cs = {}

l =df_cs.loc[:,["index","idcss"]].apply(lambda var: get_ind(var,"index",dic_cs,unique_cs,"idcss"),axis =1)
list_ind = [dic_cs[k] for k in dic_cs]
df_cs = df_cs.iloc[list_ind]

df_cs.drop("index",axis=1,inplace=True)
df_cs.reset_index(inplace=True)
df_cs.drop("index",axis=1,inplace=True)
df_cs.reset_index(inplace=True)

col = ['cs ID', 'idcss', 'respoCS', 'nom_CS', 'codeCS','semestre','annee']
df_cs.columns = col

dic_csdid = {}
df_cs.loc[:,["cs ID","idcss"]].apply(lambda var: get_ind(var,"cs ID",dic_csdid,unique_cs,"idcss"),axis =1)
df_cs.head()
df["cs ID"] = df["idcss"].apply(lambda var : dic_csdid[var])

df_cs.drop("idcss",inplace= True,axis=1)

mandatory = ['STA','STB','STC','IGA','IGB']

df_cs["jacq"] = df_cs.apply(lambda line : jacq_dic[line["annee"]][line["semestre"]][line["codeCS"]] if line["codeCS"] in mandatory else 4 ,axis = 1)

maj(tot = tot)
#Dim CG
rel_CG_nom = {"IG": "Compétences en ingénierie",
             "interp": "Compétences interpersonnelles",
             "intra" : "Compétences intra-personnelles",
             "ST" : "Compétences scientifiques et techniques"}
df_cg = df.loc[:,["index","codeCS"]]

df_cg["codeCS"] = df_cg["codeCS"].apply(lambda var: var[0:-1])
df_cg["cg_nom"] = df_cg["codeCS"].apply(lambda var: rel_CG_nom[var])

unique_cg = df_cg["codeCS"].unique()
dic_cg = {}

l =df_cg.loc[:,["index","codeCS"]].apply(lambda var: get_ind(var,"index",dic_cg,unique_cg,"codeCS"),axis =1)
list_ind = [dic_cg[k] for k in dic_cg]
df_cg = df_cg.iloc[list_ind]

df_cg.drop("index",axis=1,inplace=True)
df_cg.reset_index(inplace=True)
df_cg.drop("index",axis=1,inplace=True)
df_cg.reset_index(inplace=True)

col = ["cg id","code cg","cg_nom"]
df_cg.columns = col

dic_cgdid = {}
df_cg.loc[:,["cg id","code cg"]].apply(lambda var: get_ind(var,"cg id",dic_cgdid,unique_cg,"code cg"),axis =1)
df_cg.head()
df["cg ID"] = df["codeCS"].apply(lambda var : dic_cgdid[var[:-1]])


maj(tot = tot)

# Dim Degenerated Lieu
temp = {'id' : [0], 'lieu': ['Nantes']}
lieu_d = pd.DataFrame(temp)
dic_temp = {'Nantes': 0}
df['lieu_ID'] = df.apply(lambda var : dic_temp[var['lieu']],axis =1)
maj(tot = tot)

#Fact Table TDFNotes
def jnote(line):
    if line["note"] == "+":
        return int(df_cs[df_cs["cs ID"] == line["cs ID"]]['jacq']+1)
    elif line["note"] == "=":
        return int(df_cs[df_cs["cs ID"] == line["cs ID"]]['jacq'])
    else: 
        return 0

ft_notes = df.loc[:,["cs ID","UV ID","time_id","std ID","lieu_ID","note"]]
ft_notes["jetons_acquis"] = ft_notes.apply(lambda line: jnote(line), axis = 1)
ft_notes.drop("note",inplace = True, axis = 1)

maj(tot = tot)

# Fact Table TDF_csuv
ft_csuv = df.loc[:,["cs ID","UV ID"]]

def niv_cs(line):
    tmp = df_cs[df_cs["cs ID"] == line["cs ID"]]

    if tmp["semestre"][tmp.index[0]] == "S1":
        return 1
    elif tmp["semestre"][tmp.index[0]] == "S2" :
        return 2

ft_csuv["niveau_CS"] = ft_csuv.apply(lambda line : niv_cs(line),axis = 1)
ft_csuv["nb_jetons"] = 4


maj(tot = tot)



#Fact Table TDF_cscg

ft_cscg = df.loc[:,["cs ID","cg ID"]]
ft_cscg = ft_cscg.drop_duplicates()

maj(tot = tot)

#Fact Table Comp

maj(tot = tot)

#Modifying the column's names

maj(tot = tot)

#Creating tables
print("CREATING FILES")
tot = 9
maj(reset = True, tot = tot)

"""
df_tps
df_student
df_UV
df_cs
df_cg
lieu_d

ft_notes
ft_csuv
ft_cscg
"""

df_student.columns = ['std_ID', 'etudiantID', 'nom', 'prenom', 'annee_promo']
df_student.to_csv("../results/table/dim_etudiant.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)


df_UV.columns = ['uv_ID', 'nom_UV', 'code_UV', 'annee', 'semestre']
df_UV.to_csv("../results/table/dim_UV.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

df_cs.columns = ['cs_ID', 'respo_cs', 'nom_cs', 'code_cs', 'semestre', 'annee', 'jacq']
df_cs.to_csv("../results/table/dim_CS.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

df_cg.columns = ['cg_ID', 'code_cg', 'nom_cg']
df_cg.to_csv("../results/table/dim_CG.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)


ft_notes.columns = ['cs_ID', 'uv_ID', 'temps_id', 'std_ID', 'lieu_ID', 'jetons_acquis']
ft_notes.to_csv("../results/table/table_de_fait_notes.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

ft_csuv.columns = ['cs_ID', 'uv_ID', 'niveau_CS', 'nb_jetons']
ft_csuv.to_csv("../results/table/table_de_fait_csuv.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

ft_cscg.columns = ['cs_ID','cg_ID']
ft_cscg.to_csv("../results/table/table_de_fait_cscg.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

lieu_d.columns = ['lieu_ID', 'campus']
lieu_d.to_csv("../results/table/dim_lieu.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)


df_tps.columns = ["temps_ID", "annee","semestre"]
df_tps.to_csv("../results/table/dim_temps.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

print("TABLES SAVED")







#### Cleaning files

