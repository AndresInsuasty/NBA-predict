#forecast script using models from ./models

#Libraries
from pycaret.regression import * 


#load models
def load_drafkings():
    try:
        df_model = load_model('utils/models/catb_saved_DF')
        print('Model of Drafkings uploaded')
        return df_model
    except:
        print('Error uploading the model')
        return []
    
def load_fanduel():
    try:
        df_model = load_model('utils/models/catb_saved_Fanduel')
        print('Model of Fanduel uploaded')
        return df_model
    except:
        print('Error uploading the model')
        return []