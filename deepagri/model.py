import pandas as pd
import numpy as np
from psutil import NIC_DUPLEX_FULL
from deepagri.data_full import get_df_full
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
# from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error
from sklearn.inspection import permutation_importance



def run_model(agg_type="M", model=None, metrics=["mae"], scaler=None, X=None,
              y=None, **kwargs):
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


    if scaler==None:
        scaler=RobustScaler()

    pipe=Pipeline([
                ('Scaler',scaler),
                ('Model',model)
                ])
    return pipe

    df = get_df_full(agg_type=agg_type, **kwargs)

    n_departements=int(df.index.str[5:].nunique())

    if X==None:
        X=df.drop(columns=['Production'])
    if y==None:
        y=df['Production']

    X_train=X[:-n_departements]
    y_train=y[:-n_departements]
    X_test=X[-n_departements:]
    y_test=y[-n_departements:]

    train_size=cv
    test_size=train_size+1

    for i in range(0,X.shape[0]-nb_dep_par_annee,nb_dep_par_annee):
        rang_split=i+nb_dep_par_annee*train_size
        rang_max_test=i+nb_dep_par_annee*test_size

    results = []
    if "mae" in metrics:
        results.append(("mae", mean_absolute_error(y_test, y_pred)))

        if X_test.shape[0]==0:
            break
        model=def_model()
        model=fit_model(model,X_train,y_train)
        score.append(mean_absolute_error(y_true=y_test,y_pred=model.predict(X_test)))

    return score

def permutation_score(pipe,X,y):
    permutation_score = permutation_importance(pipe, X, y, n_repeats=10)
    importance_df = pd.DataFrame(np.vstack((X.columns,permutation_score.importances_mean)).T) # Unstack results from permutation_score
    importance_df.columns=['feature','score decrease']
    return importance_df.sort_values(by="score decrease", ascending = False)

def full_model(cross_val=False):
    '''
    Return a model fitted with the full data and a score of cross_val(if on True)
    '''
    model=build_model

    df=get_df_full()

    X=df.drop(columns=['Production'])
    y=df['Production']

    if cross_val:
        score=cross_val_model(model,X,y)
    else :
        score=[]

    model=fit_model(model(),X,y)

    return model,score

if __name__=='__main__':
    print(full_model(True))
