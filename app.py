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

geojson_path = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/deepagri/data/departements.json?token=GHSAT0AAAAAABRZSTYPRBKUPX6I2JWETXZEYRGDUUQ'

# Dataframe Preprocessing
filepath = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/5d081b5a3fb2185e861d8f37f9bbeb2d88d8bbfe/deepagri/data/Production_Y.csv'
df = pd.read_csv(filepath)
df.drop('Unnamed: 0',axis=1,inplace=True)
df = df.drop('Prod.(t)',axis=1)
df.set_index('Année',inplace=True)
df = df.T
df = df.reset_index()

# Calculating yearly variations in production
for i in range(2001,2022):
    df[f'Var {i}-{i-1}']=round((df[i]-df[i-1])/df[i-1]*100,2)
df = df.drop([i for i in range(2000,2022)], axis=1)

st.markdown("<h1 style='text-align: center; color: black;'>DeepAgri Project</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Forecasting French Soft Wheat Production in 2022</h3>", unsafe_allow_html=True)

st.title('DeepAgri Project')
st.subheader('Forecasting French Soft Wheat Production in 2022')

st.markdown('')
columns_names = st.columns(4)
col_name_0 = columns_names[0].markdown('Pierre CERA-HUELVA')
col_name_1 = columns_names[1].markdown('Gaspar DUPAS')
col_name_2 = columns_names[2].markdown('Constantin TALANDIER')
col_name_3 = columns_names[3].markdown('Wenfang ZHOU')
st.markdown('')
st.markdown('')
st.markdown('')

# Selecting a year with a slider
year = st.slider('Select a year', 2002, 2021, step=1)
st.markdown('')

# Creating the dataframe to plot
df = df[['index',f'Var {year}-{year-1}']]
df['index']=df['index'].astype(str)
df = df.dropna()

# Correcting the problem of '0' with integer below 10
for i in range(0,9):
    df['index'][i]= '0' + df['index'][i]

#Creating charts
df_graph = df.copy()
df_graph = df_graph.drop(0,axis=0)
df_graph['index']=df_graph['index'].astype(str)
df_graph.set_index('index', inplace=True)
df_graph = df_graph.dropna()

chart_data = df_graph[f'Var {year}-{year-1}']

st.bar_chart(chart_data)
st.markdown('')
st.markdown('')

# Build a DataFrame with Cities and lat long in columns
def get_map_data():
    return pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon'])

df_map_cities = get_map_data()
st.map(df_map_cities)

st.markdown('')
st.markdown('')

col_button = st.columns(3)
col_name_0 = col_button[0].text('')
col_name_1 = col_button[1].button('Predict 2022')
col_name_2 = col_button[2].text('')

if col_name_1:
    st.metric("French Soft Wheat 2022", "35.47 MlnT", "+0.52 MlnT vs 2021")
    # Building choropleth map with Folium
    m = folium.Map(location=[47, 1],
                tiles='cartodb positron',
                min_zoom=4,
                max_zoom=7,
                zoom_start=6)

    m.choropleth(
        geo_data=geojson_path,
        data=df,
        columns=['index', f'Var {year}-{year-1}'],
        key_on='feature.properties.code',
        fill_color='YlOrBr',
        fill_opacity=0.8,
        line_opacity=0.4,
        legend_name=f'Production of Soft Wheat - {year}')
    folium_static(m)

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
