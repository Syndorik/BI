from random import shuffle
import sys
import os

sys.path.insert(0,"../lib")

import argparse
import pandas as pd
import numpy as np
import copy

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

tot = 13
maj(reset=True, tot = tot)

#Preparation
def get_ind(var,strr,dic,unique,printed):
    if((var[printed] in unique) and (var[printed] not in dic) ):
        dic[var[printed]] = var[strr]
        
def get_ind2(df):
    df.drop('index', axis = 1,inplace=True)
    df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True)
    return df

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

df_tps = get_ind2(df_tps)
df_tps.drop("index",axis=1,inplace=True)
df_tps.reset_index(inplace=True)
df_tps.drop("index",axis=1,inplace=True)
df_tps.reset_index(inplace=True)

col = ['time_id', 'annee', 'semestre', 'unicite']
df_tps.columns = col

df["time_id"] = df.apply(lambda var : df_tps[df_tps["unicite"] == var["unicite"]].index[0],axis = 1)
df_tps.drop("unicite",inplace= True,axis=1)

maj(tot = tot)

#Dim Etudiant

df_student = df.loc[:,["index","N° Etudiant","Nom","Prénom","time_year"]]
df_student = get_ind2(df_student)

df_student.drop("index",axis=1,inplace=True)
df_student.reset_index(inplace=True)
df_student.drop("index",axis=1,inplace=True)
df_student.reset_index(inplace=True)

col = list(df_student.columns)
col[0] = "std ID"
df_student.columns = col

df["std ID"] = df.apply(lambda var : df_student[df_student["N° Etudiant"] == var["N° Etudiant"]].index[0],axis = 1)


maj(tot = tot)


#Dim UV

df_UV = df.loc[:,["index","nom_UV","code_UV","time_year","semestre"]]
df_UV = get_ind2(df_UV)
df_UV.drop("index",axis=1,inplace=True)
df_UV.reset_index(inplace=True)
df_UV.drop("index",axis=1,inplace=True)
df_UV.reset_index(inplace=True)

col = list(df_UV.columns)
col[0] = "uv ID"
df_UV.columns = col

df["UV ID"] = df.apply(lambda var : df_UV[(df_UV["nom_UV"] == var["nom_UV"]) & (df_UV["code_UV"] == var["code_UV"]) & (df_UV["time_year"] == var["time_year"]) & (df_UV["semestre"] == var["semestre"])]["uv ID"].index[0],axis = 1)

maj(tot = tot)

#Dim CS

df_cs = df.loc[:,["index","idcss","responsable_UE","libelle_UE","codeCS","semestre","time_year"]]
df_cs = get_ind2(df_cs)
df_cs.drop("index",axis=1,inplace=True)
df_cs.reset_index(inplace=True)
df_cs.drop("index",axis=1,inplace=True)
df_cs.reset_index(inplace=True)

col = ['cs ID', 'idcss', 'respoCS', 'nom_CS', 'codeCS','semestre','annee']
df_cs.columns = col

df["cs ID"] = df.apply(lambda var : df_cs[(df_cs["idcss"] == var["idcss"]) & (df_cs["semestre"] == var["semestre"]) & (df_cs["annee"] == var["time_year"])].index[0],axis = 1)

df_cs.drop("idcss",inplace= True,axis=1)
mandatory = ['STA','STB','STC','IGA','IGB']
df_cs["jacq"] = df_cs.apply(lambda line : jacq_dic[line["annee"]][line["semestre"]][line["codeCS"]] if line["codeCS"] in mandatory else  4,axis = 1)
#df_cs["jacq"]= df_cs.apply(lambda line : 4 if((line["jacq"] == 0) and (line["semestre"] == "S2")) else int(line["jacq"]),axis = 1)
maj(tot = tot)

#Dim CG
rel_CG_nom = {"IG": "Compétences en ingénierie",
             "interp": "Compétences interpersonnelles",
             "intra" : "Compétences intra-personnelles",
             "ST" : "Compétences scientifiques et techniques"}
df_cg = df.loc[:,["index","codeCS"]]
df_cg["codeCS"] = df_cg["codeCS"].apply(lambda var: var[0:-1])
df_cg["cg_nom"] = df_cg["codeCS"].apply(lambda var: rel_CG_nom[var])

df_cg = get_ind2(df_cg)

