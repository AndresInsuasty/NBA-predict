import pandas as pd
from itertools import  *
from pycaret.regression import *
import streamlit as st

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

def select_teams(teams,columns,salary_l=60000,num_team=20):
  num=1
  output={}
  for team in teams:
    aux_df = pd.DataFrame(team,columns=columns)
    if aux_df['FD_SALARY'].sum() <= salary_l :
       contar_team=aux_df.groupby('TEAM')['TEAM'].count()
       count = len(contar_team[contar_team>4])
       if count == 0:
         output['team'+str(num)]=aux_df
         num += 1
         if num>num_team:
           break;
  return output

def sum_pts(df):
    col=['PLAYERS', 'TEAM', 'FD_POS', 'FD_SALARY', 'FD_PTS']
    aux_df= pd.DataFrame(df,columns=col)
    return aux_df['FD_PTS'].sum()
    
@st.cache(suppress_st_warning=True)
def get_teams(data,inicio,fin):
    #Separamos por posicion
    SG_d = data[data['FD_POS']=='SG'].sort_values('FD_PTS',ascending=False)
    SF_d = data[data['FD_POS']=='SF'].sort_values('FD_PTS',ascending=False)
    PG_d = data[data['FD_POS']=='PG'].sort_values('FD_PTS',ascending=False)
    PF_d = data[data['FD_POS']=='PF'].sort_values('FD_PTS',ascending=False)
    C_d = data[data['FD_POS']=='C'].sort_values('FD_PTS',ascending=False)

    #reducimos numero de registros(dejamos los mayores pts)
    SG_d = SG_d[inicio:fin]
    SF_d = SF_d[inicio:fin]
    PG_d = PG_d[inicio:fin]
    PF_d = PF_d[inicio:fin]
    C_d = C_d[inicio:fin]
    
    #Convertirmos en lista para sacar combinatoria
    SG_d = SG_d.values.tolist()
    SF_d = SF_d.values.tolist()
    PG_d = PG_d.values.tolist()
    PF_d = PF_d.values.tolist()
    C_d = C_d.values.tolist()

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

    teams = []
    teams = juntar(SG,SF)
    teams = juntar(teams,PG)
    teams = juntar(teams,PF)
    teams = juntar(teams,C)

    #Como estaban ordenados las primeros tienen los mayores pts
    best_team= teams[0:50000]
    #ordenamos
    best_team.sort(key=sum_pts,reverse=True)

    return best_team