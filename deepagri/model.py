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

def cross_val_model(def_model,X,y, cv=5, nb_dep_par_annee=93):
    '''
    Execute a cross validation of the model and return a mae score.
    def_model: function that return a model not fitted
    X,y : the full X and y df
    cv: number of year to train on for each fold
    nb_dep_par_annee : nombre de departements qui composent une année
    '''
    score=[]

    train_size=cv
    test_size=train_size+1

    for i in range(0,X.shape[0]-nb_dep_par_annee,nb_dep_par_annee):
        rang_split=i+nb_dep_par_annee*train_size
        rang_max_test=i+nb_dep_par_annee*test_size

        X_train=X[i:rang_split]
        X_test=X[rang_split:rang_max_test]
        y_train=y[i:rang_split]
        y_test=y[rang_split:rang_max_test]

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
    return importance_df.sort_values(by="score decrease")

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
