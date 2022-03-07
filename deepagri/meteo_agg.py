# Package to aggregate meteo data
# -------------------------------------------------------
# Expected inputs:
# ../raw_data/Meteo/historique_meteo_daily.csv
# ../raw_data/Meteo/scraped_meteo_name_key.xlsx

import pandas as pd
import numpy as np
import os

PATH=os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'raw_data'),'Meteo')

REGION_KEY_OFFSET = 41

def count_outliers(series, threshold=1, greater=True, relative_thresh=True):
    """
    Aggregator function to count occurences greater / smaller than n standard
    deviations.
    ----------
    Parameters:
    threshold: Float, default 1.
            Number of standard deviations to set as a threshold.
    greater: Boolean, default True.
            If True, will count occurences greater than the given threshold.
            If False, will count occurences smaller than the given threshold.
    relative_thresh: Boolean, default True.
            If True, will take the threshold as a number of standard deviations,
            and count the number of days above / below (mean + threshold * s.d)
            If False, will take the threshold as the absolute value of a
            temperature to beat, in °C
    """
    if relative_thresh: # threshold as a standard dev
        limit = series.mean() + threshold * series.std()
    else:
        limit = threshold

    if greater:
        return (series >= limit).sum()
    elif not greater:
        return (series <= limit).sum()


