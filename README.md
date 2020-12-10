# NBA-predict
Forecasting of scores or Fantasypoints on Draftkings and Fanduel


# steps
1. Create an environment called NBA with conda
```
conda create -n NBA python=3.6
```

2. if you already have an environment, you can activate with
```
conda activate NBA
```

3. Let's to install streamlit
```
pip install streamlit
```

4. to confirm the correct instalation of streamlit run the code
```
streamlit hello
```
It will appear a Demo in your browser localhost:8501 to stop it Ctrl + c

5. Install pycaret with the following command
```
pip install pycaret
```
6. For me was necessary install xlrd to work with excel files
```
pip install xlrd
```
7. Now we are going to run the code with following command in our terminal
```
streamlit run main.py
```
8. Enjoy the application in your browser in localhost:8501



# Requirements
* python==3.6
* streamlit==0.72
* pycaret==2.2.2
* xlrd==1.2.0