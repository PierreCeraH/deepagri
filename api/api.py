import sndhdr
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# define a root `/` endpoint
@app.get("/")
def index():
    return {"ok": True}

#/predict?cluster_0=0&cluster_1=1&cluster_2=0&cluster_3=0&cluster_4=0&windspeed_max_09_n_1=7.766667&windspeed_max_11_n_1=7.733333&tmin_c_10_n_1=27&tmax_c_01=6&dewmax_c_09_n_1=18&uv_idx_01=1.451613&uv_idx_03=2.645161&tmin_deg_10_n_1=2&tmax_c_04=6&dewmax_c_11_n_1=12&snow_mm_03=1.4&tmax_deg_05=23&rain_mm_10_n_1=273.5&rain_mm_11_n_1=17.5

@app.get("/predict")
def predict(cluster_0,
            cluster_1,
            cluster_2,
            cluster_3,
            cluster_4,
            windspeed_max_09_n_1,
            windspeed_max_11_n_1,
            tmin_c_10_n_1,
            tmax_c_01,
            dewmax_c_09_n_1,
            uv_idx_01,
            uv_idx_03,
            tmin_deg_10_n_1,
            tmax_c_04,
            dewmax_c_11_n_1,
            snow_mm_03,
            tmax_deg_05,
            rain_mm_10_n_1,
            rain_mm_11_n_1):

    X_pred=pd.DataFrame({'cluster_0':cluster_0,
        'cluster_1':cluster_1,
        'cluster_2':cluster_2,
        'cluster_3':cluster_3,
        'cluster_4':cluster_4,
        'windspeed_max 09_n-1':windspeed_max_09_n_1,
        'windspeed_max 11_n-1':windspeed_max_11_n_1,
        'tmin_c 10_n-1':tmin_c_10_n_1,
        'tmax_c 01':tmax_c_01,
        'dewmax_c 09_n-1':dewmax_c_09_n_1,
        'uv_idx 01':uv_idx_01,
        'uv_idx 03':uv_idx_03,
        'tmin_deg 10_n-1':tmin_deg_10_n_1,
        'tmax_c 04':tmax_c_04,
        'dewmax_c 11_n-1':dewmax_c_11_n_1,
        'snow_mm 03':snow_mm_03,
        'tmax_deg 05':tmax_deg_05,
        'rain_mm 10_n-1':rain_mm_10_n_1,
        'rain_mm 11_n-1':rain_mm_11_n_1
        },index=[0])
    pipeline = joblib.load('Model_DeepAgri.joblib')

    pred=pipeline.predict(X_pred)
    print(pred)
    return {'Rendement':pred[0]}
