from webbrowser import get
import pandas as pd
from deepagri.data_pop import get_data_population
from deepagri.data_price import get_prices
from deepagri.data_prod import get_production, get_df_all
from deepagri.meteo_agg import agg_meteo
from deepagri.data_rendement import get_data_rendement
from deepagri.data_region_ohe import ohe_regions, ohe_cluster_prod, ohe_13_regions
import os

PATH=os.path.dirname(os.path.dirname(__file__))

def get_df_full(agg_type='S', ohe='full',what='rendement', **kwargs):
    '''
    Return a dataframe with all the data of meteo of the year and the year before,
    prices ratios, population, yield n-1 and price of the matos.
    ---------------
    Parameters:
    agg_type: String 'S', 'M' or 'W'. Aggregation type for the data.
    ohe: String 'full', 'prod_cluster'. What one-hot encoded columns to add for
        department identification
        - 'full' -> OHE on department number
        - 'prod_cluster' -> OHE on departments clustered into 5 by production
        - 'regions_france' -> OHE on departments split by Région
    '''
    df_pop=get_data_population()
    df_prices=get_prices()
    df_prod=get_df_all(what=what)
    df_meteo=agg_meteo(agg_type=agg_type, **kwargs)
    df_matos=pd.read_csv(os.path.join(os.path.join(PATH,'raw_data'),'matos.csv'),index_col='0')

    df=df_pop.merge(df_prod,left_index=True,right_index=True)
    df=df.merge(df_prices,left_index=True,right_index=True)
    df=df.merge(df_matos,left_index=True,right_index=True)
    df=df.rename(columns={'1':"Prix_matos"})

    df_meteo.columns=[' '.join(col).strip() for col in df_meteo.columns.values] #Suppression du multiindex des columns
    df_meteo.columns = df_meteo.columns.get_level_values(0)

    df_meteo=df_meteo.loc[:'2021-95',:].dropna()

    df=df.merge(df_meteo,left_index=True,right_index=True)

    if ohe=='full':
        df=ohe_regions(df)
    if ohe=='prod_cluster':
        df=ohe_cluster_prod(df)
    if ohe=='regions_france':
        df=ohe_13_regions(df)

    return df

if __name__=='__main__':
    print(get_df_full('M'))
