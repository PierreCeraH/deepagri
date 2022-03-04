import requests
import pandas as pd
import os
from tqdm import tqdm

FILEPATH=os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data/Meteo/')
CLASSEMENT_OFFSET = 41

PARAM_KEY_EXAMPLE = """param_key=
('__cf_chl_tk', 'F6pnR2S6FlBuLYz3PC.u9_AGa0Em0CYME0RXHYQ8le8-1646295246-0-gaNycGzNDNE')"""
HEADER_EXAMPLE = (
    """header = {
    'authority': 'www.historique-meteo.net',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.historique-meteo.net/france/corse/ajaccio/2022/02/',
    'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
    'cookie': 'euconsent-v2=CPVMwMAPVMwMABcAIBENCECgAP_AAH_AAAqIIDkZ_C9MQWNjUX58A_s0aYxHxgAGoWQADACJgygBCAPA8IQEwGAYIAVAAogKAAAAoiZBAAAhCAlAAAEAQAAAACCMAEAAAAAAICIAgAARAgEACAhBEQAAEAIAAABBABAAgAAEQhoAQAAAAAAgAAAAAAAgAACBAAAAAAAAAAAAAAAAAAggOACYKkxAA2JQYEgQaRQogBBGAAQAIAAIAIGCKAAIAADghABwQAgAAAAAiAgAAACiBgEAAAEACEAAAABAAEAAAAgAAAAAAAAAIgAAAAEAAAAACAABAAAAAAAAAEEAAACAAAAAEABAAAAAACAAAAAAAAAAAMAAAAAAAAAAAAAAAAAAAAAA.x6pux3I.4UGADABZAIgAVIBJYEsQUGAAQACAAgACAAQAEA; __cf_bm=.vXWIt.jblfaNmL9gMYHae0N_.2EQpcgzgVTZqrzTx0-1646295172-0-AdTkucwT68/2AduFiYYON/Fcba91rkpxeQ4eXZgNSyMPVDxoBOTDOAA8F1vJxSxE2NHMe2YbMeoZnEeTaMuIrMkriuKFzqefcNyWgEZqgtmm2NSkV7nP3ho7bQu4Qhx1Ag==; cf_chl_2=e44bce0bffd9b73; cf_chl_prog=x11; cf_clearance=9YYMobtexq9fVVJIBSH8wL1CWzRpJkKNXj1mmHLP5Ik-1646295247-0-150',
}"""
)

def get_scrape_list(file=None):
    """Returns the list of ids to scrape from Classement_Departement.xlsx"""
    if file==None:
        file = os.path.join(FILEPATH, 'Classement_Departement.xlsx')

    df = pd.read_excel(file)
    df = df[['Departement','id_hist_meteo']]
    df = df[CLASSEMENT_OFFSET:]
    df = df.dropna()
    df = df[df.columns].astype(int)

    return list(df['id_hist_meteo'].values)

def scrape_historique_meteo(headers=None, param_key=None, scrape_list=[]):
    if (headers==None) | (param_key==None):
        print("Make sure to pass a header and a param_key as arguments!")
        print("They should be in the following formats:")
        print("Header:\n" + HEADER_EXAMPLE)
        print("\nparam_key:\n" + PARAM_KEY_EXAMPLE)

        return

    if not scrape_list:
        scrape_list = get_scrape_list()

    df = pd.DataFrame()
    counter=0
    for id_ in tqdm(scrape_list):
        params = (
            ('ville_id', id_),
            param_key,
        )

        response=requests.get('https://www.historique-meteo.net/site/export.php',
                              headers=headers, params=params)

        # print((id_, response.status_code))
        if response.status_code==403:
            print("403 Error!")
            print("Go to your browser, press F12, navigate to the 'Network' tab")
            print("Then go to https://www.historique-meteo.net/site/export.php?ville_id=1012")
            print("Refresh the page to rerun the request until 'export.php...' "
                  + "turns blue, then RClick copy as cURL (bash), pass it to "
                  + "curlconverter, and extract the header and param_key from "
                  + "there.")
            print("Try again with the new parameters!")
            return
        tmp = pd.DataFrame([l.split(",") for l in response.text.split("\n")][3:])
        tmp.columns = tmp.iloc[0]
        tmp = tmp.iloc[1:]
        tmp['id'] = id_
        df = df.append(tmp)
        counter+=1

    print(f"Succesfully scraped {counter} files")
    return df

def clean_df(df, meteo_key=None):
    if meteo_key==None:
        meteo_key = pd.read_excel(os.path.join(FILEPATH,
                                               'scraped_meteo_name_key.xlsx'))
    meteo_key = meteo_key[meteo_key['keep']==1.0]
    name_dict = pd.Series(meteo_key['name_clean'].values, index=meteo_key['name_raw']).to_dict()

    df = df[meteo_key.name_raw]
    df = df.rename(columns=name_dict)
    df = df.reset_index(drop=True)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index("date")

    return df


def meteo_scrape(scraper_headers=None, scraper_param_key=None,
                 classement_departement=None, meteo_key=None,):
    scrape_list = get_scrape_list(classement_departement)

    df = scrape_historique_meteo(scraper_headers, scraper_param_key, scrape_list)

    df = clean_df(df, meteo_key=meteo_key)

    df.to_csv(os.path.join(FILEPATH, 'historique_meteo_daily.csv'))
