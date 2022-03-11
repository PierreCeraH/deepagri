import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def show_table(df_final):

    liste_noms_dept = ['00 - FRANCE','01 - Ain','02 - Aisne','03 - Allier','04 - Alpes-de-Haute-Provence',
                '05 - Hautes-Alpes','06 - Alpes-Maritimes','07 - Ardèche','08 - Ardennes',
                '09 - Ariège','10 - Aube','11 - Aude','12 - Aveyron',
                '13 - Bouches-du-Rhône','14 - Calvados','15 - Cantal','16 - Charente',
                '17 - Charente-Maritime','18 - Cher','19 - Corrèze',
                "21 - Côte-d'Or","22 - Côtes-d'Armor","23 - Creuse","24 - Dordogne",
                "25 - Doubs","26 - Drôme","27 - Eure","28 - Eure-et-Loir",
                "29 - Finistère","30 - Gard","31 - Haute-Garonne","32 - Gers",
                "33 - Gironde","34 - Hérault","35 - Ille-et-Vilaine","36 - Indre",
                "37 - Indre-et-Loire","38 - Isère","39 - Jura","40 - Landes",
                "41 - Loir-et-Cher","42 - Loire","43 - Haute-Loire","44 - Loire-Atlantique",
                "45 - Loiret","46 - Lot","47 - Lot-et-Garonne","48 - Lozère",
                "49 - Maine-et-Loire","50 - Manche","51 - Marne","52 - Haute-Marne",
                "53 - Mayenne","54 - Meurthe-et-Moselle","55 - Meuse","56 - Morbihan",
                "57 - Moselle","58 - Nièvre","59 - Nord","60 - Oise",
                "61 - Orne","62 - Pas-de-Calais","63 - Puy-de-Dôme","64 - Pyrénées-Atlantiques",
                "65 - Hautes-Pyrénées","66 - Pyrénées-Orientales","67 - Bas-Rhin","68 - Haut-Rhin",
                "69 - Rhône","70 - Haute-Saône","71 - Saône-et-Loire","72 - Sarthe",
                "73 - Savoie","74 - Haute-Savoie","76 - Seine-Maritime","77 - Seine-et-Marne",
                "79 - Deux-Sèvres","80 - Somme","81 - Tarn","82 - Tarn-et-Garonne",
                "83 - Var","84 - Vaucluse","85 - Vendée","86 - Vienne",
                "87 - Haute-Vienne","88 - Vosges","89 - Yonne","90 - Territoire de Belfort",
                "91 - Essonne","93 - Seine-Saint-Denis","94 - Val-de-Marne","95 - Val-d'Oise"]

    option = st.selectbox('Select a department', liste_noms_dept)
    opt_num = option[:2]

# ------------------------------------------------------------------------------
# PLOTTING THE EVOLUTION OF A CHOSEN DEPARTMENT PRODUCTION
# ------------------------------------------------------------------------------

    fig = plt.figure(figsize=(10, 4))
    plt.title(f'{option[3:]}')
    clrs = ['#ffb482' if (x == 2022) else '#4c72b0' for x in df_final.columns]
    values = np.array(df_final.loc[opt_num])
    idx = np.array(df_final.columns)

    sns.barplot(x=idx, y=values / 10**6, palette=clrs)
    plt.xticks(rotation=45)
    plt.ylabel('Millions')

    st.pyplot(fig)

    st.markdown("<h6 style='text-align: center; color: #708090;'>DeepAgri Project - Le Wagon - Data Science - Batch #802</h6>", unsafe_allow_html=True)
    columns_names = st.columns(4)
    col_name_0 = columns_names[0].markdown("<h7 style='text-align: center; color: #708090;'>Pierre Cera-Huelva</h7>", unsafe_allow_html=True)
    col_name_1 = columns_names[1].markdown("<h7 style='text-align: center; color: #708090;'>Gaspar Dupas</h7>", unsafe_allow_html=True)
    col_name_2 = columns_names[2].markdown("<h7 style='text-align: center; color: #708090;'>Constantin Talandier</h7>", unsafe_allow_html=True)
    col_name_3 = columns_names[3].markdown("<h7 style='text-align: center; color: #708090;'>Wenfang Zhou</h7>", unsafe_allow_html=True)

    taloche_pic = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/taloche_pic.jpeg'
    wenfang_pic = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/wenfang_pic.jpeg'
    gaspar_pic = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/gaspar_pic.jpeg'
    pierre_pic = 'https://raw.githubusercontent.com/PierreCeraH/deepagri/master/pierre_pic.jpeg'

    #pictures = st.columns(4)
    #pic_0 = pictures[0].image(pierre_pic, channels="RGB", output_format="auto")
    #pic_1 = pictures[1].image(gaspar_pic, channels="RGB", output_format="auto")
    #pic_2 = pictures[2].image(taloche_pic, channels="RGB", output_format="auto")
    #pic_3 = pictures[3].image(wenfang_pic, channels="RGB", output_format="auto")
