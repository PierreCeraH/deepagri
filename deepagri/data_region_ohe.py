import pandas as pd

def ohe_regions(df:pd.DataFrame()):

    departements = pd.Series("dpt_"+df.index.astype(str).str[5:], index=df.index)
    dummies = pd.get_dummies(departements)

    return df.join(dummies)