df_cg.drop("index",axis=1,inplace=True)
df_cg.reset_index(inplace=True)
df_cg.drop("index",axis=1,inplace=True)
df_cg.reset_index(inplace=True)

col = ["cg id","code cg","cg_nom"]
df_cg.columns = col

df["cg ID"] = df.apply(lambda var : df_cg[df_cg["code cg"] == var["codeCS"][:-1]].index[0],axis = 1)



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
        return 5
    elif line["note"] == "=":
        return 4
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
ft_csuv.drop_duplicates(inplace=True)


maj(tot = tot)



#Fact Table TDF_cscg

ft_cscg = df.loc[:,["cs ID","cg ID"]]
ft_cscg = ft_cscg.drop_duplicates()

maj(tot = tot)

#Dim dégénéré CS code
df_csdegen = df.loc[:,["codeCS"]].drop_duplicates()
df_csdegen = df_csdegen.reset_index().drop("index",axis=1).reset_index()
df_csdegen.columns = ["code_cs_ID","code_CS"]

#Fact Table TDF_csnote
def ret_niv_jetons(line):
    cc = ft_notes[(ft_notes["std ID"] == line["std ID"]) & (ft_notes["cs ID"].isin(df_cs[df_cs["codeCS"] == line["codeCS"]].index))].groupby("cs ID").sum()
    cc = cc.reset_index()
    cc["jacq"] = cc.apply(lambda line : list(df_cs[df_cs["cs ID"] == line["cs ID"]]["jacq"])[0],axis = 1)
    cc["jetons_acquis"] = cc.apply(lambda line : str(line["jetons_acquis"]) +"_"+str(ret_nv(line))+"_"+str(line["jacq"]),axis = 1)
    return "-".join(list(cc["jetons_acquis"]))

def ret_nv(line):
    s = list(df_cs[df_cs["cs ID"] == line["cs ID"]]["semestre"])[0]
    if(s == "S1"):
        return 1
    else:
        return 2

def retnbjeton(line):
    jsum = sum(ft_notes[(ft_notes["std ID"] == line["std ID"]) & (ft_notes["cs ID"] == line["cs ID"]) ]["jetons_acquis"])
    jaac = list(df_cs[df_cs["cs ID"] == line["cs ID"]]["jacq"])[0]
    if jsum > jaac :
        return jaac
    else:
        return jsum

def niv_atteint(line):
    if line["nb_jeton"] == line["jetonmax"]:
        return line["niv"]
    else:
        return 0


def split_nv2(line):
    l = line["tmp"].split("-")
    if(len(l) == 2):
        l = l[1]
        
    else :
        l = l[0]
        splitt = l.split("_")
        niv = splitt[1]
        if (int(niv) != 2):
            return 0
        
        ll = splitt[0]
        if(int(ll) > int(splitt[2])):
            ll = splitt[2]
        return ll

    splitt = l.split("_")
    ll = splitt[0]
    if(int(ll) > int(splitt[2])):
        ll = splitt[2]
    return ll

def split_nv1(line):
    l = line["tmp"].split("-")[0]
    
    splitt = l.split("_")
    niveau = int(splitt[1])
    if(niveau == 2):
        return 0
    
    ll = splitt[0]
    if(int(ll) > int(splitt[2])):
        ll = splitt[2]
    return ll

def splitjacq_nv1(line):
    l = line["tmp"].split("-")[0]
    splitt = l.split("_")
    niveau = int(splitt[1])
    if(niveau == 2):
        return 0
    return splitt[2]

def splitjacq_nv2(line):
    l = line["tmp"].split("-")
    if(len(l) == 2):
        l = l[1]
    else :
        l = l[0]
        splitt = l.split("_")
        niv = splitt[1]
        if (int(niv) != 2):
            return 0
        return splitt[2]

    splitt = l.split("_")
    return splitt[2] 


def niveau_atteint(line):
    nbj2a = int(line["nbre_jetons_niveau2_acquis"])
    nbj1a = int(line["nbre_jetons_niveau1_acquis"])
    tmpjac2 = int(line["tmp_jac2"])
    tmpjac1 = int(line["tmp_jac1"])
    if((nbj2a == tmpjac2) and (tmpjac2 != 0)):
        return 2
    elif((nbj1a == tmpjac1) and (tmpjac1 !=0)):
        return 1
    elif((nbj1a + nbj2a >= tmpjac1) and (tmpjac1 != 0)):
        return 1
    else:
        return 0

