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

if __name__=='__main__':
    print(get_production())
