#TODO rename this if nobody using it
import pandas as pd
import os


def ohe_regions(df:pd.DataFrame()):

    departements = pd.Series("dpt_"+df.index.astype(str).str[5:], index=df.index)
    dummies = pd.get_dummies(departements)

    return df.join(dummies)

def ohe_cluster_prod(df, cluster=pd.DataFrame()):
    if cluster.empty:
        cluster_path=os.path.join(os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'raw_data'),
                                  'region_prod_cluster.csv')
        cluster = pd.read_csv(cluster_path)
    departments = pd.DataFrame(df.index.astype(str).str[5:].astype(int),
                               index=df.index, columns=['departments'])

    dpts_clustered = departments.merge(cluster, how='left').set_index(departments.index)
    dpts_clustered = dpts_clustered.drop(columns="departments")

    return df.join(dpts_clustered)
