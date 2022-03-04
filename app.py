import streamlit as st
import datetime
import requests

'''
# DeepAgri - Forecasting French wheat production for 2022 !
'''


st.title('Forecasting French Soft Wheat Production - Deep Learning Model')

passenger_count = st.slider('Select a modulus', 1, 10, 2)

traject_date = st.date_input(
    "Date of your traject",
    datetime.date(2022, 1, 1))
st.write('Date of the traject', traject_date)

traject_time = st.time_input('Set the traject time', datetime.time(8, 45))
st.write('Time of the traject', traject_time)

pickup_datetime = datetime.datetime.combine(traject_date, traject_time)

columns = st.columns(2)

#DEPARTURE COORDINATES
#st.markdown('Coordinates of your DEPARTURE point :')
pickup_latitude = columns[0].number_input('Insert the Departure LATITUDE')
#st.write('Departure LATITUDE : ', pickup_latitude)
pickup_longitude = columns[1].number_input('Insert the Departure LONGITUDE')
#st.write('Departure LONGITUDE : ', pickup_longitude)

#ARRIVAL COORDINATES
#st.markdown('Coordinates of your ARRIVAL point :')
dropoff_latitude = columns[0].number_input('Insert the Arrival LATITUDE')
#st.write('Arrival LATITUDE : ', dropoff_latitude)
dropoff_longitude = columns[1].number_input('Insert the Arrival LONGITUDE')
#st.write('Arrival LONGITUDE : ', dropoff_longitude)

bt = st.button('Calculate fare')

params = {
    'pickup_datetime' : pickup_datetime,
    'pickup_longitude' : pickup_longitude,
    'pickup_latitude' : pickup_latitude,
    'dropoff_longitude' : dropoff_longitude,
    'dropoff_latitude' : dropoff_latitude,
    'passenger_count' : passenger_count
}
url = 'https://taxifare.lewagon.ai/predict'

if bt:
    response = requests.get(url, params).json()
    st.write(response['fare'])
