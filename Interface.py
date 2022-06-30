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




st.title("Phantom Chief")
df = pd.read_excel("Data/BD Phantom Chief.xlsx",index_col=1)
df_aliment = pd.read_excel("Data/Aliment.xlsx",index_col=('Index'))
df_filtre = df[['type','Difficulter','nbpersonne']]
menu = ["Accueil","Daily","Recommendation","Gaspi"]
choice = st.sidebar.selectbox("Menu", menu)
df['tempstotal'] = 0
for df_val in df.index:
    temps = "".join(df["TempEtape"][df_val]).split(",")
    for x in range (len(temps)):
        temps[x] = int(temps[x][:-3])
    df['tempstotal'][df_val] = sum(temps)

def proposerecipe(df):
    df['color'] = 0
    green = Color("green")
    colors = list(green.range_to(Color("red"), (len(df) + 1)))
    i = 0
    for df_val in df.index:
        df['color'][df_val] = colors[i].hex
        i += 1
    for df_val in df.index:
        color = (df['color'][df_val])[1:]
        while len(color) != 6:
            color = '0' + color
        color = '#' + color
        st.write(f"""<h3 style="text-align:center;color:{color}">
                 {df_val}
                 </h3>
                 <h4 style="text-align:center;color:light">
                 {df['nbpersonne'][df_val]} personnes
                 </h4>""", unsafe_allow_html=True)
        temps = "".join(df["TempEtape"][df_val]).split(",")
        for x in range (len(temps)):
            temps[x] = int(temps[x][:-3])
        tempstotal = str(df['tempstotal'][df_val]) + "min"
        st.write(f"""<h3 style="text-align:center">
                 Environ : {tempstotal}
                 </h3>
                 <h4 style="text-align:center;color:light">
                 {" ou ".join("".join(df['type'][df_val]).split(","))}
                 </h4>""", unsafe_allow_html=True)
        i = 0
        ingrlist = []
        etapelist = []
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
            st.write("""
                <h2 style="text-align:center;color:red">
                Enjoy !! :D
                </h2>
                """,unsafe_allow_html=True)

        i+= 1
        st.write("- - - - - - - - - - - - - - - - - - - -")



def get_co2_Unité(ingredient,Aliment):
    ind_max=0
    score_max=jaro.jaro_metric(ingredient,Aliment.iloc[0,0])
    for i in range(len(Aliment['Ingredient'])):
        if jaro.jaro_metric(ingredient,Aliment.iloc[i,0])>=score_max :
            ind_max=i
            score_max=jaro.jaro_metric(ingredient,Aliment.iloc[i,0])
    return Aliment.iloc[ind_max,:]

def get_co2_Liste(Liste_ingredient,Aliment):
    retour=np.zeros((1,3))
    print(retour)
    for i in Liste_ingredient:
        a=np.array(get_co2_Unité(i, Aliment))
        retour=np.vstack((retour,a))
    retour=pd.DataFrame(retour,columns=(Aliment.columns)).drop(0,axis=0)
    return retour

def Algo_distance( Aliment, Re, Input_liste=[]):
    Recette = pd.DataFrame(Re)
    df_retour = get_co2_Liste(Input_liste,Aliment)
    L_retour=list(df_retour['Ingredient'])
    st.write(L_retour)
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



if choice == "Accueil":
    st.write(f"""
    <h1 style="color:#AEC6CF;text-align:center">
        Main page
    </h1>
    <h2 style="text-align:center">
    #Phantom Chief
    </h2>
    """,unsafe_allow_html=True)
    st.write("""
    <h1 style="color:#AEC6CF;text-align:center">
        C'est notre page d'acceuil :D
    </h1>
    <h2 style="text-align:center">
    V1.1
    </h2>
    """,unsafe_allow_html=True)

elif choice == "Daily":
    st.write("""
    #My Daily \n
    Hello *world!*
    """)
    number = st.select_slider(
    'Select a number of recipe',
    options=[x for x in range(5,11)])
    df3 = df.head(int(number))
    proposerecipe(df3)

elif choice == "Recommendation":
    st.write("""
    #My Recommendation \n
    Hello *world!*
    """)
    labelchoose = st.selectbox("Type", set(df["Difficulter"]))
    df2 = df.loc[df["Difficulter"] == labelchoose]
    time = st.checkbox("Trié par temps")
    if time:
        df2 = df2.sort_values(by = 'tempstotal')
    vege = st.checkbox("Affiché que les plats végétariens ?")
    if vege:
        proposerecipe(df2[df2['presenceViande'] == 0])
    else:
        proposerecipe(df2)
    
    #st.write(df2)
    

elif choice == "Gaspi":
    st.write("""
    #My Gaspi \n
    Hello *world!*
    """)
    inpute = st.text_area("Please insert your ingredients separate with enter ...")
    if (inpute != ""):
        newdataframe = Algo_distance(df_aliment, df, inpute.split("\n"))
        proposerecipe(newdataframe.sort_values(by = 'distance', ascending = False).head(10))
    else:
        st.write("Waiting for your ingredients...")

else:
    st.write("""
    #My Error \n
    Hello *world!*
    """)






