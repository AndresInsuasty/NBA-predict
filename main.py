# Script to run the principal code 
import streamlit as st
import pandas as pd
import numpy as np
import os

# local packages
from utils import load_model
from utils.selec_team_ai import *

st.title('NBA Fantasy points prediction')
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
    
    
    
    
    