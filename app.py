from asyncore import file_dispatcher
from ctypes import alignment
import streamlit as st
import datetime
import requests
from streamlit_folium import folium_static
import folium
import os
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import seaborn as sns
import time
from apps import department_pred
details = False
# ------------------------------------------------------------------------------
# DEF API FUNCTION
# ------------------------------------------------------------------------------
#@st.cache
def pred(Serie):
    url='https://deepagridocker-tdgkcolwlq-ew.a.run.app/predict'
    params={
        'cluster_0':Serie['cluster_0'],
        'cluster_1':Serie['cluster_1'],
        'cluster_2':Serie['cluster_2'],
        'cluster_3':Serie['cluster_3'],
        'cluster_4':Serie['cluster_4'],
        'windspeed_max_09_n_1':Serie['windspeed_max 09_n-1'],
        'windspeed_max_11_n_1':Serie['windspeed_max 11_n-1'],
        'tmin_c_10_n_1':Serie['tmin_c 10_n-1'],
        'tmax_c_01':Serie['tmax_c 01'],
        'dewmax_c_09_n_1':Serie['dewmax_c 09_n-1'],
        'uv_idx_01':Serie['uv_idx 01'],
        'uv_idx_03':Serie['uv_idx 03'],
        'tmin_deg_10_n_1':Serie['tmin_deg 10_n-1'],
        'tmax_c_04':Serie['tmax_c 04'],
        'dewmax_c_11_n_1':Serie['dewmax_c 11_n-1'],
        'snow_mm_03':Serie['snow_mm 03'],
        'tmax_deg_05':Serie['tmax_deg 05'],
        'rain_mm_10_n_1':Serie['rain_mm 10_n-1'],
        'rain_mm_11_n_1':Serie['rain_mm 11_n-1']
    }
    resp=requests.get(url,params).json()
    return(resp['Rendement'])

# ------------------------------------------------------------------------------
# GETTING THE DATAFRAME
# ------------------------------------------------------------------------------

geojson_path = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/deepagri/data/departements.json?token=GHSAT0AAAAAABRZSTYPRBKUPX6I2JWETXZEYRGDUUQ'

# Dataframe Preprocessing
filepath = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/5d081b5a3fb2185e861d8f37f9bbeb2d88d8bbfe/deepagri/data/Production_Y.csv'
df = pd.read_csv(filepath)
df.drop('Unnamed: 0',axis=1,inplace=True)


# ------------------------------------------------------------------------------
# SHAPING THE STREAMLIT INTERFACE
# ------------------------------------------------------------------------------

image_url = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/agr_top_im.jpg'
st.image(image_url, channels="RGB", output_format="auto")

st.markdown("<h3 style='text-align: center; color: #808080;'>Forecasting French Soft Wheat Production in 2022</h3>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: #608080;'>Machine Learning model - Forecasting before March 1st (harvest in July)</h6>", unsafe_allow_html=True)
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
# # Build columns with features
# image_meteo = 'https://github.com/PierreCeraH/deepagri/blob/1967bcc27bc69827029dd6be9016982072cf3865/meteo.jpeg?raw=True'
# image_bourse = 'https://github.com/PierreCeraH/deepagri/blob/1967bcc27bc69827029dd6be9016982072cf3865/cours_bourse.jpg?raw=True'
# image_ble = 'https://github.com/PierreCeraH/deepagri/blob/1967bcc27bc69827029dd6be9016982072cf3865/ble_recole.jpg?raw=True'

# st.markdown("<h3 style='text-align: center; color: #408080;'>Features</h3>", unsafe_allow_html=True)
# st.markdown('')
# st.markdown('')
# col_features = st.columns(3)
# col_feat_0 = col_features[0].markdown("<h6 style='text-align: center; color: #308080;'>Weather data</h6>", unsafe_allow_html=True)
# col_feat_0 = col_features[0].image(image_meteo)
# col_feat_1 = col_features[1].markdown("<h6 style='text-align: center; color: #308080;'>Historical Areas & Yields </h6>", unsafe_allow_html=True)
# col_feat_1 = col_features[1].image(image_ble)
# col_feat_2 = col_features[2].markdown("<h6 style='text-align: center; color: #308080;'>Historical Prices</h6>", unsafe_allow_html=True)
# col_feat_2 = col_features[2].image(image_bourse)

# # ------------------------------------------------------------------------------
# # BUILDING THE MAP WITH CITIES
# # ------------------------------------------------------------------------------
# st.markdown('')
# st.markdown('')
# st.markdown("<h3 style='text-align: center; color: #408080;'>Cities used for data collection</h3>", unsafe_allow_html=True)
# st.markdown('')

