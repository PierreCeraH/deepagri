from webbrowser import get
import pandas as pd
import os

PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data')

def get_production():
    filepath = os.path.join(PATH,'Production_Y.xlsx')

    df = pd.read_excel(filepath)

    df = df.rename(columns={'TOTAL':'FRANCE'})

    y_France = df[['FRANCE']]

    df = df.drop('FRANCE', axis=1)
    df = df.set_index('Année')

    df = df.loc[2009:,:]

    dept_to_keep = [80, 62, 2, 51, 60, 26, 27, 59, 76, 77, 10, 89, 14, 20, 55, 21, 86,
                45, 8, 18, 57, 35, 61, 54, 37, 79, 36, 41, 49, 53, 72, 52, 56, 17,
                32, 28, 85, 50, 67, 70, 3, 63, 71, 58, 78, 44, 16, 47, 91, 1, 81,
                95, 88, 31, 68, 38, 82, 39, 25, 23, 43, 12, 22, 69, 87, 42, 24, 11,
                46, 90, 15, 9, 74, 34, 19, 65, 33, 64, 5, 4, 48, 30, 7, 40, 84, 73,
                13, 93, 94, 83, 66, 29, 6]

    cols_to_drop = []

    for i in range(1,96):
        if i not in dept_to_keep :
            cols_to_drop.append(i)

    df = df.drop(columns=cols_to_drop)

    y = pd.DataFrame(df.stack())

    y = y.rename(columns={0:'Production'})
    y = y.reset_index()
    y['Ind']=y['Année'].astype(int).astype(str)+'-'+y['level_1'].astype(int).astype(str)

    y = y.drop(['level_1','Année'], axis=1)
    y = y.set_index('Ind')

    df=y[['Production']].applymap(lambda x: str(x.replace(',','.')))
    df=df[['Production']].applymap(lambda x: str(x.replace(' ','')))
    df['Production']=pd.to_numeric(df['Production'])

    return df

def get_df_all(what='rendement'):
    '''
    Renvoi un df sous forme d'une colonne avec l'index AAAA-D
    what : soit 'rendement', 'production' ou 'surface'
    '''
    filepath = os.path.join(PATH,'Histo_data_YieldsAreasProd.xlsx')
    df = pd.read_excel(filepath, sheet_name='Blé tendre')

    df = df.rename(columns={'Unnamed: 0':'Année'})
    df = df.set_index('Année')

    col_rendements = []
    col_surfaces = []
    col_prod = []

    for col in df.columns :
        if '1' in col: #rendements
            col_rendements.append(col)
        elif '2' in col: #production
            col_prod.append(col)
        else: #surfaces
            col_surfaces.append(col)

    if what=='rendement':
        df_return=df[col_rendements].drop(['Année',2022],axis=0)
    elif what=='production':
        df_return = df[col_prod].drop(['Année',2022],axis=0)
    elif what=='surface' :
        df_return=df[col_surfaces].drop(['Année',2022],axis=0)

    dept_codes = [1,2,3,4,5,6,7,8,9,10,
                11,12,13,14,15,16,17,18,19,
                21,22,23,24,25,26,27,28,29,30,
                31,32,33,34,35,36,37,38,39,40,
                41,42,43,44,45,46,47,48,49,50,
                51,52,53,54,55,56,57,58,59,60,
                61,62,63,64,65,66,67,68,69,70,
                71,72,73,74,75,76,77,78,79,80,
                81,82,83,84,85,86,87,88,89,90,
                91,92,93,94,95,'FRANCE']

    col_names = df_return.columns

    dict_rename = dict(zip(col_names, dept_codes))

    df_return = df_return.rename(columns=dict_rename)

    df_return = pd.DataFrame(df_return.stack())

    df_return = df_return.rename(columns={0:what})
    df_return = df_return.reset_index()
    df_return['Ind']=df_return['Année'].astype(int).astype(str)+'-'+df_return['level_1'].astype(str)

    df_return = df_return.drop(['level_1','Année'], axis=1)
    df_return = df_return.set_index('Ind')

    return df_return

if __name__=='__main__':
    print(get_df_all())
