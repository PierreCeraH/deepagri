from asyncore import file_dispatcher
import streamlit as st
import datetime
import requests
from streamlit_folium import folium_static
import folium
import os
import pandas as pd
import json
import numpy as np


geojson_path = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/deepagri/data/departements.json?token=GHSAT0AAAAAABRZSTYPRBKUPX6I2JWETXZEYRGDUUQ'

# Dataframe Preprocessing
#filepath = '/Users/pierre/code/PierreCeraH/deepagri/raw_data/cleaned/Production_Y.xlsx'
filepath = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/5d081b5a3fb2185e861d8f37f9bbeb2d88d8bbfe/deepagri/data/Production_Y.csv'
df = pd.read_csv(filepath)

df = df.drop('Prod.(t)',axis=1)
df.set_index('Année',inplace=True)
df = df.T
df = df.reset_index()

# Calculating yearly variations in production
for i in range(2001,2022):
    df[f'Var {i}-{i-1}']=round((df[i]-df[i-1])/df[i-1]*100,2)

df = df.drop([i for i in range(2000,2022)], axis=1)




st.title('Project DEEPAGRI')
st.title('Forecasting French Soft Wheat Production in 2022')

# Selecting a year with a slider
year = st.slider('Select a year', 2002, 2021, step=1)

# Creating the dataframe to plot
df = df[['index',f'Var {year}-{year-1}']]
df['index']=df['index'].astype(str)
df = df.dropna()

# Correcting the problem of '0' with integer below 10
for i in range(0,9):
    df['index'][i]= '0' + df['index'][i]

#Creating charts
df_graph = df.copy()
df_graph.set_index('index', inplace=True)
df_graph = df_graph.dropna()

chart_data = df_graph[f'Var {year}-{year-1}']

columns = st.columns(2)
col_1 = columns[0].area_chart(chart_data)
col_2 = columns[1].bar_chart(chart_data)

# Building map with Folium
m = folium.Map(location=[47, 1],
               tiles='cartodb positron',
               min_zoom=2,
               max_zoom=7,
               zoom_start=6)



m.choropleth(
    geo_data=geojson_path,
    data=df,
    columns=['index', f'Var {year}-{year-1}'],
    key_on='feature.properties.code',
    fill_color='YlOrBr',
    fill_opacity=0.6,
    line_opacity=0.4,
    legend_name=f'Production of Soft Wheat - {year}')


folium_static(m)





bt = st.button('Predict 2022')

if bt:
    st.metric("French Soft Wheat 2022", "35.47 MlnT", "-1.52 MlnT")

#params = {
#    'pickup_datetime' : pickup_datetime,
#    'pickup_longitude' : pickup_longitude,
#    'pickup_latitude' : pickup_latitude,
#    'dropoff_longitude' : dropoff_longitude,
#    'dropoff_latitude' : dropoff_latitude,
#    'passenger_count' : passenger_count
#}
#url = 'https://taxifare.lewagon.ai/predict'

#if bt:
#    response = requests.get(url, params).json()
#    st.write(response['fare'])
