# Script to run the principal code 
import streamlit as st
import pandas as pd
import numpy as np
import os

# local packages
from utils.load_model import *
from utils.selec_team_ai import *

st.title('NBA Fantasy points prediction')
selection_file = st.selectbox("Select a File extension",['CSV','XLSX'])
uploaded_file = st.file_uploader("Choose a file",type=['csv','xlsx'])
#Cargar archivo
if uploaded_file is not None:
    if selection_file=='CSV':
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)
    #st.write(data.head())
    uploaded_file.seek(0) #libera memoria
    #Equipos de los datos
    data.dropna(subset=['TEAM'],inplace=True) #drop row con equipo nan
    teams = data['TEAM'].unique()

    selected_teams = np.zeros(len(teams))
    st.write(teams)
    st.markdown('# Select your teams to make predictions please!')
    for id,team in enumerate(teams):
        selected_teams[id] = st.checkbox(team,value=True)
    #Se concatenan los equipos con los seleccionados
    teams_df = pd.concat([pd.Series(teams),pd.Series(selected_teams)],axis=1)
    teams_df.columns=['TEAM','Selected']
    teams_selected_df = teams_df[teams_df['Selected']==True]
    if st.button('Predict'):
        #filtra los equipos seleccionados 
        filter = data[data['TEAM'].isin(teams_selected_df['TEAM'].to_list())]
        filter = filter.reset_index(drop=True)
        #st.write(filter)
        st.dataframe(filter)

        #cargamos el modelo
        model = load_fanduel()
        st.title('NBA Fantasy points Results')
        data_predict = predict(filter,model)
        st.write(data_predict)

        salary = st.number_input("Max Salary", 60000)

        n_teams = st.number_input("¿How much Lineups do you want?", 20)

        #Generacion de equipos
        st.title('NBA Fantasy points Lineups')
        output_team = get_teams(data_predict,salary,n_teams) 
        #Muestra de equipos
        pts=0
        cont=1
        for key in output_team:
            pts = output_team[key]['FD_PTS'].sum()
            st.subheader('Lineups '+str(cont))
            st.markdown('**_SALARY_** = '+str(round(output_team[key]['FD_SALARY'].sum(),2))+' USD')
            st.markdown('**_FANTASY POINTS_** = '+str(round(pts,2)))
            st.write(output_team[key])
            cont+=1
    
    
    
    