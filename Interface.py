# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:31:29 2022

@author: Rivar
"""
import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title="Phantom Chief",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="ghost",  # String, anything supported by st.image, or None.
)

st.title("Phantom Chief")
df = pd.read_excel("Data/BD Phantom Chief.xlsx",index_col=1)
df_filtre = df[['type','Difficulter','nbpersonne']]
menu = ["Accueil","Daily","Recommendation","Gaspi"]
choice = st.sidebar.selectbox("Menu", menu)

l = ["Menu"]

def Gaspi(l):
    l = "Gaspi"

if choice == "Accueil":
    st.write("""
    <h1 style="color:#AEC6CF;text-align:center">
        Main page
    </h1>
    <h2 style="text-align:center">
    #Phatom Chief
    </h2>
    <p style="text-align:center">
    Hello world!
    </p>
    """,unsafe_allow_html=True)
    st.write(df_filtre)
    elem = np.arange(len(df))
    number = st.select_slider(
    'Select the number of the recipe',
    options=df.index)
    d = df[df.index == number]
    ingre = np.array(" ".join(df[df.index == number]["Ingredient"].values).split(","), dtype=np.str)
    qt = np.array(" ".join(df[df.index == number]["QtIngredient"].values).split(","), dtype=np.str)
    info = np.char.add(qt, " ")
    info = np.char.add(info, ingre)
    st.write("""
    <h2 style="text-align:center;color:green">
    Ingredients
    </h2>
    """,unsafe_allow_html=True)
    for ing in info:
        st.write(ing)
    st.write("""
    <h2 style="text-align:center;color:blue">
    ETAPE
    </h2>
    """,unsafe_allow_html=True)
    etapechoosing = "".join(df[df.index == number]["Etape"]).split(";")
    for etape in etapechoosing:
        st.write(etape)
    st.write("""
        <h2 style="text-align:center;color:red">
        Enjoy !! :D
        </h2>
        """,unsafe_allow_html=True)
elif choice == "Daily":
    st.write("""
    #My Daily \n
    Hello *world!*
    """)
    st.write(df.sample(frac=1))
elif choice == "Recommendation":
    st.write("""
    #My Recommendation \n
    Hello *world!*
    """)
    number = st.select_slider(
    'Select a number of recipe',
    options=["5", "10", "15", "20"])
    st.write('This is your element', df.head(int(number)))
    labelchoose = st.selectbox("Type", set(df["Difficulter"]))
    st.write(df.loc[df["Difficulter"] == labelchoose])
elif choice == "Gaspi":
    st.write("""
    #My Gaspi \n
    Hello *world!*
    """)
    inpute = st.text_area("Please insert your ingredients separate with enter ...")
    if (inpute != ""):
        st.write(inpute.split("\n"))
    else:
        st.write("Waiting for your ingredients...")
else:
    st.write("""
    #My Error \n
    Hello *world!*
    """)


