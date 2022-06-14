# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:31:29 2022

@author: Rivar
"""
import pandas as pd
import streamlit as st
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
    a = st.button("Gaspi")
    st.write(choice)
    if a:
        choice = "Gaspi"
        st.write(choice)
        
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
    st.write('My favorite color is', df.head(int(number)))
elif choice == "Gaspi":
    st.write("""
    #My Gaspi \n
    Hello *world!*
    """)
else:
    st.write("""
    #My Error \n
    Hello *world!*
    """)