# image_path = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/deepagri/data/ville_name_id_coords.csv'
# df_map_cities = pd.read_csv(image_path)
# df_map_cities = df_map_cities.drop(['Unnamed: 0','id'], axis=1)
# df_map_cities = df_map_cities.rename(columns={'long':'lon'})
# st.map(df_map_cities,zoom=4.8)
# st.markdown('')
# st.markdown('')

# ------------------------------------------------------------------------------
# CREATING A CENTERED BUTTON
# ------------------------------------------------------------------------------
col11, col21, col31 = st.columns(3)
bt = col21.button('Prediction for 2022')
# col_button = st.columns(3)
# col_name_0 = col_button[0].text('')
# col_name_1 = col_button[1].text('')
# bt = col_button[2].button('Prediction 2022')
# col_name_3 = col_button[3].text('')
# col_name_4 = col_button[4].text('')

# ------------------------------------------------------------------------------
#GETTING RESULTS FROM THE API & SHOWING MAP
# ------------------------------------------------------------------------------
#if bt:
# ------------------------------------------------------------------------------
# RETRIEVING RESULTS FROM THE API
# ------------------------------------------------------------------------------

#@st.cache(suppress_st_warning=True)
def show_predict():
    api_file = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/notebooks/X_pred_2022_final.csv'
    df_2022 = pd.read_csv(api_file)
    df_2022['Unnamed: 0'] = df_2022['Unnamed: 0'].str[5:]
    df_2022['Unnamed: 0'] = df_2022['Unnamed: 0'].apply(lambda x : x.zfill(2))
    df_2022.rename(columns={'Unnamed: 0':'dept'},inplace=True)
    df_2022.set_index('dept',inplace=True)

    # --------------------------------------------------------------------------
    # ADDING A PROGRESS BAR
    # --------------------------------------------------------------------------
    'Suspense...Calculating...'
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)
    df_pred=pd.DataFrame(columns=[0])

    #gif_image = 'https://github.com/PierreCeraH/deepagri/blob/streamlit-with-page/video_parf.mp4?raw=true'
    gif_image = 'https://github.com/PierreCeraH/deepagri/blob/master/video_parf.mp4?raw=true'
    #st.video(gif_image)
    st.markdown(f'''<video controls autoplay width="703">
                <source src={gif_image} type="video/mp4">
                </video>''', unsafe_allow_html=True)
    # st.markdown(f'<img src={gif_image}/>', unsafe_allow_html=True)
    count = 7
    for i,s in df_2022.iterrows():
        df_pred.loc[i]=pred(s)
        # Update the progress bar with each iteration.
        bar.progress(count + 1)
        count += 1
    time.sleep(0.5)

    #df_pred = pd.DataFrame(df_2022.apply(pred, axis=1))

    surfaces_2022_file = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/surfaces2022.csv'
    df_surfaces_2022 = pd.read_csv(surfaces_2022_file)
    df_surfaces_2022['Unnamed: 0'] = df_surfaces_2022['Unnamed: 0'].apply(lambda x : x.zfill(2))
    df_surfaces_2022.rename(columns={'Unnamed: 0':'dept'},inplace=True)

    df_surfaces_2022.set_index('dept',inplace=True)
    df_pred_2022 = df_surfaces_2022.merge(df_pred,left_index=True,right_index=True)
    df_pred_2022['prod']=df_pred_2022['2022']*df_pred_2022[0]
    df_pred_2022.drop(['2022',0],axis=1,inplace=True)

    df_pred_2022.loc['00']=df_pred_2022['prod'].sum()
    df_pred_2022.rename(columns={'prod':2022},inplace=True)



