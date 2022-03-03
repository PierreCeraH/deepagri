import pandas as pd

def get_data_population(pourcentage=False,annee_start=2009,annee_fin=2021):

    annees=[1968,1975,1982,1990,1999,2008,2013,2018]
    df=pd.DataFrame()
    for annee in annees:
        df_=pd.read_excel('raw_data/population_1964_2018_light.xlsx','DEP_'+str(annee))
        df[annee]=df_['Agriculteurs\nActifs ayant un emploi\nRP'+str(annee)]
        if annee==2018:
            df.index=df_['Département']
    df=df.T
    df=df.rename(columns={'index': 'Année'}, index={'Département': 'Index'})

    nom_dep=df.columns
    nom_dep=nom_dep[0:-4] #nom des département sans les DOM-TOM pour pouvoir boucler dessus

    annees=pd.DataFrame([i for i in range(1968,2023)]) #Liste des années totales

    df_full=df.copy()
    df_full=df_full.merge(annees,left_index=True,right_on=0,how='right')
    df_full=df_full.set_index(0) #Merge du df années et du df pour avoir une ligne par année

    # Calcul des points entre chaques années
    for dep in nom_dep: # Boucle sur les colonnes
        for j in range(7): # Boucle sur les années avec des données sur le df de base
            y_1=df.iloc[j,:][dep]
            y_2=df.iloc[j+1,:][dep]
            x_1=int(df.iloc[j,:].name)
            x_2=int(df.iloc[j+1,:].name)
            coef=(y_2-y_1)/(x_2-x_1) # calcul du coef directeur

            for i in range(x_1+1,x_2): #Boucle sur les années manquantes entre x_1 et x_2 sur le df_full
                valeur_n_1=df_full.loc[i-1][dep]
                df_full.loc[i][dep]=valeur_n_1+coef
        for i in range(x_2+1,2023):
            valeur_n_1=df_full.loc[i-1][dep]
            df_full.loc[i][dep]=valeur_n_1+coef

    df_full=df_full.rename(columns={'01':'1','02':'2','03':'3','04':'4','05':'5','06':'6','07':'7','08':'8','09':'9'})
    df_full.index.name='Année'
    df_full['20']=df_full['2A']+df_full['2B']
    df_full=df_full.drop(columns=["2A","2B","971","972","973","974","92","75"])


    if pourcentage:
        df_pop_full=get_population()
        df_prop=100*df_full/df_pop_full
        df_prop=df_prop.dropna()
        df_full=df_prop.copy()

    df_full=df_full[df_full.index>annee_start-1]
    df_full=df_full[df_full.index<annee_fin+1]

    df=pd.DataFrame(df_full.stack())
    if pourcentage:
        df = df.rename(columns={0:'Pourcentage'})
    else :
        df = df.rename(columns={0:'Agriculteur'})
    df = df.reset_index()
    df['Index']=df['Année'].astype(str)+'-'+df['level_1'].astype(str)

    df = df.drop(['level_1','Année'], axis=1)
    df = df.set_index('Index')

    return df



def get_population():
    '''
    Retourne un dataframe avec la population francaise par région et par année entre 1975 et 2022
    '''

    annees_pop=[str(i) for i in range(1975,2023)]
    df_pop=pd.read_excel('raw_data/estim-pop-dep-sexe-gca-1975-2022.xls',sheet_name=annees_pop,header=4,index_col=0,usecols='A,H')
    df_pop_full=df_pop['1975'].drop('Total',axis=1).copy()

    for annee in annees_pop:
        df_pop_full=df_pop_full.merge(df_pop[str(annee)],left_index=True,right_index=True).dropna()
        df_pop_full=df_pop_full.rename(columns={'Total':int(annee)})

    df_pop_full=df_pop_full[[i for i in range(1975,2023)]]
    df_pop_full=df_pop_full.T
    df_pop_full=df_pop_full.rename(columns={'01':'1','02':'2','03':'3','04':'4','05':'5','06':'6','07':'7','08':'8','09':'9'})
    df_pop_full['20']=df_pop_full['2A']+df_pop_full['2B']
    df_pop_full=df_pop_full.drop(columns=["2A","2B","92","75"])
    df_pop_full.index.name='Année'

    return df_pop_full

if __name__=='__main__':
    print(get_data_population(pourcentage=True))
