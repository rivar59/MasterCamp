import numpy as np
import pandas as pd

data=pd.read_excel("BD Phantom Chief.xlsx",index_col=1)

aliment=data['Ingredient']

#liste de tout les aliment
retour=[]
for i in range(len(aliment)):
    a=aliment[i]
    retour.append(a.split(','))
#concataine les liste
all_aliment=[]
for i in retour:
    all_aliment+=i
    
#supprime les espace au debut
for i in all_aliment:
    if i[0]==' ':
        i=i[1:]
for i in aliment:
    i=i.lower()

a=set(all_aliment)
c=list(a)
b=sorted(c)
        
data_aliment=pd.DataFrame(b)
    

data_aliment.to_excel('Aliment.xlsx')