def ratio_jeton_niv_2(line):
    nv_cs = int(line["niveau_atteint_Cs"])
    tmpjac = int(line["tmp_jac2"])
    if nv_cs == 2:
        return 100
    elif nv_cs == 0:
        return 0
    elif tmpjac == 0:
        return 0
    else:
        return 100*int(line["nbre_jetons_niveau2_acquis"])/tmpjac

def ratio_jeton_niv_1(line):
    nv_cs = int(line["niveau_atteint_Cs"])
    tmpjac = int(line["tmp_jac1"])
    if nv_cs == 2:
        return 100
    elif (nv_cs == 1):
        return 100
    elif tmpjac == 0:
        return 0
    else:
        return 100*int(line["nbre_jetons_niveau1_acquis"])/tmpjac
    
def ret_nivmax_poss(line):
    spli = line["tmp"].split("-")
    if len(spli) == 2:
        return 2
    spli = spli[0].split("_")
    if int(spli[1]) == 2:
        return 2
    else:
        return 1

ft_csnote = df.loc[:,["std ID","codeCS"]]
ft_csnote.drop_duplicates(inplace= True)
ft_csnote["tmp"] = ft_csnote.apply(lambda line : ret_niv_jetons(line),axis=1)

ft_csnote["nbre_jetons_niveau1_acquis"] = ft_csnote.apply(lambda line : split_nv1(line),axis = 1)
ft_csnote["nbre_jetons_niveau2_acquis"] = ft_csnote.apply(lambda line : split_nv2(line),axis = 1)
ft_csnote["tmp_jac1"] = ft_csnote.apply(lambda line : splitjacq_nv1(line),axis = 1)
ft_csnote["tmp_jac2"] = ft_csnote.apply(lambda line : splitjacq_nv2(line),axis = 1)
ft_csnote["niveau_atteint_Cs"] = ft_csnote.apply(lambda line : niveau_atteint(line),axis = 1)

ft_csnote["ratio_jeton_niv_de_0_à_1"] =ft_csnote.apply(lambda line : ratio_jeton_niv_1(line),axis = 1)
ft_csnote["ratio_jeton_niv_de_1_à_2"] =ft_csnote.apply(lambda line : ratio_jeton_niv_2(line),axis = 1)
ft_csnote["niv_max_possible"] = ft_csnote.apply(lambda line : ret_nivmax_poss(line),axis =1)

ft_csnote.drop(["tmp","tmp_jac1","tmp_jac2"],axis = 1,inplace=True)
ft_csnote["codeCS"] = ft_csnote["codeCS"].apply(lambda col : list(df_csdegen[df_csdegen["code_CS"] == col]["code_cs_ID"])[0])
ft_csnote.columns = ['std_ID', 'code_cs_ID', 'nbre_jetons_niveau1_acquis',
       'nbre_jetons_niveau2_acquis', 'niveau_atteint_Cs','ratio_jeton_niv_de_0_à_1', 'ratio_jeton_niv_de_1_à_2',
       'niv_max_possible']

#Add missing line (ie Cs non evaluated during this year)

def get_missing_line_cs(std):
    comp = [0,1,2,3,4,5,6,7,8,9]
    list_code_cs = list(std["code_cs_ID"])
    myset = set(comp).difference(list_code_cs)
    toappend = []
    for k in myset:
        toappend.append(k)
    line_to_append[list(std["std_ID"])[0]] = toappend


grp_by_std = ft_csnote.groupby("std_ID")
line_to_append ={}

grp_by_std.apply(lambda line : get_missing_line_cs(line))

copy_dic = copy.deepcopy(line_to_append)
for k in copy_dic:
    if line_to_append[k] == []:
        line_to_append.pop(k)
        
std_col = []
code_cs_col = []


for k in line_to_append.items():
    lenn = len(k[1])
    std_id = [k[0]]*lenn
    code_cs = k[1]
    code_cs_col.append(code_cs)
    std_col.append(std_id)

std_pd = [item for sublist in std_col for item in sublist]
code_cs_ID_pd = [item for sublist in code_cs_col for item in sublist]
nbre_jetons_niveau1_acquis_pd = [0]*len(code_cs_ID_pd)
nbre_jetons_niveau2_acquis_pd = [0]*len(code_cs_ID_pd)
niveau_atteint_Cs_pd = [0]*len(code_cs_ID_pd)
ratio_jeton_niv_de_0_à_1_pd = [0]*len(code_cs_ID_pd)
ratio_jeton_niv_de_1_à_2_pd = [0]*len(code_cs_ID_pd)
niv_max_possible_pd = [0]*len(code_cs_ID_pd)

