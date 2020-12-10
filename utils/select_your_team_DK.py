from pycaret.regression import *
import pandas as pd
def team_dk(df,catb_DK):
  def read(df,df_aux_1):
    score_F=[]
    positions=[]
    df_score=predict_model(catb_DK,data=df_aux_1)
    for i in range(len(df_score)):
      score_F.append(df_score.values[i][22])

    df['SCORED_DK']=score_F

    df_aux_2=df.drop(['MIN','FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'OR', 'DR', 'TOT', 'A', 'PF', 'ST', 'TO', 'BL', 'PTS', 'USAGE \nRATE (%)', 'DAYS\nREST','VENUE\n(R/H)', 'STARTER\n(Y/N)'],axis=1)
    for i in range(len(df_aux_2)):
      if df_aux_2.at[i,'POSITION_DK.1']=='C':
        positions.append('C')
      elif df_aux_2.at[i,'POSITION_DK.1']=='PF':
        positions.append('PF')
      elif df_aux_2.at[i,'POSITION_DK.1']=='PG':
        positions.append('PG')
      elif df_aux_2.at[i,'POSITION_DK.1']=='SF':
        positions.append('SF')
      elif df_aux_2.at[i,'POSITION_DK.1']=='SG':
        positions.append('SG')


    df_aux_2=df_aux_2.drop(['POSITION_DK.1'],axis=1)
    df_aux_2['POSITION']=positions
    df_aux_2=df_aux_2[['PLAYER \\nFULL NAME', 'TEAM','POSITION', 'SALARY_DK', 'SCORED_DK']]
    return(df_aux_2)
  def suma_PG(lista,bound=12500):
      k=0
      player_list=[]
      player_list_aux=[]
      for i in range(len(lista)):
          k=k+1
          for j in range(k,len(lista)): 
              
              if lista[i][3]+lista[j][3]<=bound:
                  player_list_aux.append(lista[i])
                  player_list_aux.append(lista[j])
                  #salary of two players
                  player_list_aux.append(lista[i][3]+lista[j][3])
                  #points of two players
                  player_list_aux.append(lista[i][4]+lista[j][4])
                  player_list.append(player_list_aux)
                  player_list_aux=[]
      return(player_list)

  def suma_SG(lista,bound=12500):
      k=0
      player_list=[]
      player_list_aux=[]
      for i in range(len(lista)):
          k=k+1
          for j in range(k,len(lista)): 
              
              if lista[i][3]+lista[j][3]<=bound:
                  player_list_aux.append(lista[i])
                  player_list_aux.append(lista[j])
                  #salary of two players
                  player_list_aux.append(lista[i][3]+lista[j][3])
                  #points of two players
                  player_list_aux.append(lista[i][4]+lista[j][4])
                  player_list.append(player_list_aux)
                  player_list_aux=[]
      return(player_list)
  def suma_SF(lista,bound=12500):
      k=0
      player_list=[]
      player_list_aux=[]
      for i in range(len(lista)):
          k=k+1
          for j in range(k,len(lista)): 
              
              if lista[i][3]+lista[j][3]<=bound:
                  player_list_aux.append(lista[i])
                  player_list_aux.append(lista[j])
                  #salary of two players
                  player_list_aux.append(lista[i][3]+lista[j][3])
                  #points of two players
                  player_list_aux.append(lista[i][4]+lista[j][4])
                  player_list.append(player_list_aux)
                  player_list_aux=[]
      return(player_list)
  def suma_PF(lista,bound=12500):
      k=0
      player_list=[]
      player_list_aux=[]
      for i in range(len(lista)):
          k=k+1
          for j in range(k,len(lista)): 
              
              if lista[i][3]+lista[j][3]<=bound:
                  player_list_aux.append(lista[i])
                  player_list_aux.append(lista[j])
                  #salary of two players
                  player_list_aux.append(lista[i][3]+lista[j][3])
                  #points of two players
                  player_list_aux.append(lista[i][4]+lista[j][4])
                  player_list.append(player_list_aux)
                  player_list_aux=[]
      return(player_list)
  def suma_C(lista,bound=6250):
      k=0
      player_list=[]
      player_list_aux=[]
      for i in range(len(lista)):
            
        if lista[i][3]<=bound:
          player_list_aux.append(lista[i])
          
          #salary of two players
          player_list_aux.append(lista[i][3])
          #points of two players
          player_list_aux.append(lista[i][4])
          player_list.append(player_list_aux)
          player_list_aux=[]
      return(player_list)
  def fbool(lista):
    k=0
    teams_aux=[]
    while k<len(lista):
      t=lista.count(lista[k])
      k=k+t
      teams_aux.append(t)
    teams_aux_1=[0]*len(teams_aux)
    for i in range(len(teams_aux_1)):
      teams_aux_1[i]=teams_aux[i]-4
    bool_1=all(x<=0 for x in teams_aux_1)
    return bool_1,max(teams_aux_1)
  def teams_sort(lista):
    team=sorted([lista[0][0][1],lista[1][0][1],lista[1][1][1],
                  lista[2][0][1],lista[2][1][1],lista[3][0][1],
                  lista[3][1][1],lista[4][0][1],lista[4][1][1]])
    return team

  def players(a):
    if a=='PG':
      return players_PG
    if a=='PF':
      return players_PF
    if a=='SF':
      return players_SF
    if a=='SG':
      return players_SG
  def change(team,list_sol,list_problem,j):
    i=0
    while i<=len(list_sol)-1 and (list_sol[i][0][1]==team or list_sol[i][1][1]==team):
      i=i+1
    if i==len(list_sol):
      return print("it is not possible to change")
    else:
      list_problem[j]=list_sol[i]
      return list_problem
  def select_FD(total_players):
    teams=teams_sort(total_players)
    bool_1=fbool(teams)[0]

    if bool_1 == True:
      names=[]
      team=[]
      position=[]
      salary=[]
      points=[]
      names.append(total_players[0][0][0])
      names.append(total_players[1][0][0])
      names.append(total_players[1][1][0])
      names.append(total_players[2][0][0])
      names.append(total_players[2][1][0])
      names.append(total_players[3][0][0])
      names.append(total_players[3][1][0])
      names.append(total_players[4][0][0])
      names.append(total_players[4][1][0])

      team.append(total_players[0][0][1])
      team.append(total_players[1][0][1])
      team.append(total_players[1][1][1])
      team.append(total_players[2][0][1])
      team.append(total_players[2][1][1])
      team.append(total_players[3][0][1])
      team.append(total_players[3][1][1])
      team.append(total_players[4][0][1])
      team.append(total_players[4][1][1])

      position.append(total_players[0][0][2])
      position.append(total_players[1][0][2])
      position.append(total_players[1][1][2])
      position.append(total_players[2][0][2])
      position.append(total_players[2][1][2])
      position.append(total_players[3][0][2])
      position.append(total_players[3][1][2])
      position.append(total_players[4][0][2])
      position.append(total_players[4][1][2])

      salary.append(total_players[0][0][3])
      salary.append(total_players[1][0][3])
      salary.append(total_players[1][1][3])
      salary.append(total_players[2][0][3])
      salary.append(total_players[2][1][3])
      salary.append(total_players[3][0][3])
      salary.append(total_players[3][1][3])
      salary.append(total_players[4][0][3])
      salary.append(total_players[4][1][3])
    
      points.append(total_players[0][0][4])
      points.append(total_players[1][0][4])
      points.append(total_players[1][1][4])
      points.append(total_players[2][0][4])
      points.append(total_players[2][1][4])
      points.append(total_players[3][0][4])
      points.append(total_players[3][1][4])
      points.append(total_players[4][0][4])
      points.append(total_players[4][1][4])
    
      df = pd.DataFrame({'name':names,'team':team,'position':position,'salary':salary,'points':points})
      total=df['salary'].sum()
      if total<=50000:
        print(200000000000)
        df_aux=df.drop([0],axis=0)
        df_1=df_aux.min(axis=0)
        index = df_aux[df_aux['points']==df_1[4]].index.tolist()
        df=df.drop([index[0]],axis=0)
        return df
      else:
        print(10000000000)
        for i in range(1,9):
          if total-df.at[i,'salary']<=50000:
            salary_list.append(df.at[i,'points'])
        m=min(salary_list)
        df_aux=df.drop([0],axis=0)
        df_1=df_aux.min(axis=0)
        index = df_aux[df_aux['points']==m].index.tolist()
        df=df.drop([index[0]],axis=0)
        return df
  

      
    
    else:
    

      problem=mode(teams)
    
      total_players=sorted(total_players, key = lambda x: x[2])
      i=0

      while bool_1==False:
          if len(total_players[i])!=3: 
            if total_players[i][0][1]==problem and total_players[i][1][1]==problem:
              position_list=players(total_players[i][0][2])
              total_players=change(problem,position_list,total_players,i)
          teams=teams_sort(total_players)
          bool_1=fbool(teams)[0]
          i=i+1
    names=[]
    team=[]
    position=[]
    salary=[]
    points=[]
    names.append(total_players[0][0][0])
    names.append(total_players[1][0][0])
    names.append(total_players[1][1][0])
    names.append(total_players[2][0][0])
    names.append(total_players[2][1][0])
    names.append(total_players[3][0][0])
    names.append(total_players[3][1][0])
    names.append(total_players[4][0][0])
    names.append(total_players[4][1][0])

    team.append(total_players[0][0][1])
    team.append(total_players[1][0][1])
    team.append(total_players[1][1][1])
    team.append(total_players[2][0][1])
    team.append(total_players[2][1][1])
    team.append(total_players[3][0][1])
    team.append(total_players[3][1][1])
    team.append(total_players[4][0][1])
    team.append(total_players[4][1][1])

    position.append(total_players[0][0][2])
    position.append(total_players[1][0][2])
    position.append(total_players[1][1][2])
    position.append(total_players[2][0][2])
    position.append(total_players[2][1][2])
    position.append(total_players[3][0][2])
    position.append(total_players[3][1][2])
    position.append(total_players[4][0][2])
    position.append(total_players[4][1][2])

    salary.append(total_players[0][0][3])
    salary.append(total_players[1][0][3])
    salary.append(total_players[1][1][3])
    salary.append(total_players[2][0][3])
    salary.append(total_players[2][1][3])
    salary.append(total_players[3][0][3])
    salary.append(total_players[3][1][3])
    salary.append(total_players[4][0][3])
    salary.append(total_players[4][1][3])
    
    points.append(total_players[0][0][4])
    points.append(total_players[1][0][4])
    points.append(total_players[1][1][4])
    points.append(total_players[2][0][4])
    points.append(total_players[2][1][4])
    points.append(total_players[3][0][4])
    points.append(total_players[3][1][4])
    points.append(total_players[4][0][4])
    points.append(total_players[4][1][4])
    
    
    df = pd.DataFrame({'name':names,'team':team,'position':position,'salary':salary,'points':points})
    total=df['salary'].sum()
    if total<=50000:
      df_aux=df.drop([0],axis=0)
      df_1=df_aux.min(axis=0)
      index = df_aux[df_aux['points']==df_1[4]].index.tolist()
      df=df.drop([index[0]],axis=0)
      return df
    else:
      for i in range(1,9):
        if total-df.at[i,'salary']<=50000:
          salary_list.append(df.at[i,'points'])
      m=min(salary_list)
      df_aux=df.drop([0],axis=0)
      df_1=df_aux.min(axis=0)
      index = df_aux[df_aux['points']==m].index.tolist()
      df=df.drop([index[0]],axis=0)
      return df
  df_aux_1=df.drop(['PLAYER \\nFULL NAME','TEAM'],axis=1)
  df_aux_2=read(df,df_aux_1)
  df_C=df_aux_2[df_aux_2.POSITION == 'C']
  df_SG=df_aux_2[df_aux_2.POSITION == 'SG']
  df_SF=df_aux_2[df_aux_2.POSITION == 'SF']
  df_PG=df_aux_2[df_aux_2.POSITION == 'PG']
  df_PF=df_aux_2[df_aux_2.POSITION == 'PF']
  list_PG=suma_PG(df_PG.values)
  list_PF=suma_PF(df_PF.values)
  list_SG=suma_SG(df_SG.values)
  list_SF=suma_SF(df_SF.values)
  list_C=suma_C(df_C.values)



  player_C=sorted(list_C, reverse=True, key = lambda x: x[2])
  players_PG=sorted(list_PG, reverse=True, key = lambda x: x[3])
  players_PF=sorted(list_PF, reverse=True,key = lambda x: x[3])
  players_SG=sorted(list_SG,reverse=True, key = lambda x: x[3])
  players_SF=sorted(list_SF,reverse=True, key = lambda x: x[3])

  total_players=[player_C[0],players_PG[0],players_PF[0],players_SG[0],players_SF[0]]
  #print(select_FD(total_players))
  return select_FD(total_players)