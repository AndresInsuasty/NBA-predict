#forecast script using models from ./models

#Libraries
from pycaret.regression import * 


#load models 
def load_fanduel():
    try:
        df_model = load_model('utils/models/model_pre')
        print('Model of Fanduel uploaded')
        return df_model
    except:
        print('Error uploading the model')
        return []