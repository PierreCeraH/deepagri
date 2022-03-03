# Package to aggregate meteo data
# -------------------------------------------------------
# Expected inputs:
# ../raw_data/Meteo/historique_meteo_daily.csv
# ../raw_data/Meteo/scraped_meteo_name_key.xlsx

import pandas as pd
import numpy as np

REGION_KEY_OFFSET = 41

def count_outliers(series, threshold=1, greater=True):
    """
    Aggregator function to count occurences greater / smaller than n standard
    deviations.
    ------------
    Params:
    threshold: Number of standard deviations to set as a threshold. Default 1
    greater: Boolean. If true, will count occurences greater than the given
            threshold. If false, will count occurences smaller than the given
            threshold.
    """
    if greater:
        return (series >= (series.mean() + threshold * series.std())).sum()
    elif not greater:
        return (series <= (series.mean() - threshold * series.std())).sum()
    else:
        raise TypeError("Argument 'greater' should be a boolean")


class MeteoAggregator():

    def __init__(self,
                 meteo_data='../raw_data/Meteo/historique_meteo_daily.csv',
                 cleaning_key='../raw_data/Meteo/scraped_meteo_name_key.xlsx',
                 region_key='../raw_data/Meteo/Classement_Departement.xlsx'):
        self.df = pd.read_csv(meteo_data)
        self.clean_key = pd.read_excel(cleaning_key)
        self.clean_key = self.clean_key[self.clean_key['keep']==1.0]

        self.region_key = pd.read_excel(region_key)
        self.region_key = (self.region_key[REGION_KEY_OFFSET:]
                           .dropna(subset=['id_hist_meteo']))
        self.region_key[['Departement','id_hist_meteo']] = (
            self.region_key[['Departement','id_hist_meteo']].astype(int))


    def clean_names(self, df=pd.DataFrame(), col_clean='name_clean'):
        if df.empty:
            df = self.df
        df = df[self.clean_key[col_clean]]
        return df

    def add_dept(self, df=pd.DataFrame(), col_region='id_hist_meteo'):
        """Adds a 'code_dep' column to df"""

        region_key = self.region_key
        region_key = region_key.dropna(subset=[col_region])
        region_key['code_dep'] = region_key['Departement'].astype(str).str[:2]

        if df.empty:
            df = self.df
        df = (df.merge(region_key[['code_dep', col_region]],
                       left_on='id', right_on=col_region)
              .drop(columns=['id', col_region]))

        df['date_reg'] = df['date'].astype(str).str[:5] + df['code_dep'].astype(str)

        return df

    def get_agg_dict(self, threshold=1, higher_thresh=None, lower_thresh=None):
        """Returns an aggregation dictionary"""
        if higher_thresh==None:
            higher_thresh=threshold
        if lower_thresh==None:
            lower_thresh=threshold

        agg_dict = pd.Series(self.clean_key['agg'].values,
                     index=self.clean_key['name_clean']).to_dict()
        del agg_dict['date']
        del agg_dict['id']
        agg_dict['tmax_c'] = (lambda x :
            count_outliers(x, threshold=threshold, greater=True))
        agg_dict['tmin_c'] = (lambda x :
            count_outliers(x, threshold=threshold, greater=False))

        return agg_dict

    def downshift(self, df_agg:pd.DataFrame(), cols_to_shift, shift=None):
        if shift==None:
            shift = self.region_key['Departement'].nunique()

        idx = pd.IndexSlice

        df_agg.loc[:, idx[:,cols_to_shift]] = (df_agg.loc[:, idx[:,cols_to_shift]]
                                               .shift(shift))

        return df_agg

    def agg_month(self, df:pd.DataFrame(), agg_dict=None):
        """
        Aggregate and unstack a df such that there is:
        - One row per year per region
        - One column per feature per month
        """
        if agg_dict==None:
            agg_dict = self.get_agg_dict()

        df['date_reg'] = df['date'].astype(str).str[:5] + df['code_dep'].astype(str)
        df['month'] = df['date'].astype(str).str[5:7]

        df_agg = df.groupby(['date_reg', 'month']).agg(agg_dict)

        df_agg = df_agg.unstack(level=1)

        return df_agg

    def agg_week(self, df:pd.DataFrame(), agg_dict=None):
        """
        Aggregate and unstack a df such that there is:
        - One row per year per region
        - One column per feature per week of year
        """
        if agg_dict==None:
            agg_dict = self.get_agg_dict()

        df['date'] = pd.to_datetime(df['date'])
        df['week_of_year'] = df['date'].apply(lambda x:
            int(pd.Timestamp.isocalendar(x)[1]))

        df_agg = df.groupby(['date_reg', 'week_of_year']).agg(agg_dict)
        df_agg = df_agg.unstack(level=1)

        return df_agg

    def agg_sp(self, df:pd.DataFrame(), agg_dict=None):
        """
        Aggregate and unstack a df such that there is:
        - One row per year per region
        - One column per feature for jan-march, one column per feature for sept-jan
        """
        if agg_dict==None:
            agg_dict = self.get_agg_dict()
        agg_dict['date'] = 'first'

        df = df.reset_index()
        df['period'] = 0
        df["month"] = df['date'].astype(str).str[5:7].astype(int)
        df.loc[df['month'] < 3, 'period'] = 'jan-mar'
        df.loc[df['month'] >= 9, 'period'] = 'sept_jan'
        df = df.drop(columns='month')
        df = df[df['period']!=0]

        df_agg = df.groupby(['period', 'date_reg']).agg(agg_dict)
        df_agg = df_agg.unstack(level=0)

        df_agg = self.downshift(df_agg, 'sept_jan')

        return df_agg


    def agg_unstack(self, df:pd.DataFrame(), agg_type="M", agg_dict=None):
        """
        Wrapper function for the agg_X functionns
        Returns an aggregated and unstacked df, such that:
        For agg_type = "M", there is:
            - One row per year per region
            - One column per feature per month
        For agg_type = "W", there is:
            - One row per year per region
            - One column per feature per week of year
        For agg_type = "S", there is:
            - One row per year per region
            - One column per feature for jan-march, one column per feature for sept-jan
        -------------
        Params:
        df: dataframe, dataframe to aggregate
        agg_type: string, method to use to aggregate
            -"M": aggregates at a monthly level
            -"W": aggregates at a weekly level, indexed on Mondays
            -"S": aggregates into 2 periods, Jan-March and Sept-Jan
        agg_dict: dictionary, dict containing the agg functions
        """
        if (agg_type=="M"):
            df_agg = self.agg_month(df, agg_dict=agg_dict)

        if (agg_type=="W"):
            df_agg = self.agg_week(df, agg_dict=agg_dict)

        if (agg_type=="S"):
            df_agg = self.agg_sp(df, agg_dict=agg_dict)

        return df_agg


