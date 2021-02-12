# Script to run the principal code 
import streamlit as st
import pandas as pd
import numpy as np
import os
import math

# local packages
from utils.load_model import *
from utils.selec_team_ai import *

st.title('NBA Fantasy points prediction')
selection_file = st.selectbox("Select a File extension",['XLSX','CSV',])
uploaded_file = st.file_uploader("Choose a file",type=['csv','xlsx'])
#Cargar archivo
if uploaded_file is not None:
    data = load_data(uploaded_file,selection_file)
    #st.write(data.head())
    uploaded_file.seek(0) #libera memoria
    #Equipos de los datos
    st.dataframe(data)
    data.dropna(subset=['TEAM'],inplace=True) #drop row con equipo nan
    teams = np.sort(data['TEAM'].unique())
    data = prom_values(data)
    #st.dataframe(data)
    
    selected_teams = np.zeros(len(teams))
    #st.write(teams)
    st.markdown('# Select your teams to make predictions please!')

    options = st.multiselect(
        'What teams are going to play?',
        teams)
    filter = data[data['TEAM'].isin(options)]
    filter = filter.reset_index(drop=True)

    fact={}
    teams_se = np.sort(filter['TEAM'].unique())
    col1, col2 = st.beta_columns(2)
    #num_fact = 0    
    num_fact= round(len(teams_se)/2,0)
    cont=0
    if(num_fact > 1):
        for team_s in teams_se:
            if cont<num_fact:
                fact[team_s] = col1.slider('closing '+team_s, 1, int(num_fact))
            else: 
                fact[team_s] = col2.slider('closing '+team_s, 1, int(num_fact))
            cont+=1

    #jugadores para excluir
    filter['namep_team'] = filter['PLAYERS'].str.cat(filter['TEAM'],sep=" | ")
    players = np.sort(filter['namep_team'].unique())
    options = st.multiselect(
        'What players do you want to exclude?',
        players)
    filter = filter[~filter['namep_team'].isin(options)]
    filter.drop(['namep_team'],axis=1,inplace=True)
    filter = filter.reset_index(drop=True)

    st.dataframe(filter)

    salary = st.number_input("Max Salary", value=60000)
    n_teams = st.number_input("¿How much Lineups do you want?", value=20)

    predi = st.checkbox("Predict")
    if predi:  #st.button('Predict')
    #cargamos el modelo
        model = load_fanduel()
        st.title('NBA Fantasy points Results')
        data_predict = predict(filter,model)
        st.write(data_predict)

        print(fact.keys())
        fac_dec=1/(num_fact*2)
        for i in data_predict.index:
            data_predict['FD_PTS'][i] = data_predict['FD_PTS'][i] * (1.05+float(fact[data_predict['TEAM'][i]]*fac_dec))
        #data_predict['FD_PTS'] = data_predict['FD_PTS'] * 
            
        #Generacion de equipos
        st.title('NBA Fantasy points Lineups')
        columns = data_predict.columns
        inicio=0
        fin=6
        SG,SF,PG,PF,C = get_player(data_predict,inicio,fin) 
        arr_team = get_teams(SG,SF,PG,PF,C,inicio,fin)
        output_team = {}
        aux=select_teams(arr_team,columns,output_team,salary,n_teams)
        print(aux)
        output_team.update(aux)
        print('Entre while teams')
        #print("Antes while "+str(len(output_team)))
        while(len(output_team)<n_teams):
            inicio+=1
            fin+=1
            arr_team =  get_teams(SG,SF,PG,PF,C,inicio,fin)
            aux=select_teams(arr_team,columns,output_team,salary,n_teams)
            print(aux)
            output_team.update(aux)
            print('sali output')
            #print("Dentro while "+str(len(output_team)))
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
    
    
    
    