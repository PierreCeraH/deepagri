import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

def weighted_mae(y_test:pd.DataFrame(), y_pred:np.array,
                 df_prod:pd.DataFrame()):
    '''
    Returns weighted mae
    ----------
    Parameters:
    y_test: pd.DataFrame(), the y_test
    y_pred: np.array(), the array return of model.fit(X_test)
    df_prod: pd.DataFrame(), can be full_df, full_df[['production']], or any
        subsample of those two containing every year-dep in y_test
    '''
    year_sum = df_prod.loc[y_test.index].sum()
    y_test_pond = (y_test * df_prod['production'] / year_sum).dropna()
    y_pred_pond = (pd.Series(y_pred, index=y_test.index)
                   * df_prod['production'] / year_sum).dropna()

    return mean_absolute_error(y_test_pond, y_pred_pond) * len(y_test)

def weigh_features(df, df_prod, metric_cols=None):
    df['year'] = df.index.str[:4]
    df['dep'] = df.index.str[5:]

    df_plot = df.join(df_prod, how='left')
    df_plot = df_plot.drop(columns='production_n-1')

    if metric_cols==None:
        metric_cols = df_plot.columns[:-3]

    df_plot[metric_cols] = df_plot.apply(lambda x: x[metric_cols]
                                         * x['production'], axis=1)

    df_plot = df_plot.groupby('year').sum()

    df_plot = df_plot.appy(lambda x: x[metric_cols] / x['production'], axis=1)
