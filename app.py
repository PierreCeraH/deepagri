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

geojson_path = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/deepagri/data/departements.json?token=GHSAT0AAAAAABRZSTYPRBKUPX6I2JWETXZEYRGDUUQ'

# Dataframe Preprocessing
filepath = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/5d081b5a3fb2185e861d8f37f9bbeb2d88d8bbfe/deepagri/data/Production_Y.csv'
df = pd.read_csv(filepath)
df.drop('Unnamed: 0',axis=1,inplace=True)

# ------------------------------------------------------------------------------
# BUILDING THE DF_VAR FOR THE CHOROCLETH MAP
# ------------------------------------------------------------------------------

df_var = df.copy()
#df_gr = df.copy()

df_var = df_var.drop('Prod.(t)',axis=1)
df_var.set_index('Année',inplace=True)
df_var = df_var.T
df_var = df_var.reset_index()

# Calculating yearly variations in production
#for i in range(2001,2022):
#    df_var[f'Var {i}-{i-1}']=round((df[i]-df[i-1])/df[i-1]*100,2)
#df_var = df_var.drop([i for i in range(2000,2022)], axis=1)

for i in range(2001,2022):
    df_var[f'Var {i}-{i-1}']=df_var[i]/df_var[i].sum()*100 - df_var[i-1]/df_var[i-1].sum()*100
df_var = df_var.drop([i for i in range(2000,2022)], axis=1)

# ------------------------------------------------------------------------------
# YEAR TO MODIFY WITH 2022 ONCE MODEL IS READY AND RESULTS IN DF
year = 2017
# ------------------------------------------------------------------------------

# Creating the dataframe to plot
df_var = df_var[['index',f'Var {year}-{year-1}']]
df_var['index']=df_var['index'].astype(str)
df_var = df_var.dropna()

# Correcting the problem of '0' with integer below 10
for i in range(0,9):
    df_var['index'][i]= '0' + df_var['index'][i]

# ------------------------------------------------------------------------------
# SHAPING THE STREAMLIT INTERFACE
# ------------------------------------------------------------------------------

image_url = 'https://github.com/PierreCeraH/deepagri/blob/master/photo_wheat.jpg?raw=true'
st.image(image_url, channels="RGB", output_format="auto")

st.markdown("<h3 style='text-align: center; color: #808080;'>Forecasting French Soft Wheat Production in 2022</h3>", unsafe_allow_html=True)
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')

# Build columns with features
image_meteo = 'https://github.com/PierreCeraH/deepagri/blob/1967bcc27bc69827029dd6be9016982072cf3865/meteo.jpeg?raw=True'
image_bourse = 'https://github.com/PierreCeraH/deepagri/blob/1967bcc27bc69827029dd6be9016982072cf3865/cours_bourse.jpg?raw=True'
image_ble = 'https://github.com/PierreCeraH/deepagri/blob/1967bcc27bc69827029dd6be9016982072cf3865/ble_recole.jpg?raw=True'

st.markdown("<h3 style='text-align: center; color: #408080;'>Features</h3>", unsafe_allow_html=True)
st.markdown('')
st.markdown('')
col_features = st.columns(3)
col_feat_0 = col_features[0].markdown("<h6 style='text-align: center; color: #308080;'>Weather data</h6>", unsafe_allow_html=True)
col_feat_0 = col_features[0].image(image_meteo)
col_feat_1 = col_features[1].markdown("<h6 style='text-align: center; color: #308080;'>Historical Areas & Yields </h6>", unsafe_allow_html=True)
col_feat_1 = col_features[1].image(image_ble)
col_feat_2 = col_features[2].markdown("<h6 style='text-align: center; color: #308080;'>Historical Prices</h6>", unsafe_allow_html=True)
col_feat_2 = col_features[2].image(image_bourse)

# ------------------------------------------------------------------------------
# BUILDING THE MAP WITH CITIES
# ------------------------------------------------------------------------------
st.markdown('')
st.markdown('')
st.markdown("<h3 style='text-align: center; color: #408080;'>Cities used for data collection</h3>", unsafe_allow_html=True)
st.markdown('')

image_path = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/deepagri/data/ville_name_id_coords.csv'
df_map_cities = pd.read_csv(image_path)
df_map_cities = df_map_cities.drop(['Unnamed: 0','id'], axis=1)
df_map_cities = df_map_cities.rename(columns={'long':'lon'})
st.map(df_map_cities,zoom=4.8)
st.markdown('')
st.markdown('')

# ------------------------------------------------------------------------------
# CREATING A CENTERED BUTTON
# ------------------------------------------------------------------------------
col_button = st.columns(5)
col_name_0 = col_button[0].text('')
col_name_1 = col_button[1].text('')
bt = col_button[2].button('Predict 2022')
col_name_3 = col_button[3].text('')
col_name_4 = col_button[4].text('')

# ------------------------------------------------------------------------------
#GETTING RESULTS FROM THE API & SHOWING MAP
# ------------------------------------------------------------------------------
if bt:
# ------------------------------------------------------------------------------
# RETRIEVING RESULTS FROM THE API
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
# PLOTTING THE CHOROPLETH MAP WITH RESULTS
# ------------------------------------------------------------------------------
    st.metric("French Soft Wheat 2022", "35.47 MlnT", "+0.52 MlnT vs 2021")

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

