# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:31:29 2022

@author: Rivar
"""
import pandas as pd
import streamlit as st
import numpy as np
import jaro
from colour import Color

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title="Phantom Chief",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="ghost",  # String, anything supported by st.image, or None.
)



def color_all(df):
    df['color'] = 0
    green = Color("green")
    colors = list(green.range_to(Color("red"), (len(df) + 1)))
    i = 0
    for df_val in df.sort_values(by = 'Prediction eco').index:
        df['color'][df_val] = colors[i].hex
        i += 1
    return df

def proposerecipe(df):
    for df_val in df.index:
        color = (df['color'][df_val])[1:]
        while len(color) != 6:
            color = '0' + color
        color = '#' + color
        st.write(f"""<h2 style="text-align:center;color:{color}">
                 {df_val}
                 </h2>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"""
                     <h4 style="text-align:center;color:{color}">
                     {df['nbpersonne'][df_val]} personnes
                     </h4>""", unsafe_allow_html=True)
            st.write(f"""
                     <h4 style="text-align:center;color:{color}">
                     Bilan carbonne de la recette : {round(df["Prediction eco"][df_val]*100)} sur 100
                     </h4>
                     """,unsafe_allow_html=True)

        with col2:
            st.image(df['Url'][df_val])

        with col3:
            temps = "".join(df["TempEtape"][df_val]).split(",")
            for x in range (len(temps)):
                temps[x] = int(temps[x][:-3])
            tempstotal = str(df['tempstotal'][df_val]) + "min"
            st.write(f"""<h4 style="text-align:center;color:{color}">
                     Environ : {tempstotal}
                     </h4>
                     <h4 style="text-align:center;color:{color}">
                     {" ou ".join("".join(df['type'][df_val]).split(","))}
                     </h4>""", unsafe_allow_html=True)

        col2_1, col2_2 = st.columns(2)
        i = 0
        ingrlist = []
        etapelist = []
        with col2_1:
            ingr = st.checkbox("Ingredients pour " + df_val)
            ingrlist.append(ingr)
            if ingrlist[i]:
                ingre = np.array("".join(df["Ingredient"][df_val]).split(","), dtype=np.str)
                qt = np.array("".join(df["QtIngredient"][df_val]).split(","), dtype=np.str)
                info = np.char.add(qt, " ")
                info = np.char.add(info, ingre)
                st.write("""
                <h2 style="text-align:center;color:green">
                Ingredients
                </h2>
                """,unsafe_allow_html=True)
                for ing in info:
                    st.write(ing)
                st.write("- - - - - - - - - - - - -")

        with col2_2:
            etape = st.checkbox("Etape pour " + df_val)
            etapelist.append(etape)
            if etapelist[i]:
                st.write("""
                <h2 style="text-align:center;color:blue">
                ETAPE
                </h2>
                """,unsafe_allow_html=True)
                etapechoosing = "".join(df["Etape"][df_val]).split(";")
                for etape in etapechoosing:
                    st.write(etape)
                st.write("- - - - - - - - - - - - -")

        i+= 1

        st.write("""- - - - - - - - - - - - - - - - - - - -""")


def get_co2_Unité(ingredient,Aliment):
    ind_max=0
    score_max=jaro.jaro_metric(ingredient,Aliment.iloc[0,0])
    for i in range(len(Aliment['Ingredient'])):
        if jaro.jaro_metric(ingredient,Aliment.iloc[i,0])>=score_max :
            ind_max=i
            score_max=jaro.jaro_metric(ingredient,Aliment.iloc[i,0])
    return Aliment.iloc[ind_max,:]

def get_co2_Liste(Liste_ingredient,Aliment):
    retour=np.zeros((1,len(Aliment.columns)))
    for i in Liste_ingredient:
        a=np.array(get_co2_Unité(i, Aliment))
        retour=np.vstack((retour,a))
    retour=pd.DataFrame(retour,columns=(Aliment.columns)).drop(0,axis=0)
    return retour

def Algo_distance( Aliment, Re, Input_liste=[]):
    Recette = pd.DataFrame(Re)
    df_retour = get_co2_Liste(Input_liste,Aliment)
    L_retour=list(df_retour['Ingredient'])
    st.write(f"""Nous avons compris {" ".join(L_retour)}""")
    S_Recette=Recette['Ingredient']
    distance=[]
    print(L_retour)
    for i in range(len(S_Recette)):
        L2=S_Recette[i].split(',')
        L1=L_retour
        res = len(set(L1) & set(L2)) / float(len(set(L1) | set(L2))) * 100
        distance.append(res)
    Recette['distance']=distance
    return Recette

st.title("Phantom Chief")
df = pd.read_excel("Data/BD Phantom Chief final.xlsx",index_col=1)
df_aliment = pd.read_excel("Data/Aliment_v3.xlsx",index_col=('Index'), decimal=',')
menu = ["Accueil","Daily","Recommandation","Gaspi"]
choice = st.sidebar.selectbox("Menu", menu)
df['tempstotal'] = 0
for df_val in df.index:
    temps = "".join(df["TempEtape"][df_val]).split(",")
    for x in range (len(temps)):
        temps[x] = int(temps[x][:-3])
    df['tempstotal'][df_val] = sum(temps)



df = color_all(df)
if choice == "Accueil":
    st.write(f"""
    <h1 style="color:#AEC6CF;text-align:center">
        Welcome
    </h1>
    <h2 style="text-align:center">
    #Phantom Chief
    </h2>
    """,unsafe_allow_html=True)
    st.write("""
    <h2 style="text-align:center">
    V1.1
    </h2>
    """,unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(
            "Ressource/ghostEnAttendantValHein.png",
        )

    with col3:
        st.write(' ')

elif choice == "Daily":
    number = st.select_slider(
    'Select a number of recipe',
    options=[x for x in range(5,11)])
    df3 = df.sample(n = 11)
    proposerecipe(df3.head(number))

elif choice == "Recommandation":
    st.write("""
    My Recommendation \n
    """)
    tochoose_level = set(df["Difficulter"])
    tochoose_level.add("Toutes les recettes")
    labelchoose = st.selectbox("Type", tochoose_level, index = 1)
    if (labelchoose != "Toutes les recettes"):
        df2 = df.loc[df["Difficulter"] == labelchoose]
    else:
        df2 = df
    time = st.checkbox("Trié par temps")
    if time:
        df2 = df2.sort_values(by = 'tempstotal')
    sort_eco = st.checkbox("Trie par impact environnemental")
    if sort_eco:
        df2 = df2.sort_values(by = 'Prediction eco')
    if sort_eco and time:
        df2 = df2.sort_values(by = ['Prediction eco','tempstotal'])

    vege = st.checkbox("Affiché que les plats végétariens ?")
    if vege:
        proposerecipe(df2[df2['presenceViande'] == 0])
    else:
        proposerecipe(df2)

    #st.write(df2)


elif choice == "Gaspi":
    st.write("""
    #My Gaspi \n
    Essayons d'éviter le gaspillage
    """)
    inpute = st.text_area("Please insert your ingredients separate with enter ...")
    if (inpute != ""):
        ress = inpute.split("\n")
        l = []
        for words in ress:
            if words != "" and words != " ":
                word = words[0].upper() + words[1:]
                l.append(word)
        newdataframe = Algo_distance(df_aliment, df, l)
        proposerecipe(newdataframe.sort_values(by = 'distance', ascending = False).head(10))
    else:
        st.write("Waiting for your ingredients...")

else:
    st.write("""
    #My Error \n
    Hello *world!*
    """)






