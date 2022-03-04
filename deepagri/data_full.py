import pandas as pd
from deepagri.data_pop import get_data_population
from deepagri.data_price import get_prices
from deepagri.data_prod import get_production
from deepagri.meteo_agg import agg_meteo
import os

PATH=os.path.dirname(os.path.dirname(__file__))

def get_df_full(agg_type='S'):
    '''
    Return a dataframe with all the data of meteo,
    '''
    df_pop=get_data_population()
    df_prices=get_prices()
    df_prod=get_production()
    df_meteo=agg_meteo(agg_type=agg_type)
    df_matos=pd.read_csv(os.path.join(os.path.join(PATH,'raw_data'),'matos.csv'),index_col='0')

    df=df_pop.merge(df_prod,left_index=True,right_index=True)
    df=df.merge(df_prices,left_index=True,right_index=True)
    df=df.merge(df_matos,left_index=True,right_index=True)
    df=df.rename(columns={'1':"Prix_matos"})

    df_meteo.columns=[' '.join(str(col)).strip() for col in df_meteo.columns.values] #Suppression du multiindex des columns
    df_meteo.columns = df_meteo.columns.get_level_values(0)

    df_meteo=df_meteo.loc[:'2021-95',:].dropna()

    df=df.merge(df_meteo,left_index=True,right_index=True)

    return df





if __name__=='__main__':
    print(get_df_full('M'))