class MeteoAggregator():

    def __init__(self,
                meteo_data=os.path.join(PATH,'historique_meteo_daily.csv'),
                cleaning_key=os.path.join(PATH,'scraped_meteo_name_key.xlsx'),
                region_key=os.path.join(PATH,'Classement_Departement.xlsx')):
        self.df = pd.read_csv(meteo_data)
        self.clean_key = pd.read_excel(cleaning_key)
        self.clean_key = self.clean_key[self.clean_key['keep']==1.0]

        self.region_key = pd.read_excel(region_key)
        self.region_key = (self.region_key[REGION_KEY_OFFSET:]
                           .dropna(subset=['id_hist_meteo']))
        self.region_key[['Departement','id_hist_meteo']] = (
            self.region_key[['Departement','id_hist_meteo']].astype(int))


    def get_clean_data(self, df=pd.DataFrame(), col_clean='name_clean',
                       col_raw='name_raw'):
        """
        Gets the data, cleans column names and adds the tmax_deg and tmin_deg
        columns
        """
        if df.empty:
            df = self.df
        df = df.rename(pd.Series(self.clean_key[col_clean].values,
                                 index=self.clean_key[col_raw]).to_dict(),
                       axis=1)
        df = df[self.clean_key[col_clean]]

        df['tmax_deg'] = df['tmax_c']
        df['tmin_deg'] = df['tmin_c']

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

        df['date_dep'] = df['date'].astype(str).str[:5] + df['code_dep'].astype(str)

        return df

    def get_agg_dict(self, threshold=1, higher_thresh=None, lower_thresh=None,
                     relative_thresh=True):
        """Returns an aggregation dictionary to be used by agg_unstack()
        See count_outliers() for parameters
        """
        if higher_thresh==None:
            higher_thresh=threshold
        if lower_thresh==None:
            lower_thresh=threshold

        agg_dict = pd.Series(self.clean_key['agg'].values,
                     index=self.clean_key['name_clean']).to_dict()
        del agg_dict['date']
        del agg_dict['id']
        agg_dict['tmax_c'] = (lambda x :
            count_outliers(x, threshold=threshold, greater=True,
                           relative_thresh=relative_thresh))
        agg_dict['tmin_c'] = (lambda x :
            count_outliers(x, threshold=threshold, greater=False,
                           relative_thresh=relative_thresh))
        agg_dict['tmax_deg'] = "max"
        agg_dict['tmin_deg'] = "min"

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

        df['date_dep'] = df['date'].astype(str).str[:5] + df['code_dep'].astype(str)
        df['month'] = df['date'].astype(str).str[5:7]

        # Editing month names to reflect months >= 3 being from n-1
        df.loc[~df['month'].isin(['01','02','03','04','05']), 'month'] = (
            df.loc[~df['month'].isin(['01','02','03','04','05']), 'month']
            + "_n-1")

        df_agg = df.groupby(['date_dep', 'month']).agg(agg_dict)
        df_agg = df_agg.unstack(level=1)

        df_agg = self.downshift(df_agg, ['06_n-1', '07_n-1', '08_n-1',
                                         '09_n-1', '10_n-1', '11_n-1', '12_n-1'])

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
        df['year_of_week_start'] = df['date'].apply(lambda x:
            str(pd.Timestamp.isocalendar(x)[0]))
        df['week_of_year'] = df['date'].apply(lambda x:
            str(pd.Timestamp.isocalendar(x)[1]).zfill(2))

        df.drop(columns=['date_dep', 'date'])
        df['date_dep'] = df['year_of_week_start'] + "-" + df['code_dep']

        # Drop 22nd week because it's usually halfway on may-june
        # which causes issues, and it's far back enough in n-1 that it's
        # mostly irrelevant
        # Also drop week 35 for same reasons except on Aug-Sept
        df = df[df['week_of_year']!='22']
        df = df[df['week_of_year']!='35']
        df = df[df['week_of_year']!='53'] # Rare occurence so dropped
        df.loc[~df['week_of_year'].isin(
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
             '11','12','13','14','15','16','17','18','19','20','21']),
               'week_of_year'] = (df.loc[~df['week_of_year'].isin(
                   ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11','12','13','14','15','16','17','18','19','20','21']),
                                         'week_of_year'] + "_n-1")

        df_agg = df.groupby(['date_dep', 'week_of_year']).agg(agg_dict)
        df_agg = df_agg.unstack(level=1)

        df_agg = self.downshift(df_agg, ['23_n-1',
            '24_n-1', '25_n-1', '26_n-1', '27_n-1', '28_n-1', '29_n-1',
            '30_n-1', '31_n-1', '32_n-1', '33_n-1', '34_n-1', '35_n-1',
            '36_n-1', '37_n-1', '38_n-1', '39_n-1', '40_n-1', '41_n-1',
            '42_n-1', '43_n-1', '44_n-1', '45_n-1', '46_n-1', '47_n-1',
            '48_n-1', '49_n-1', '50_n-1', '51_n-1', '52_n-1'])

        return df_agg

    def agg_sp(self, df:pd.DataFrame(), agg_dict=None):
        """
        Aggregate and unstack a df such that there is:
        - One row per year per region
        - One column per feature for jan-march, one column per feature for sept-jan
        """
        if agg_dict==None:
            agg_dict = self.get_agg_dict()

        df = df.reset_index()
        df['period'] = 0
        df["month"] = df['date'].astype(str).str[5:7].astype(int)
        df.loc[df['month'] < 6, 'period'] = 'jan-may'
        df.loc[df['month'] >= 9, 'period'] = 'sept-dec_n-1'
        df = df.drop(columns=['month', 'index', 'date'])
        df = df[df['period']!=0]

        df_agg = df.groupby(['period', 'date_dep']).agg(agg_dict)
        df_agg = df_agg.unstack(level=0)

        df_agg = self.downshift(df_agg, 'sept-dec_n-1')

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
        if (agg_type=="S"):
            df_agg = self.agg_sp(df, agg_dict=agg_dict)
            return df_agg

        df['period'] = 0
        df["month"] = df['date'].astype(str).str[5:7].astype(int)
        df.loc[df['month'] < 6, 'period'] = 'jan-mar'
        df.loc[df['month'] >= 9, 'period'] = 'sept-jan_n-1'
        df = df[df['period']!=0]
        df = df.drop(columns=['month', 'period'])

        if (agg_type=="M"):
            df_agg = self.agg_month(df, agg_dict=agg_dict)

        if (agg_type=="W"):
            df_agg = self.agg_week(df, agg_dict=agg_dict)

        return df_agg


def agg_meteo(meteo_data=os.path.join(PATH,'historique_meteo_daily.csv'),
              cleaning_key=os.path.join(PATH,'scraped_meteo_name_key.xlsx'),
              region_key=os.path.join(PATH,'Classement_Departement.xlsx'),
              agg_type='M',**kwargs):
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

    **kwargs: count_outliers() arguments
    """
    magg = MeteoAggregator(meteo_data, cleaning_key, region_key)

    df = magg.get_clean_data()
    df = magg.add_dept(df)

    agg_dict = magg.get_agg_dict(**kwargs)

    df_agg = magg.agg_unstack(df, agg_type=agg_type, agg_dict=agg_dict)

    return df_agg

if __name__=='__main__':
    print(agg_meteo(agg_type='S'))