# ------------------------------------------------------------------------------
# CREATING THE DADDY DATAFRAME
# ------------------------------------------------------------------------------

    df_gr = df.copy()
    df_gr.rename(columns={"Prod.(t)":'00'},inplace=True)
    df_gr.set_index('Année',inplace=True)
    # Correcting the problem of '0' with integer below 10
    for i in range(1,10):
        df_gr.rename(columns={f'{i}' : f'0{i}'},inplace=True)

    df_gr = df_gr.reset_index()
    df_gr.drop(['75','92'],axis=1,inplace=True)
    df_gr.set_index('Année',inplace=True)

    df_big = df_gr.T
    df_final = df_big.join(df_pred_2022, how='left')
    df_final[2022]=df_final[2022]/10

    prediction_FRANCE = round(df_final[2022]['00']/1_000_000,2)
    var_vs_2021 = round((df_final[2022]['00'] - df_final[2021]['00'])/1_000_000,2)

    # ------------------------------------------------------------------------------
    # BUILDING THE DF_VAR FOR THE CHOROCLETH MAP
    # ------------------------------------------------------------------------------

    df_var = df.copy()

    df_var = df_var.drop('Prod.(t)',axis=1)
    df_var.set_index('Année',inplace=True)
    df_var = df_var.T
    df_var = df_var.reset_index()
    df_var['index']=df_var['index'].astype(str).apply(lambda x: x.zfill(2))

    df_var = df_var.merge(df_final[2022], left_on='index', right_index=True, how='left')
    df_var = df_var.dropna()


    # # Calculating yearly variations in production
    # for i in range(2001,2022+1):
    #    df_var[f'Var {i}-{i-1}']=round((df[i]-df[i-1])/df[i-1]*100,2)
    # df_var = df_var.drop([i for i in range(2000,2022)], axis=1)

    # ------------------------------------------------------------------------------
    # YEAR TO MODIFY WITH 2022 ONCE MODEL IS READY AND RESULTS IN DF
    year = 2022
    # ------------------------------------------------------------------------------

    df_var = df_var[['index',year-1, year]]

    # # % Variation in % CONTRIBUTION vs. last year
    # df_var[f'Var {year}-{year-1}'] = ((df_var[year] / df_var[year].sum()*100)
    #                                 - (df_var[year-1] / df_var[year-1].sum()*100))

    # % Variation in PRODUCTION vs. last year
    df_var[f'Var {year}-{year-1}'] = (df_var[year] - df_var[year-1]) / df_var[year-1]*100

    df_var.loc[df_var[2021]<100_000, f'Var {year}-{year-1}'] = 0
    df_var.loc[df_var['index'].isin(['20','75']), f'Var {year}-{year-1}'] = 0 # Paris + Corse
    df_var.loc[df_var['index']=='28', f'Var {year}-{year-1}'] = 0 # Outlier: ~+1m, +273%
    df_var.loc[df_var['index']=='26', f'Var {year}-{year-1}'] = 0 # Outlier: ~-1m, -92%

    df_var = df_var[['index', f'Var {year}-{year-1}']]

    # ------------------------------------------------------------------------------
    # BUILDING DF_CLUSTER FOR CHOROPLETH
    # ------------------------------------------------------------------------------

    df_cluster = pd.read_csv(
        'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/region_cluster.csv',
        index_col=False)
    # df_cluster = df_cluster.drop(columns='Unnamed: 0')
    df_cluster['region'] = df_cluster['region'].astype(str).apply(lambda x: x.zfill(2))


# ------------------------------------------------------------------------------
# PLOTTING THE CHOROPLETH MAP WITH RESULTS
# ------------------------------------------------------------------------------

    # st.markdown('### Departments of France, clustered by Production')
    # st.markdown('')

    # cm = folium.Map(location=[47, 1],
    #             tiles='cartodb positron',
    #             min_zoom=5,
    #             max_zoom=7,
    #             zoom_start=5.5)

    # cm.choropleth(
    #     geo_data=geojson_path,
    #     data=df_cluster,
    #     columns=['region', 'cluster'],
    #     key_on='feature.properties.code',
    #     fill_color='YlOrBr',
    #     fill_opacity=0.8,
    #     line_opacity=0.4,
    #     legend_name=f'Production cluster')

    # folium_static(cm)

    st.markdown('')
    # st.metric("French Soft Wheat 2022", f'{prediction_FRANCE} MlnT', f'{var_vs_2021} MlnT vs 2021')

    col_results = st.columns(3)
    col_results_0 = col_results[0].text('')
    results = col_results[1].metric("French Soft Wheat 2022", f'{prediction_FRANCE} MlnT', f'{var_vs_2021} MlnT vs 2021')
    col_results_3 = col_results[2].text('')

    m = folium.Map(location=[47, 1],
                tiles='cartodb positron',
                min_zoom=5,
                max_zoom=7,
                zoom_start=5.5)

    m.choropleth(
        geo_data=geojson_path,
        data=df_var,
        columns=['index', f'Var {year}-{year-1}'],
        key_on='feature.properties.code',
        fill_color='YlOrBr',
        fill_opacity=0.8,
        line_opacity=0.4,
        legend_name=f'Production of Soft Wheat - {year}')

    folium_static(m)

    st.session_state.df_final = df_final

if bt:
    show_predict()

if "department_view" not in st.session_state:
    col1, col2, col3 = st.columns(3)
    details = col2.button('View Departments')

if details or "department_view" in st.session_state:
    st.session_state.department_view = True
    department_pred.show_table(st.session_state.df_final)

# if st.button("prediction"):

#     st.write("I do the pred")

#     # call the pred HERE

#     st.session_state.prediction_result = pd.DataFrame(dict(a=[1, 3], b=[2, 4]))

# # print the results
# if "prediction_result" in st.session_state:

#     filter = st.selectbox("select an option", ["1", "3"])

#     st.session_state.prediction_result[st.session_state.prediction_result.a == int(filter)]

# else:

#     "pas de pred"
