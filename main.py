# Script to run the principal code 
import streamlit as st
import pandas as pd
import numpy as np
import os

# local packages
from utils import forecast
from utils.select_your_team_F import team_f
from utils.select_your_team_DK import team_dk
from utils.selec_team_ai import *

st.title('NBA Fantasy points prediction')
selection = st.selectbox("Select a Platform",['Drafkings','Fanduel'])
selection_file = st.selectbox("Select a File extension",['CSV','XLSX'])
uploaded_file = st.file_uploader("Choose a file",type=['csv','xlsx'])

if uploaded_file is not None:
    if selection_file=='CSV':
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)
    #st.write(data.head())
    uploaded_file.seek(0) #libera memoria
    teams = pd.unique(data['TEAM'])
    selected_teams = np.zeros(len(teams))
    st.markdown('# Select your teams to make predictions please!')
    for id,team in enumerate(teams):
        selected_teams[id] = st.checkbox(team,value=True)
    teams_df = pd.concat([pd.Series(teams),pd.Series(selected_teams)],axis=1)
    teams_df.columns=['TEAM','Selected']
    teams_selected_df = teams_df[teams_df['Selected']==True]
    filter = data[data['TEAM'].isin(teams_selected_df['TEAM'].to_list())]
    filter = filter.reset_index(drop=True)
    st.write(filter)
    try:
        output={}
        if selection == 'Drafkings':
            model = forecast.load_drafkings()
            data2 = predict_fp(filter,model) #predecir fantasy points
            C,PG,PF,SG,SF = segment_data(data2) # segmentar por posiciones
            n = st.slider('Select the number of best players',0,12,8)
            C = find_better(C,n) # escoger los n  mejores
            PG = find_better(PG,n) # escoger los n  mejores
            PF = find_better(PF,n) # escoger los n  mejores
            SG = find_better(SG,n) # escoger los n  mejores
            SF = find_better(SF,n) # escoger los n  mejores
            output = finals_teams(C,PG,PF,SG,SF,iterations=50)
        elif selection == 'Fanduel':
            model = forecast.load_fanduel()    
            data2 = predict_fp(filter,model) #predecir fantasy points
            C,PG,PF,SG,SF = segment_data(data2,platform='POSITION_F') # segmentar por posiciones
            n = st.slider('Select the number of best players',0,15,8)
            C = find_better(C,n) # escoger los n  mejores
            PG = find_better(PG,n) # escoger los n  mejores
            PF = find_better(PF,n) # escoger los n  mejores
            SG = find_better(SG,n) # escoger los n  mejores
            SF = find_better(SF,n) # escoger los n  mejores
            output = finals_teams(C,PG,PF,SG,SF,iterations=200,limit=60000,platform='SALARY_F.1')

        output = delete_equals(output)   
        st.markdown('# Here is your team!')
        cont=1
        for key,value in output.items():
            st.markdown('#### Team'+str(cont))
            TEXT='Fantasy Points: '+str(round(value['fantasy points'].sum(),2)) +' | '
            if selection=='Drafkings':
                TEXT += 'Salary: $' + str(round(value['SALARY_DK'].sum(),2))+' USD'
            else:
                TEXT += 'Salary: $'+str(round(value['SALARY_F.1'].sum(),2))+' USD'
            st.markdown(TEXT)
            st.write(value)
            cont += 1
    except:
        st.markdown('# Please review your data or parameters, we found errors')
    
    
    
    
    