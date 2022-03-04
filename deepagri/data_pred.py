from deepagri.meteo_agg import agg_meteo
from deepagri.data_pop import get_data_population
from deepagri.data_price import get_prices_2022

import pandas as pd

def get_X_pred():

    """ This function returns the X for the prediction of 2022 production"""

    df_meteo = agg_meteo(agg_type="W")

    # 2022 meteo

    list_ = []
    for i in df_meteo.index :
        list_.append('2022' in i)

    df_2022 = df_meteo[list_]

    list_col = []
    for i in df_2022.columns :
        if not(i[0] in list_col) :
            list_col.append(i[0])
    list_col

    # 2021 to 2022 meteo

    list_ = []
    for i in df_meteo.index :
        list_.append('2021' in i)

    df_2021 = df_meteo[list_]

    list_weeks = ['01','02','03','04','05','06','07','08','10_n-1','11_n-1','12_n-1','13_n-1','14_n-1','15_n-1','16_n-1','17_n-1','18_n-1','19_n-1','20_n-1','21_n-1','22_n-1']
    list_weeks_2022 = ['01','02','03','04','05','06','07','08']
    list_weeks_2021 = ['10_n-1','11_n-1','12_n-1','13_n-1','14_n-1','15_n-1','16_n-1','17_n-1','18_n-1','19_n-1','20_n-1','21_n-1','22_n-1']

    list_tuples = []
    for i in list_col :
        for j in list_weeks :
            list_tuples.append((i,j))

    index = pd.MultiIndex.from_tuples(list_tuples, names=["", "week_of_year"])

    df_final_predict = pd.DataFrame(index=df_2022.index, columns=index)

    for i in list_col :

        for j in list_weeks_2022 :
            col = df_2022[i,j]
            df_final_predict[i,j] = col
        for j in list_weeks_2021 :
            col = df_2021[i,j]
            df_final_predict[i,j] = list(col)

    df_final_predict.columns=[' '.join(col).strip() for col in df_final_predict.columns.values] #Suppression du multiindex des columns
    df_final_predict.columns = df_final_predict.columns.get_level_values(0)

    # Nbr agri 2022

    data_agg = get_data_population(annee_start=2022,annee_fin=2022)

    df_final_predict = df_final_predict.merge(data_agg,right_index=True, left_index=True)

    # Prices ration 2022

    data_prod = get_prices_2022()

    df_final_predict = df_final_predict.merge(data_prod,right_index=True, left_index=True)

    # Matos 2022

    df_matos = pd.DataFrame(91.6,index=df_2022.index, columns=['Prix_matos'])

    df_final_predict = df_final_predict.merge(df_matos,right_index=True, left_index=True)

    return df_final_predict
