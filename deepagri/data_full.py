import pandas as pd
from deepagri.data_pop import get_data_population
from deepagri.data_price import get_prices
from deepagri.data_prod import get_production
from deepagri.meteo_agg import agg_meteo

def get_df_full(agg_type='S'):
    '''
    Return a dataframe with all the data of meteo,
    '''
    df_pop=get_data_population()
    df_prices=get_prices()
    df_prod=get_production()
    df_meteo=agg_meteo(agg_type=agg_type)

    df=df_pop.merge(df_prod,left_index=True,right_index=True)
    df=df.merge(df_prices,left_index=True,right_index=True)

    df_meteo.columns=[' '.join(col).strip() for col in df_meteo.columns.values] #Suppression du multiindex des columns
    df_meteo.columns = df_meteo.columns.get_level_values(0)

    df_meteo=df_meteo.loc[:'2021-95',:].dropna()

    df=df.merge(df_meteo,left_index=True,right_index=True)

    return df





if __name__=='__main__':
    print(get_df_full())