# ------------------------------------------------------------------------------
# PLOTTING THE EVOLUTION OF A CHOSEN DEPARTMENT PRODUCTION
# ------------------------------------------------------------------------------

    df_graph_dept = df.copy()
    df_graph_dept = df_graph_dept.rename(columns={'Prod.(t)':'00'})
    df_graph_dept.set_index('Année',inplace=True)
    df_graph_dept = df_graph_dept.T
    df_graph_dept = df_graph_dept.reset_index()
    df_graph_dept['index']=df_graph_dept['index'].astype(str)
    df_graph_dept = df_graph_dept.dropna()

    # Correcting the problem of '0' with integer below 10
    for i in range(0,9):
        df_graph_dept['index'][i]= '0' + df_graph_dept['index'][i]
    df_graph_dept.set_index('index',inplace=True)

    liste_noms_dept = ['00 - FRANCE','01 - Ain','02 - Aisne','03 - Allier','04 - Alpes-de-Haute-Provence',
                '05 - Hautes-Alpes','06 - Alpes-Maritimes','07 - Ardèche','08 - Ardennes',
                '09 - Ariège','10 - Aube','11 - Aude','12 - Aveyron',
                '13 - Bouches-du-Rhône','14 - Calvados','15 - Cantal','16 - Charente',
                '17 - Charente-Maritime','18 - Cher','19 - Corrèze',
                "21 - Côte-d'Or","22 - Côtes-d'Armor","23 - Creuse","24 - Dordogne",
                "25 - Doubs","26 - Drôme","27 - Eure","28 - Eure-et-Loir",
                "29 - Finistère","30 - Gard","31 - Haute-Garonne","32 - Gers",
                "33 - Gironde","34 - Hérault","35 - Ille-et-Vilaine","36 - Indre",
                "37 - Indre-et-Loire","38 - Isère","39 - Jura","40 - Landes",
                "41 - Loir-et-Cher","42 - Loire","43 - Haute-Loire","44 - Loire-Atlantique",
                "45 - Loiret","46 - Lot","47 - Lot-et-Garonne","48 - Lozère",
                "49 - Maine-et-Loire","50 - Manche","51 - Marne","52 - Haute-Marne",
                "53 - Mayenne","54 - Meurthe-et-Moselle","55 - Meuse","56 - Morbihan",
                "57 - Moselle","58 - Nièvre","59 - Nord","60 - Oise",
                "61 - Orne","62 - Pas-de-Calais","63 - Puy-de-Dôme","64 - Pyrénées-Atlantiques",
                "65 - Hautes-Pyrénées","66 - Pyrénées-Orientales","67 - Bas-Rhin","68 - Haut-Rhin",
                "69 - Rhône","70 - Haute-Saône","71 - Saône-et-Loire","72 - Sarthe",
                "73 - Savoie","74 - Haute-Savoie","76 - Seine-Maritime","77 - Seine-et-Marne",
                "79 - Deux-Sèvres","80 - Somme","81 - Tarn","82 - Tarn-et-Garonne",
                "83 - Var","84 - Vaucluse","85 - Vendée","86 - Vienne",
                "87 - Haute-Vienne","88 - Vosges","89 - Yonne","90 - Territoire de Belfort",
                "91 - Essonne","93 - Seine-Saint-Denis","94 - Val-de-Marne","95 - Val-d'Oise"]

    df_gr = df.copy()
    df_gr.rename(columns={'Prod.(t)':'00'})
    df_gr.set_index('Année',inplace=True)
    df_gr = df_gr.T
    df_gr = df_gr.reset_index()

    zeros = np.zeros(96)
    df_gr[2022]=zeros
    #df_gr[2022]['00']=40_000_000
    df_gr[[2022]]=df_gr[[2021]]

    liste_noms_dept.insert(0,'Pick a department')
    option = st.selectbox('Select a department', liste_noms_dept)
    opt_num = option[:2]




    if option!='Pick a department':

        #zeros = np.zeros(96)
        #df_graph_dept[2022]=zeros
        #df_graph_2022 = pd.DataFrame(np.zeros((1,len(df_graph_dept.columns))), columns=df_graph_dept.columns)
        # ----------------------------------------------------------------------
        #df_graph_2022[2022]=40_000_000    #TO BE MODIFIED WITH 2022 PREDICTIONS
        # ----------------------------------------------------------------------
        #df_final_graph = pd.concat((df_graph_2022.T,df_graph_dept.loc[opt_num,:]),axis=1)
        #df_final_graph.rename(columns={0:option,'00':'2022'},inplace=True)

        alt.Chart(df_gr).mark_bar().encode(
        x='Année',
        y="index",
        color=alt.condition(
            alt.datum.year == 2022,  # PRECISE THE DTYPE OF 2022 : str or int
            alt.value('orange'),     # which sets the bar orange.
            alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
        )
        ).properties(width=600)


    st.markdown("<h6 style='text-align: center; color: #708090;'>DeepAgri Project - Le Wagon - Data Science - Batch #802</h6>", unsafe_allow_html=True)
    columns_names = st.columns(4)
    col_name_0 = columns_names[0].markdown("<h7 style='text-align: center; color: #708090;'>Pierre Cera-Huelva</h7>", unsafe_allow_html=True)
    col_name_1 = columns_names[1].markdown("<h7 style='text-align: center; color: #708090;'>Gaspar Dupas</h7>", unsafe_allow_html=True)
    col_name_2 = columns_names[2].markdown("<h7 style='text-align: center; color: #708090;'>Constantin Talandier</h7>", unsafe_allow_html=True)
    col_name_3 = columns_names[3].markdown("<h7 style='text-align: center; color: #708090;'>Wenfang Zhou</h7>", unsafe_allow_html=True)
