import pandas as pd
from pycaret.regression import *

def predict_fp(data,model):
    data2 = data.drop(['PLAYER \\nFULL NAME','TEAM'],axis=1)
    prediction = predict_model(model, data2)
    prediction.rename(columns={'Label':'fantasy points'},inplace=True)
    return pd.concat([data[['PLAYER \\nFULL NAME','TEAM']],prediction],axis=1)

def segment_data(data,platform='POSITION_DK.1'):
    C=data[data[platform]=='C'].sort_values('fantasy points',ascending=False)
    PG=data[data[platform]=='PG'].sort_values('fantasy points',ascending=False)
    PF=data[data[platform]=='PF'].sort_values('fantasy points',ascending=False)
    SG=data[data[platform]=='SG'].sort_values('fantasy points',ascending=False)
    SF=data[data[platform]=='SF'].sort_values('fantasy points',ascending=False)
    return C,PG,PF,SG,SF

def find_better(data,n=5):
    return data.iloc[0:n]

def random_team(C,PG,PF,SG,SF,seed=1):
    c = C.sample(1,random_state=seed)
    pg = PG.sample(2,random_state=seed)
    pf = PF.sample(1,random_state=seed)
    sg = SG.sample(2,random_state=seed)
    sf = SF.sample(2,random_state=seed)
    return pd.concat([c,pg,pf,sg,sf],axis=0)

def random_team_f(C,PG,PF,SG,SF,seed=1):
    c = C.sample(2,random_state=seed)
    pg = PG.sample(2,random_state=seed)
    pf = PF.sample(1,random_state=seed)
    sg = SG.sample(2,random_state=seed)
    sf = SF.sample(2,random_state=seed)
    return pd.concat([c,pg,pf,sg,sf],axis=0)

def finals_teams(C,PG,PF,SG,SF,iterations=10,limit=50000,platform='SALARY_DK'):
    output={}
    cont = 0
    for i in range(iterations):
        if platform=='SALARY_DK':
            rt = random_team(C,PG,PF,SG,SF,i)
        else:
            rt = random_team_f(C,PG,PF,SG,SF,i)
        if rt[platform].sum()<limit:
            equipos_conteo=rt.groupby('TEAM')['TEAM'].count()
            l_count = len(equipos_conteo[equipos_conteo>4])
            if l_count == 0:
                output['team'+str(cont)]=rt
                cont += 1
    return output