import pandas as pd





def selec_team(df):

    def suma_PG(lista,bound=12000):
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

    def suma_SG(lista,bound=12000):
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
    def suma_SF(lista,bound=12000):
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
    def suma_PF(lista,bound=12000):
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
    def suma_C(lista,bound=12000):
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


    df_aux_1=df.drop(['PLAYER \nFULL NAME','TEAM'],axis=1)
    score_F=[]
    positions=[]
    for i in range(len(df_aux_1)):

    score_F.append(catb_F.predict(df_aux_1.values)[i])

    df['SCORED_F']=score_F

    df_aux_2=df.drop(['MIN','FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'OR', 'DR', 'TOT', 'A', 'PF', 'ST', 'TO', 'BL', 'PTS', 'USAGE \nRATE (%)', 'DAYS\nREST','VENUE\n(R/H)', 'STARTER\n(Y/N)'],axis=1)
    for i in range(len(df_aux_2)):
    if df_aux_2.at[i,'C']==1:
        positions.append('C')
    elif df_aux_2.at[i,'PF.']==1:
        positions.append('PF')
    elif df_aux_2.at[i,'PG']==1:
        positions.append('PG')
    elif df_aux_2.at[i,'SF']==1:
        positions.append('SF')
    elif df_aux_2.at[i,'SG']==1:
        positions.append('SG')


    df_aux_2=df_aux_2.drop(['C', 'C/PF', 'PF.', 'PF/C', 'PG', 'PG/SF', 'PG/SG', 'SF', 'SF/PF', 'SG', 'SG/SF'],axis=1)
    df_aux_2['POSITION']=positions
    df_aux_2=df_aux_2[['PLAYER \nFULL NAME', 'TEAM','POSITION', 'SALARY_F.1', 'SCORED_F']]

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

    teams=sorted([player_C[0][0][1],players_PG[0][0][1],players_PG[1][0][1],players_PF[0][0][1],players_PF[1][0][1],
        players_SG[0][0][1],players_SG[1][0][1],players_SF[0][0][1],players_SF[1][0][1]])
    k=0
    teams_aux=[]


    while k<len(teams):
    t=teams.count(teams[k])
    k=k+t
    teams_aux.append(t)
    teams_aux_1=[0]*len(teams_aux)
    for i in range(len(teams_aux_1)):
    teams_aux_1[i]=teams_aux[i]-4

    bool_1=all(x<=0 for x in teams_aux_1)

    if bool_1 == True:
    print(total_players)
    print('Total cost')
    print(total_players[0][1]+total_players[1][2]+total_players[2][2]+total_players[3][2]
            +total_players[4][2])
    print("Total scored")
    print(total_players[0][2]+total_players[1][3]+total_players[2][3]+total_players[3][3]
            +total_players[4][3])
    else:
    problema=mode(teams)
    lista_cont=[]

    total_players=sorted(total_players, key = lambda x: x[2])
    z=0
    for i in range(len(total_players)):
        if len(total_players[i])!=3:
        if total_players[i][0][1]==problem or total_players[i][1][1]==problem:
            if  total_players[i][0][2]=='PG':
            
            while players_PG[z][0][1]==problem or players_PG[z][1][1]==problem:
                z=z+1
            total_players[i]=players_PG[z]
            print("ssssssssssssss")