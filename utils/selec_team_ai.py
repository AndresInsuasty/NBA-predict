import pandas as pd
from itertools import  *
from io import StringIO
from pycaret.regression import *
import streamlit as st
import math

@st.cache(hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True,allow_output_mutation=True)
def load_data(file_uploaded,selection_file):
    if selection_file=='CSV':
        return pd.read_csv(file_uploaded)
    else:
        return pd.read_excel(file_uploaded)

def predict(data,model):
    data_clean = clean(data)
    prediction = predict_model(model, data_clean)
    prediction.rename(columns={'Label':'FD_PTS'},inplace=True)
    return pd.concat([data[['PLAYERS','TEAM','FD_POS','FD_SALARY']],prediction['FD_PTS']],axis=1)

def clean(data):
    data_aux = data.drop([data.columns[0],'DATE','PLAYERS','TEAM', 'OPP_TEAM','VENUE\n(R/H)','CLOSING_SPREAD', 'CLOSING_TOTAL', 'PACE', 'OEFF','DEFF', 'TEAM(REST)', 'PLAYERS(REST)','FD_POS'],axis=1)
    data_aux.rename(columns={'STARTER\n(Y/N)':'STARTER','2FG':'FG','2FGA':'FGA','FD_SALARY':'SALARY'},inplace=True)
    return data_aux

def juntar(l1,l2):
  aux = []
  for x in l1:
    for y in l2:
      aux.append(x+y)
  return aux

def select_teams(teams,columns,output,salary_l=60000,num_team=20):
  num = len(output)+1
  for team in teams:
    aux_df = pd.DataFrame(team,columns=columns)
    if aux_df['FD_SALARY'].sum() <= salary_l :
       contar_team=aux_df.groupby('TEAM')['TEAM'].count()
       count = len(contar_team[contar_team>4])
       if count == 0:
         output['team'+str(num)]=aux_df
         num += 1
         if num>num_team:
           return output;
  return output


def prom_values(data):
    #Salario promedio 
    res= data.groupby(['PLAYERS', 'TEAM'])['MINS','USAGE_RATE','FD_SALARY','2FG','2FGA','3P','3PA','FT','FTA','OR','DR','REBR','AST','PF','ST','TO','BL','PTS'].mean().reset_index()
    #Elimina duplicados
    data = data.drop_duplicates(['PLAYERS', 'TEAM'],keep='last').sort_values(by=['PLAYERS']).reset_index()
    data[['MINS','USAGE_RATE']] = res[['MINS','USAGE_RATE']]
    data[['2FG','2FGA','3P','3PA','FT','FTA','OR','DR','REBR','AST','PF','ST','TO','BL','PTS']] = res[['2FG','2FGA','3P','3PA','FT','FTA','OR','DR','REBR','AST','PF','ST','TO','BL','PTS']].round(0)
    return data
    

def sum_pts(df):
    col=['PLAYERS', 'TEAM', 'FD_POS', 'FD_SALARY', 'FD_PTS']
    aux_df= pd.DataFrame(df,columns=col)
    return aux_df['FD_PTS'].sum()
    
@st.cache(suppress_st_warning=True)
def get_player(data,inicio,fin):
    #Separamos por posicion
    SG_d = data[data['FD_POS']=='SG'].sort_values('FD_PTS',ascending=False)
    SF_d = data[data['FD_POS']=='SF'].sort_values('FD_PTS',ascending=False)
    PG_d = data[data['FD_POS']=='PG'].sort_values('FD_PTS',ascending=False)
    PF_d = data[data['FD_POS']=='PF'].sort_values('FD_PTS',ascending=False)
    C_d = data[data['FD_POS']=='C'].sort_values('FD_PTS',ascending=False)
    
    #Convertirmos en lista para sacar combinatoria
    SG_d = SG_d.values.tolist()
    SF_d = SF_d.values.tolist()
    PG_d = PG_d.values.tolist()
    PF_d = PF_d.values.tolist()
    C_d = C_d.values.tolist()

    if len(SG_d)>15: SG_d = SG_d[0:-1:2]
    if len(SF_d)>15: SF_d = SF_d[0:-1:2]
    if len(PG_d)>15: PG_d = PG_d[0:-1:2]
    if len(PF_d)>15: PF_d = PF_d[0:-1:2]
    if len(C_d)>15: C_d = C_d[0:-1:2]
    
   

    #Combinatorio de los elementos
    SG = list(combinations(SG_d,2))
    SF = list(combinations(SF_d,2))
    PG = list(combinations(PG_d,2))
    PF = list(combinations(PF_d,2))
    C = list(combinations(C_d,1))

    #Organizamos para que quede list-list
    SG = [list(i) for i in SG] 
    SF = [list(i) for i in SF] 
    PG = [list(i) for i in PG] 
    PF = [list(i) for i in PF]
    C =  [list(i) for i in C]

    SG.sort(key=sum_pts,reverse=True)
    SF.sort(key=sum_pts,reverse=True)
    PG.sort(key=sum_pts,reverse=True)
    PF.sort(key=sum_pts,reverse=True)
    #get_teams(SG,SF,PG,PF,C,inicio,fin)
    return SG,SF,PG,PF,C
    
def get_teams(SG,SF,PG,PF,C,inicio,fin):
  #reducimos numero de registros(dejamos los mayores pts)
    SG = SG[inicio:fin]
    SF= SF[inicio:fin]
    PG = PG[inicio:fin]
    PF = PF[inicio:fin]
    C = C[inicio:fin]

    teams = []
    teams = juntar(SG,SF)
    teams = juntar(teams,PG)
    teams = juntar(teams,PF)
    teams = juntar(teams,C)

    #Como estaban ordenados las primeros tienen los mayores pts
    best_team= teams
    #ordenamos
    best_team.sort(key=sum_pts,reverse=True)

    return best_team