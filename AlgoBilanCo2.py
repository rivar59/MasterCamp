import pandas as pd
import numpy as np
import jaro


Aliment=pd.read_excel("Aliment.xlsx",index_col=('Index'))
Recette=pd.read_excel("BD Phantom Chief.xlsx")

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
    