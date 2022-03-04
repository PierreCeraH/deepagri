import pandas as pd
import numpy as np
from deepagri.data_full import get_df_full
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
# from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error
from sklearn.inspection import permutation_importance

def run_model(agg_type="M", model=None, metrics=["mae"]):
    """
    Fits and returns a model (default XGB), printing selected metrics holding out
    the last year (default mae) and permutation importance on the full data.
    -----------------------
    Params:
    agg_type: ["M", "S", "W"] - Aggregation type for meteo data. See
        meteo_agg.agg_meteo() for more info
    model: model to train. Defaults to an XGB
    metrics: list of metrics to return. Currently only implemented for mae
    """

    if model==None:
        model=XGBRegressor(max_depth=10, n_estimators=100, learning_rate=0.1)

    scaler=RobustScaler()
    pipe=Pipeline([
            ('Scaler',scaler),
            ('Model',model)
    ])

    df = get_df_full(agg_type=agg_type)

    X=df.drop(columns=['Production'])
    y=df['Production']

    X_test=X[-93:]
    y_test=y[-93:]
    X_train=X[:-93]
    y_train=y[:-93]

    pipe.fit(X_train,y_train)

    y_pred=pipe.predict(X_test)

    results = []
    if "mae" in metrics:
        results.append("mae", mean_absolute_error(y_test, y_pred))

    print(results[0][0] + ": " + results[0][1])

    pipe.fit(X, y)

    permutation_score = permutation_importance(pipe, X, y, n_repeats=10)
    importance_df = pd.DataFrame(np.vstack((X.columns,permutation_score.importances_mean)).T) # Unstack results from permutation_score

    print(importance_df.sort_values(by="score decrease", ascending = False))

    return model
