import pandas as pd
import numpy as np
from deepagri.data_full import get_df_full
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error
from sklearn.inspection import permutation_importance

def build_model(model=None):
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
    elif model=='linear_reg':
        model=LinearRegression()

    scaler=RobustScaler()
    pipe=Pipeline([
                ('Scaler',scaler),
                ('Model',model)
                ])
    return pipe

def fit_model(pipe,X,y):
    '''
    Return a fitted model with the X and y provided
    '''
    pipe.fit(X,y)

    return pipe

def cross_val_model(model, data=pd.DataFrame(), target='rendement',
                    X=pd.DataFrame(), y=pd.DataFrame()):
    '''
    Cross-validates a model by training it on all years except target year, and
    calculate mae for that year.
    Returns list of mae for every year in chronological order

    Input a model and either [data + target] or [X + y]
    If all are passed, [X + y] takes priority

    Returns a dictionary with:
        - key : years
        - value : tuple of (y_pred, mae_score)
    -------------
    Parameters:
    - model: model() object to fit / predict on

    Option 1:
    - data: pd.DataFrame(), full dataframe with X and y
    - target: string, name of target column in data

    Option 2:
    - X: pd.DataFrame(), X dataframe
    - y: pd.DataFrame(), y dataframe
    '''
    if X.empty & y.empty:
        if data.empty:
            return ValueError("Please pass a data object, or an X and y")
        y = data.pop(target)
        X = data

    scores = {}
    for year in X.index.str[:4].unique():
        X_train = X[X.index.str[:4]!=year]
        X_test = X[X.index.str[:4]==year]
        y_train = y[y.index.str[:4]!=year]
        y_test = y[y.index.str[:4]==year]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        scores[year] = ((y_pred, mean_absolute_error(y_test, y_pred)))

    return scores

def permutation_score(pipe,X,y):
    permutation_score = permutation_importance(pipe, X, y, n_repeats=10)
    importance_df = pd.DataFrame(np.vstack((X.columns,permutation_score.importances_mean)).T) # Unstack results from permutation_score
    importance_df.columns=['feature','score decrease']
    return importance_df.sort_values(by="score decrease")

def holdout_score(model, X, y, holdout=93):
    X_train=X[:-holdout]
    X_test=X[-holdout:]
    y_train=y[:-holdout]
    y_test=y[-holdout:]

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = mean_absolute_error(y_test, y_pred)

    return score

def full_model(model=None, cross_val=False, df=pd.DataFrame(), X=pd.DataFrame(),
               y=pd.DataFrame(), holdout=93, **kwargs):
    '''
    Return a model fitted with the full data and a score of cross_val(if on True)
    '''
    model=build_model(model)

    if df.empty:
        df=get_df_full(**kwargs)

    if X.empty:
        X=df.drop(columns=['Production'])
    if y.empty:
        y=df['Production']

    if cross_val:
        score=cross_val_model(model,X,y)
    else :
        score=holdout_score(model, X, y, holdout)

    model=fit_model(model,X,y)

    return model,score

if __name__=='__main__':
    print(full_model(True))
