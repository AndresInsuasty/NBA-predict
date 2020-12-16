# Script to run the principal code 
import streamlit as st
import pandas as pd
import os

# local packages
from utils import forecast
from utils.select_your_team_F import team_f
from utils.select_your_team_DK import team_dk

st.title('NBA Fantasy points prediction')
selection=st.selectbox("Select a Platform",['Drafkings','Fanduel'])
uploaded_file = st.file_uploader("Choose a file",type=['xlsx'])

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    st.write(data.head())
    uploaded_file.seek(0) #libera memoria
    try:
        output={}
        if selection == 'Drafkings':
            catb_DK = forecast.load_drafkings()
            output = team_dk(data,catb_DK)
        elif selection == 'Fanduel':
            catb_F = forecast.load_fanduel()    
            output = team_f(data,catb_F)
        st.markdown('# Here is your team!')
        for i in range(1,11):
            st.markdown('### Team '+str(i))
            st.write(output['lineup_'+str(i)])
    except:
        st.markdown('# Please review your data, we found errors')
    
    
    
    
    