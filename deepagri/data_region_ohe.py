#TODO rename this if nobody using it
import pandas as pd
import os


def ohe_regions(df: pd.DataFrame()):

    departements = pd.Series("dpt_" + df.index.astype(str).str[5:],
                             index=df.index)
    dummies = pd.get_dummies(departements)

    return df.join(dummies)


def ohe_cluster_prod(df, cluster=pd.DataFrame()):
    if cluster.empty:
        cluster_path = os.path.join(
            os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'raw_data'), 'region_prod_cluster.csv')
        cluster = pd.read_csv(cluster_path)
    departments = pd.DataFrame(df.index.astype(str).str[5:].astype(int),
                               index=df.index,
                               columns=['departments'])

    dpts_clustered = departments.merge(cluster,
                                       how='left').set_index(departments.index)
    dpts_clustered = dpts_clustered.drop(columns="departments")

    return df.join(dpts_clustered)


def ohe_13_regions(df: pd.DataFrame()):
    regions = [
        'Auvergne-Rhône-Alpes', 'Hauts-de-France', 'Auvergne-Rhône-Alpes',
        "Provence-Alpes-Côte d'Azur", "Provence-Alpes-Côte d'Azur",
        "Provence-Alpes-Côte d'Azur", 'Auvergne-Rhône-Alpes', 'Grand Est',
        'Occitanie', 'Grand Est', 'Occitanie', 'Occitanie',
        "Provence-Alpes-Côte d'Azur", 'Normandie', 'Auvergne-Rhône-Alpes',
        'Nouvelle-Aquitaine', 'Nouvelle-Aquitaine', 'Centre-Val de Loire',
        'Nouvelle-Aquitaine', 'Corse', 'Bourgogne-Franche-Comté', 'Bretagne',
        'Nouvelle-Aquitaine', 'Nouvelle-Aquitaine', 'Bourgogne-Franche-Comté',
        'Auvergne-Rhône-Alpes', 'Normandie', 'Centre-Val de Loire', 'Bretagne',
        'Occitanie', 'Occitanie', 'Occitanie', 'Nouvelle-Aquitaine',
        'Occitanie', 'Bretagne', 'Centre-Val de Loire', 'Centre-Val de Loire',
        'Auvergne-Rhône-Alpes', 'Bourgogne-Franche-Comté',
        'Nouvelle-Aquitaine', 'Centre-Val de Loire', 'Auvergne-Rhône-Alpes',
        'Auvergne-Rhône-Alpes', 'Pays de la Loire', 'Centre-Val de Loire',
        'Occitanie', 'Nouvelle-Aquitaine', 'Occitanie', 'Pays de la Loire',
        'Normandie', 'Grand Est', 'Grand Est', 'Pays de la Loire', 'Grand Est',
        'Grand Est', 'Bretagne', 'Grand Est', 'Bourgogne-Franche-Comté',
        'Hauts-de-France', 'Hauts-de-France', 'Normandie', 'Hauts-de-France',
        'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 'Occitanie', 'Occitanie',
        'Grand Est', 'Grand Est', 'Auvergne-Rhône-Alpes',
        'Bourgogne-Franche-Comté', 'Bourgogne-Franche-Comté',
        'Pays de la Loire', 'Auvergne-Rhône-Alpes', 'Auvergne-Rhône-Alpes',
        'Ile-de-France', 'Normandie', 'Ile-de-France', 'Ile-de-France',
        'Nouvelle-Aquitaine', 'Hauts-de-France', 'Occitanie', 'Occitanie',
        "Provence-Alpes-Côte d'Azur", "Provence-Alpes-Côte d'Azur",
        'Pays de la Loire', 'Nouvelle-Aquitaine', 'Nouvelle-Aquitaine',
        'Grand Est', 'Bourgogne-Franche-Comté', 'Bourgogne-Franche-Comté',
        'Ile-de-France', 'Ile-de-France', 'Ile-de-France', 'Ile-de-France',
        'Ile-de-France'
    ]


    dpt_region_df = pd.DataFrame({'departments':list(range(1,96)),
                                  'region':regions})
    dpt_region_df = pd.get_dummies(dpt_region_df.set_index('departments'))
    dpt_region_df = dpt_region_df.reset_index()

    departments = pd.DataFrame(df.index.astype(str).str[5:].astype(int),
                               index=df.index,
                               columns=['departments'])

    dpts_clustered = departments.merge(dpt_region_df,
                                       how='left').set_index(departments.index)
    dpts_clustered = dpts_clustered.drop(columns="departments")

    return df.join(dpts_clustered)
