# Script to run the principal code 
import streamlit as st
import pandas as pd
import numpy as np
import os

# local packages
from utils import forecast
from utils.select_your_team_F import team_f
from utils.select_your_team_DK import team_dk

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
    #st.write(data)
    st.write(filter)
    #try:
    output={}
    if selection == 'Drafkings':
        catb_DK = forecast.load_drafkings()
        output = team_dk(filter,catb_DK)
    elif selection == 'Fanduel':
        catb_F = forecast.load_fanduel()    
        output = team_f(filter,catb_F)
    st.markdown('# Here is your team!')
    for i in range(1,11):
        st.markdown('### Team '+str(i))
        st.write(output['lineup_'+str(i)])
    #except:
        #st.markdown('# Please review your data, we found errors')
    
    
    
    
    