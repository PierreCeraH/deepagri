from deepagri.meteo_agg import agg_meteo
from deepagri.data_pop import get_data_population
from deepagri.data_price import get_prices_2022
from deepagri.data_rendement import get_data_rendement

import pandas as pd

def get_X_pred(agg_type="W"):

    """ This function returns the X for the prediction of 2022 production"""

    df_meteo = agg_meteo(agg_type=agg_type)

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

    colum = df_2021['tmax_c'].columns

    list_weeks = colum
    list_weeks_2021 = list(list_weeks[9:21])
    list_weeks_2021_2022 = list(list_weeks[21:53])

    list_weeks_2022 = list(list_weeks[0:9])

    list_compl_weeks = list_weeks_2021_2022

    for i in list_weeks[0:21] :
        list_compl_weeks.append(i)

    for i in list_weeks[21:53] :
        list_weeks_2021.append(i)

    list_weeks_2021_fin =  list_weeks_2021[12:]
    list_weeks_2021_fin.extend(list_weeks_2021[0:12])

    list_tuples = []
    for i in list_col :
        for j in list_compl_weeks :
            list_tuples.append((i,j))

    index = pd.MultiIndex.from_tuples(list_tuples, names=["", "week_of_year"])

    df_final_predict = pd.DataFrame(index=df_2022.index, columns=index)

    for i in list_col :

        for j in list_weeks_2022 :
            col = df_2022[i,j]
            df_final_predict[i,j] = col
        for j in list_weeks_2021_fin :
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

    # Yield 2022

    data_rend = get_data_rendement()
    df_final_predict = df_final_predict.merge(data_rend,right_index=True, left_index=True)

    return df_final_predict