df_toappend = pd.DataFrame(data= {
    "std_ID":std_pd,
    "code_cs_ID" : code_cs_ID_pd,
    "nbre_jetons_niveau1_acquis":nbre_jetons_niveau1_acquis_pd,
    "nbre_jetons_niveau2_acquis":nbre_jetons_niveau2_acquis_pd,
    "niveau_atteint_Cs":niveau_atteint_Cs_pd,
    "ratio_jeton_niv_de_0_à_1":ratio_jeton_niv_de_0_à_1_pd,
    "ratio_jeton_niv_de_1_à_2":ratio_jeton_niv_de_1_à_2_pd,
    "niv_max_possible":niv_max_possible_pd
    })

ft_csnote = ft_csnote.append(df_toappend)
ft_csnote["ratio_jeton_niv_de_1_à_2"] = ft_csnote["ratio_jeton_niv_de_1_à_2"].apply(round)
ft_csnote["ratio_jeton_niv_de_0_à_1"] = ft_csnote["ratio_jeton_niv_de_0_à_1"].apply(round)



maj(tot = tot)

#Fact table cgnote
def ret_nivmaxcg(line):
    if(line["cg_ID"] == 0):
        return 2
    elif(line["cg_ID"] == 1):
        return 1
    elif(line["cg_ID"] == 2):
        return 1
    elif(line["cg_ID"] == 3):
        return 2

def niv_median(line):
    indices = list(df_csdegen[df_csdegen["code_CS"].isin(df_cs.loc[list(ft_cscg[ft_cscg["cg ID"] == line["cg ID"]]["cs ID"])]["codeCS"].unique())]["code_cs_ID"])
    mediann = round(ft_csnote[(ft_csnote["std_ID"] == line["std ID"]) & (ft_csnote["code_cs_ID"].isin(indices))]["niveau_atteint_Cs"].median())
    return int(mediann)

ft_cgnote = df.loc[:,["std ID","cg ID"]].drop_duplicates()
ft_cgnote["niveau_atteint_cg"] = ft_cgnote.apply(lambda line : niv_median(line),axis = 1) 
ft_cgnote.columns = ['std_ID', 'cg_ID', 'niveau_atteint_Cg']
ft_cgnote["niv_max_possible"] = ft_cgnote.apply(lambda line : ret_nivmaxcg(line),axis = 1)

#Add missing line (ie Cg non evaluated during this year)

def get_missing_line(std):
    comp = [0,1,2,3]
    list_cg = list(std["cg_ID"])
    myset = set(comp).difference(list_cg)
    toappend = []
    for k in myset:
        toappend.append(k)
    line_to_append[list(std["std_ID"])[0]] = toappend

grp_by_std = ft_cgnote.groupby("std_ID")
line_to_append ={}

grp_by_std.apply(lambda line : get_missing_line(line))

copy_dic = copy.deepcopy(line_to_append)
for k in copy_dic:
    if line_to_append[k] == []:
        line_to_append.pop(k)
        
std_col = []
cg_col = []


for k in line_to_append.items():
    lenn = len(k[1])
    std_id = [k[0]]*lenn
    cg = k[1]
    cg_col.append(cg)
    std_col.append(std_id)
std_pd = [item for sublist in std_col for item in sublist]
cg_pd = [item for sublist in cg_col for item in sublist]
niv_atteint_pd = [0]*len(cg_pd)
niv_max_possible_pd = [0]*len(std_pd)
df_toappend = pd.DataFrame(data= {"std_ID":std_pd,"cg_ID" : cg_pd,"niveau_atteint_Cg":niv_atteint_pd, "niv_max_possible":niv_max_possible_pd})
ft_cgnote = ft_cgnote.append(df_toappend)


#Dim dégénéré pourcentage
prrcentage = list(range(0,101))
df_degenereperc = pd.DataFrame(data = {"percentage_ID" : prrcentage, "value" : prrcentage})

#TDF_NiveauCsNonatteint

