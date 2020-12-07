# Script to run the principal code 
import streamlit as st
import pandas as pd
import os

# local packages
from utils import forecast
#from utils.select_your_team import selec_team

st.title('NBA Fantasy points prediction')

uploaded_file = st.file_uploader("Choose a file",type=['xlsx'])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    st.write(data.head())
    uploaded_file.seek(0)
    # load models
    DF = forecast.load_drafkings()
    FD = forecast.load_fanduel()
    #selec_team(data)

    