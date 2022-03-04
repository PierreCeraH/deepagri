import pandas as pd
import os

PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data')


def get_prices():
    url = os.path.join(PATH,'Historical_Prices_Grains_modif.xlsx')

    df = pd.read_excel(url, sheet_name='Ratios')

    df['Ratio']=df['Soft Wheat FOB Rouen']/df['Barley FOB Rouen']
    df = df.set_index('Dates')
    df = df.loc['2008-09-01':'2021-03-01',:]
    df = df.reset_index()

    df = df.drop(columns=['Soft Wheat FOB Rouen','Barley FOB Rouen'])
    df = df.rename(columns={'Ratio':'Ratio_BléOrge'})

    df = df.set_index('Dates')
    df = df.drop(df.index[df.index.month.isin([1, 2, 3, 4, 5, 6, 7, 8, 11, 12])])
    df_ = df.reset_index()


    df_ = df_.groupby([df_['Dates'].dt.year,df_['Dates'].dt.month]).median()

    df_ = df_.reset_index(level=0).rename({'Dates':'Year'},axis=1)
    df_ = df_.reset_index(level=0).rename({'Dates':'Month'},axis=1)

    df_sep = df_[df_['Month']==9]
    df_oct = df_[df_['Month']==10]

    df_sep = df_sep.set_index('Year')
    df_sep = df_sep.drop(columns='Month')
    df_oct = df_oct.set_index('Year')
    df_oct = df_oct.drop(columns='Month')
    df_oct = df_oct.rename(columns={'Ratio_BléOrge':'RatioOct'})
    df_sep = df_sep.rename(columns={'Ratio_BléOrge':'RatioSep'})

    dept_to_keep = [80, 62, 2, 51, 60, 26, 27, 59, 76, 77, 10, 89, 14, 20, 55, 21, 86,
                    45, 8, 18, 57, 35, 61, 54, 37, 79, 36, 41, 49, 53, 72, 52, 56, 17,
                    32, 28, 85, 50, 67, 70, 3, 63, 71, 58, 78, 44, 16, 47, 91, 1, 81,
                    95, 88, 31, 68, 38, 82, 39, 25, 23, 43, 12, 22, 69, 87, 42, 24, 11,
                    46, 90, 15, 9, 74, 34, 19, 65, 33, 64, 5, 4, 48, 30, 7, 40, 84, 73,
                    13, 93, 94, 83, 66, 29, 6]

    # BUILDING SEPTEMBER PRICES
    df_ind_sep = pd.DataFrame()

    for index in df_sep.index:
        for dept in dept_to_keep :
            a_row = pd.Series([str(index+1) + '-' + str(dept), df_sep['RatioSep'][index]])
            row_df = pd.DataFrame([a_row])
            df_ind_sep = pd.concat([row_df, df_ind_sep], ignore_index=True)

    df_ind_sep.index = df_ind_sep[0]
    df_ind_sep = df_ind_sep.drop(labels=0, axis=1)
    df_ind_sep = df_ind_sep.rename(columns={1:'RatioSep'})

    # BUILDING OCTOBER PRICES
    df_ind_oct = pd.DataFrame()

    for index in df_oct.index:
        for dept in dept_to_keep :
            a_row = pd.Series([str(index+1) + '-' + str(dept), df_oct['RatioOct'][index]])
            row_df = pd.DataFrame([a_row])
            df_ind_oct = pd.concat([row_df, df_ind_oct], ignore_index=True)

    df_ind_oct.index = df_ind_oct[0]
    df_ind_oct = df_ind_oct.drop(labels=0, axis=1)
    df_ind_oct = df_ind_oct.rename(columns={0:'Year', 1:'RatioOct'})

    return df_ind_sep.join(df_ind_oct, on=0)

def get_prices_2022():
    url = os.path.join(PATH,'Historical_Prices_Grains_modif.xlsx')
    df = pd.read_excel(url, sheet_name='Ratios')
    df['Ratio']=df['Soft Wheat FOB Rouen']/df['Barley FOB Rouen']
    df = df.set_index('Dates')
    df = df.loc['2021-02-20':'2022-02-22',:]
    df = df.reset_index()
    df = df.drop(columns=['Soft Wheat FOB Rouen','Barley FOB Rouen'])
    df = df.rename(columns={'Ratio':'Ratio_BléOrge'})
    df = df.set_index('Dates')
    df = df.drop(df.index[df.index.month.isin([1, 2, 3, 4, 5, 6, 7, 8, 11, 12])])
    df_ = df.reset_index()
    df_ = df_.groupby([df_['Dates'].dt.year,df_['Dates'].dt.month]).median()
    df_ = df_.reset_index(level=0).rename({'Dates':'Year'},axis=1)
    df_ = df_.reset_index(level=0).rename({'Dates':'Month'},axis=1)
    df_sep = df_[df_['Month']==9]
    df_oct = df_[df_['Month']==10]
    df_sep = df_sep.set_index('Year')
    df_sep = df_sep.drop(columns='Month')
    df_oct = df_oct.set_index('Year')
    df_oct = df_oct.drop(columns='Month')
    df_oct = df_oct.rename(columns={'Ratio_BléOrge':'RatioOct'})
    df_sep = df_sep.rename(columns={'Ratio_BléOrge':'RatioSep'})
    dept_to_keep = [80, 62, 2, 51, 60, 26, 27, 59, 76, 77, 10, 89, 14, 20, 55, 21, 86,
                    45, 8, 18, 57, 35, 61, 54, 37, 79, 36, 41, 49, 53, 72, 52, 56, 17,
                    32, 28, 85, 50, 67, 70, 3, 63, 71, 58, 78, 44, 16, 47, 91, 1, 81,
                    95, 88, 31, 68, 38, 82, 39, 25, 23, 43, 12, 22, 69, 87, 42, 24, 11,
                    46, 90, 15, 9, 74, 34, 19, 65, 33, 64, 5, 4, 48, 30, 7, 40, 84, 73,
                    13, 93, 94, 83, 66, 29, 6]
    # BUILDING SEPTEMBER PRICES
    df_ind_sep = pd.DataFrame()
    for index in df_sep.index:
        for dept in dept_to_keep :
            a_row = pd.Series([str(index+1) + '-' + str(dept), df_sep['RatioSep'][index]])
            row_df = pd.DataFrame([a_row])
            df_ind_sep = pd.concat([row_df, df_ind_sep], ignore_index=True)
    df_ind_sep.index = df_ind_sep[0]
    df_ind_sep = df_ind_sep.drop(labels=0, axis=1)
    df_ind_sep = df_ind_sep.rename(columns={1:'RatioSep'})
    # BUILDING OCTOBER PRICES
    df_ind_oct = pd.DataFrame()
    for index in df_oct.index:
        for dept in dept_to_keep :
            a_row = pd.Series([str(index+1) + '-' + str(dept), df_oct['RatioOct'][index]])
            row_df = pd.DataFrame([a_row])
            df_ind_oct = pd.concat([row_df, df_ind_oct], ignore_index=True)
    df_ind_oct.index = df_ind_oct[0]
    df_ind_oct = df_ind_oct.drop(labels=0, axis=1)
    df_ind_oct = df_ind_oct.rename(columns={0:'Year', 1:'RatioOct'})
    df_prices = df_ind_sep.join(df_ind_oct, on=0)
    return df_prices


if __name__=='__main__':
    print(get_prices())
