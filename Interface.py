# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:31:29 2022

@author: Rivar
"""
import pandas as pd
import streamlit as st
import numpy as np
st.set_page_config(page_title="Phantom Chief", page_icon="ghost")


st.title("Phantom Chief")
df = pd.read_csv("http://chendeb.free.fr/iris.data", names=["sl", "sw", "pl", "pw", "label"])
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
    st.write(df)
    elem = np.arange(len(df))
    number = st.select_slider(
    'Select the number of the recipe',
    options=elem)
    b = int(number)
    c = df.iloc[b]["label"]
    st.write(type(c))
    st.write(c)
    d = df.iloc[b]
    st.write(d.to_string())
    
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
    labelchoose = st.selectbox("Type", set(df["label"]))
    st.write(df.loc[df["label"] == labelchoose])
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


