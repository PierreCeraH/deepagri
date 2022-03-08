from asyncore import file_dispatcher
import streamlit as st
import datetime
import requests
from streamlit_folium import folium_static
import folium
import os
import pandas as pd
import json

st.title('DEEPAGRI - Forecasting French Soft Wheat Production in 2022')

geojson_path = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/deepagri/data/departements.json?token=GHSAT0AAAAAABRZSTYPRBKUPX6I2JWETXZEYRGDUUQ'

# Dataframe Preprocessing
#filepath = os.path.join('Users','pierre','code','PierreCeraH','deepagri','raw_data','cleaned','Production_Y.xlsx')
filepath = '/Users/pierre/code/PierreCeraH/deepagri/raw_data/cleaned/Production_Y.xlsx'
df = pd.read_excel(filepath)

df = df.drop('Prod.(t)',axis=1)
df.set_index('Année',inplace=True)
df = df.T
df = df.reset_index()

df.fillna(0,inplace=True)

# Calculating yearly variations in production
for i in range(2001,2022):
    df[f'Var {i}-{i-1}']=round((df[i]-df[i-1])/df[i-1]*100,2)

df = df.drop([i for i in range(2000,2022)], axis=1)

# Only one year for testing
df_test = df[['index','Var 2021-2020']]

df_test['index']=df_test['index'].astype(str)

# Correcting the problem of '0' with integer below 10
for i in range(0,9):
    df_test['index'][i]= '0' + df_test['index'][i]


# Building map with Folium
m = folium.Map(location=[47, 1],
               tiles='cartodb positron',
               min_zoom=2,
               max_zoom=7,
               zoom_start=6)


m.choropleth(
    geo_data=geojson_path,
    data=df_test,
    columns=['index', 'Var 2021-2020'],
    key_on='feature.properties.code',
    fill_color='YlOrBr',
    fill_opacity=0.6,
    line_opacity=0.4,
    legend_name='Production of Soft Wheat - 2021',
    bins=[-60, -20, 20, 60, 100, 140, 180, 220])





#def color_function(feat):
    #return "red" if int(feat["properties"]["code"][:1]) < 5 else "blue"

#folium.GeoJson(
#    geojson_path,
#    name="geojson",
#    style_function=lambda feat: {
#        "weight": 1,
#        "color": "black",
#        "opacity": 0.25,
#        "fillColor": "blue",
#        "fillOpacity": 0.25,
#   },
#    highlight_function=lambda feat: {
#        "fillColor": color_function(feat),
#        "fillOpacity": .5,
#    },
#    tooltip=folium.GeoJsonTooltip(
#        fields=['code', 'nom'],
#        aliases=['Code', 'Name'],
#        localize=True
#    ),
#).add_to(m)

folium_static(m)