ft_nivCsnonAtteint = df.loc[:,'std ID'].copy(deep = True).drop_duplicates()
list_niv_nonatteint = []
def retrieve_cs_non_atteint_niv(line):
    std_cs = ft_csnote[ft_csnote["std_ID"] == line]
    niv_1 = std_cs[std_cs["niveau_atteint_Cs"] == 1]
    niv_1_nonatteint = niv_1.apply(lambda line : str(line["std_ID"]) + "-" + str(line["niveau_atteint_Cs"]) + "-"+ str(line["ratio_jeton_niv_de_1_à_2"]),axis= 1)
    
    niv_0 = std_cs[std_cs["niveau_atteint_Cs"] == 0]
    niv_0_nonatteint = niv_0.apply(lambda line : str(line["std_ID"]) + "-" + str(line["niveau_atteint_Cs"]) + "-"+ str(line["ratio_jeton_niv_de_0_à_1"]) if(line["niv_max_possible"] != 0) else None,axis= 1)
    
    niv_0_nonatteint = list(filter(lambda x : x if x!= None else None,list(niv_0_nonatteint)))
    
    niv_2 = std_cs[std_cs["niveau_atteint_Cs"] == 2]
    niv_2_nonatteint = niv_2.apply(lambda line : str(line["std_ID"]) + "-" + str(line["niveau_atteint_Cs"]) + "-"+ str(line["ratio_jeton_niv_de_1_à_2"]),axis= 1)
    
    list_niv_nonatteint.append(list(niv_0_nonatteint))
    list_niv_nonatteint.append(list(niv_1_nonatteint))
    list_niv_nonatteint.append(list(niv_2_nonatteint))

#protocol : 

#17-1-50 niveau 1 + 50% du niveau 2 (entre 1 et 2)
#17-1-67 niveau 1 + 67% du niveau 2 (entre 1 et 2)
#

c = ft_nivCsnonAtteint.apply(lambda line : retrieve_cs_non_atteint_niv(line))

torm = ['std_ID',
  'code_cs_ID',
  'nbre_jetons_niveau1_acquis',
  'nbre_jetons_niveau2_acquis',
  'niveau_atteint_Cs',
  'ratio_jeton_niv_de_0_à_1',
  'ratio_jeton_niv_de_1_à_2',
  'niv_max_possible']
torm2 = None

list_niv_nonatteint = list(filter(lambda x : (x != torm) and (x != []),list_niv_nonatteint))
list_niv_nonatteint_sorted = [item for sublist in list_niv_nonatteint for item in sublist ]
list_niv_nonatteint_sorted = list(map(lambda x: x.split("-"),list_niv_nonatteint_sorted))

std_list = list(map(lambda x : int(x[0]),list_niv_nonatteint_sorted ))
niv_list = list(map(lambda x : int(x[1]),list_niv_nonatteint_sorted ))
perc_list = list(map(lambda x : int(x[2]),list_niv_nonatteint_sorted ))

ft_nivCsnonAtteint = pd.DataFrame(data={"std_ID": std_list, "niveau" : niv_list, "percentage" : perc_list})
ft_nivCsnonAtteint["nombre_cs_a_ce_niveau"] = 1

grpby = ft_nivCsnonAtteint.groupby(["std_ID","niveau","percentage"]).count()
ft_nivCsnonAtteint = grpby.reset_index()


maj(tot = tot)

#TDF_NiveauCgNonatteint

ft_nivCgnonAtteint = df.loc[:,"std ID"].drop_duplicates()

def diffniv(line):
    diff = line["niv_max_possible"] - line["niveau_atteint_Cg"]
    if diff <0:
        return 0
    else :
        return diff

nv_cg_non_atteint_list = []
def retrieve_cg_non_atteint_niv(line):
    notes = ft_cgnote[ft_cgnote["std_ID"] == line] 
    temp = notes.apply(lambda line : str(line["std_ID"]) + "-" + str(diffniv(line))+ "-" + str(line["niv_max_possible"]),axis= 1)
    nv_cg_non_atteint_list.append(list(temp))

c = ft_nivCgnonAtteint.apply(lambda line : retrieve_cg_non_atteint_niv(line))
nv_cg_non_atteint_list = [item for sublist in nv_cg_non_atteint_list for item in sublist]
nv_cg_non_atteint_list = list(map(lambda l : l.split("-"), nv_cg_non_atteint_list))

#Protocol:
#Code : 0-0-2 : stdID-nbniveaumanquant-niv_max_possible

