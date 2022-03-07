import streamlit as st
import datetime
import requests
from streamlit_folium import folium_static
import folium
import os
import pandas as pd

st.title('DEEPAGRI - Forecasting French Soft Wheat Production in 2022')

m = folium.Map(location=[47, 1], zoom_start=5)

geojson_path = '/Users/pierre/code/PierreCeraH/deepagri/raw_data/departements.json'
cities_path = '/Users/pierre/code/PierreCeraH/deepagri/raw_data/lewagon_cities.csv'

#for _, city in pd.read_csv(cities_path).iterrows():

#    folium.Marker(
#        location=[city.lat, city.lon],
#        popup=city.city,
#        icon=folium.Icon(color="red", icon="info-sign"),
#    ).add_to(m)

def color_function(feat):
    return "red" if int(feat["properties"]["code"][:1]) < 5 else "blue"

folium.GeoJson(
    geojson_path,
    name="geojson",
    style_function=lambda feat: {
        "weight": 1,
        "color": "black",
        "opacity": 0.25,
        "fillColor": color_function(feat),
        "fillOpacity": 0.25,
    },
    highlight_function=lambda feat: {
        "fillColor": color_function(feat),
        "fillOpacity": .5,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['code', 'nom'],
        aliases=['Code', 'Name'],
        localize=True
    ),
).add_to(m)

folium_static(m)
