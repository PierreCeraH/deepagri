from webbrowser import get
import pandas as pd
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data')


def get_data_rendement():
    df = pd.read_excel(os.path.join(PATH,'Histo_data_YieldsAreasProd.xlsx'))
    df = df.rename(columns={'Unnamed: 0':'ANNEE'})

    df = df.loc[1:,:]
    df = df.set_index('ANNEE')

    cols = df.columns
    cols_to_drop = []
    for col in cols :
        if '2' not in col:
            cols_to_drop.append(col)

    df = df.drop(cols_to_drop, axis=1)

    df = df.drop('TOTAL.2', axis=1)
    df = df.loc[2009:,:]

    cols = df.columns
    dict_col_to_rename = {}
    i=1
    for col in cols :
        dict_col_to_rename[col]=i
        i = i+1
    df = df.rename(columns=dict_col_to_rename)

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

    df_surfaces = pd.DataFrame(df.stack())

    df_surfaces = df_surfaces.rename(columns={0:'_n-1'})
    df_surfaces = df_surfaces.reset_index()
    df_surfaces['Ind']=df_surfaces['ANNEE'].astype(int).astype(str)+'-'+df_surfaces['level_1'].astype(str)

    df_surfaces = df_surfaces.drop(['level_1','ANNEE'], axis=1)
    df_surfaces = df_surfaces.set_index('Ind')
    df_surfaces=df_surfaces.shift(93).dropna()

    return df_surfaces

if __name__=='__main__':
    print(get_data_rendement())