def agg_meteo(meteo_data='../raw_data/Meteo/historique_meteo_daily.csv',
              cleaning_key='../raw_data/Meteo/scraped_meteo_name_key.xlsx',
              region_key='../raw_data/Meteo/Classement_Departement.xlsx',
              agg_type="M", temp_outlier_threshold=1):
    """Script-callable function
    Outputs a clean aggregated DataFrame, with a DATE-REGION index of form
    "YYYY-XX"
    ----------------
    PARAMS:
    meteo_data: local path to 'historique_meteo_daily.csv' on the drive (in
        DeepAgri -> Meteo -> historique_meteo)

    cleaning_key: local path to 'scraped_meteo_name_key.xlsx' on the drive (in
        DeepAgri -> Meteo -> historique_meteo)

    region_key: local path to 'Classement_Departement.xlsx' on the drive (in
        DeepAgri -> Meteo -> historique_meteo)

    agg_type: Aggregation type. Valid options are:
        - "W": weekly aggregation
        - "M": monthly aggregation
        - "S": special aggregation - split into jan-march and sept-jan periods

    temp_outlier_threshold: aggregation key for the max and min temperature
        columns, which count the number of days past the threshold. Defined in
        standard deviations, i.e. a temp_outlier_threshold=1 means we will count
        all days where we are more than one standard deviation outside the mean.
    """
    magg = MeteoAggregator(meteo_data, cleaning_key, region_key)

    df = magg.clean_names()
    df = magg.add_dept(df)

    agg_dict = magg.get_agg_dict(threshold=temp_outlier_threshold)

    df_agg = magg.agg_unstack(df, agg_type='S', agg_dict=agg_dict)

    return df_agg