std_id_list = list(map(lambda x : int(x[0]),nv_cg_non_atteint_list ))
nb_nv_manquant_list = list(map(lambda x : int(x[1]),nv_cg_non_atteint_list ))
niv_max_possible_list = list(map(lambda x : int(x[2]),nv_cg_non_atteint_list ))

ft_nivCgnonAtteint = pd.DataFrame(data = {"std_ID" : std_id_list, "nb_niv_manquant": nb_nv_manquant_list, "niv_max_possible" :niv_max_possible_list })

grpby = ft_nivCgnonAtteint.groupby(["std_ID","niv_max_possible"]).sum()
ft_nivCgnonAtteint = grpby.reset_index()

#Dim dégénérée Niveau
df_nv_degenere = pd.DataFrame(data = {"ID" : list(range(3)), "Niveau" : list(range(3))})


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

df_csdegen
ft_csnote
ft_cgnote
df_degenereperc

ft_nivCsnonAtteint
ft_nivCgnonAtteint
df_nv_degenere
"""

df_student.columns = ['std_ID', 'etudiantID', 'nom', 'prenom', 'annee_actuelle']
df_student.to_csv("../results/table/dim_etudiant.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)


df_csdegen.to_csv("../results/table/dim_cscode_degenere.csv",encoding = 'utf-8-sig', index = False)

ft_csnote.columns = ['std_ID', 'code_cs_ID', 'nbre_jetons_niveau1_acquis',
       'nbre_jetons_niveau2_acquis', 'niveau_atteint_Cs',
       'ratio_jeton_niv_de_0_à_1', 'ratio_jeton_niv_de_1_à_2',
       'niv_max_possible']
ft_csnote.to_csv("../results/table/table_de_fait_RstCs.csv",encoding = 'utf-8-sig', index = False)


ft_cgnote.columns = ['std_ID', 'cg_ID', 'niveau_atteint_Cg', 'niv_max_possible']
ft_cgnote.to_csv("../results/table/table_de_fait_RstCg.csv",encoding = 'utf-8-sig', index = False)


df_UV.columns = ['uv_ID', 'nom_uv', 'code_uv', 'annee', 'semestre']
df_UV.to_csv("../results/table/dim_UV.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

df_cs.columns = ['cs_ID', 'respo_cs', 'nom_cs', 'code_cs', 'semestre', 'annee', 'jacq']
df_cs.to_csv("../results/table/dim_CS.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

df_cg.columns = ['cg_ID', 'code_cg', 'nom_cg']
df_cg.to_csv("../results/table/dim_CG.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

df_degenereperc.columns = ['percentage_ID', 'percentage']
df_degenereperc.to_csv("../results/table/dim_percentage_degenere.csv",encoding = 'utf-8-sig', index = False)

ft_nivCsnonAtteint.columns = ['std_ID', 'niveau_ID', 'percentage_ID', 'nb_Nv_NA']
ft_nivCsnonAtteint.to_csv("../results/table/table_de_fait_NvCsNA.csv",encoding = 'utf-8-sig', index = False)

ft_nivCgnonAtteint.columns = ['std_ID', 'niveau_ID', 'nb_Nv_NA']
ft_nivCgnonAtteint.to_csv("../results/table/table_de_fait_NvCgNA.csv",encoding = 'utf-8-sig', index = False)

df_nv_degenere.columns = ['niveau_ID', 'niveau']
df_nv_degenere.to_csv("../results/table/table_de_fait_NvCgNA.csv",encoding = 'utf-8-sig', index = False)

ft_notes.columns = ['cs_ID', 'uv_ID', 'temps_id', 'std_ID', 'lieu_ID', 'jetons_acquis']
ft_notes.to_csv("../results/table/table_de_fait_notes.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

ft_csuv.columns = ['cs_ID', 'uv_ID', 'niveau_CS', 'nb_jetons']
ft_csuv.to_csv("../results/table/table_de_fait_csuv.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

ft_cscg.columns = ['cs_ID','cg_ID']
ft_cscg.to_csv("../results/table/table_passerelle_cscg.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

lieu_d.columns = ['lieu_ID', 'campus']
lieu_d.to_csv("../results/table/dim_lieu.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)


df_tps.columns = ["temps_ID", "annee","semestre"]
df_tps.to_csv("../results/table/dim_temps.csv",encoding = 'utf-8-sig', index = False)
maj(tot = tot)

print("TABLES SAVED")







#### Cleaning files

