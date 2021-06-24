#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 22:58:22 2021

@author: saadia
"""

""" Modélisation mécaniques des structures """

# imports biblio Python
import numpy as np
import matplotlib.pyplot as plt 


# Données d'entrées
u_ref=0.12015
s_ref=35.28

# Initialisation
e_loc=[]
e_glob=[]

# Fonction charge les données d'un fichier sous forme de liste 
# fichier -> liste
def ficList(nom_fichier):
    """ Retourne une liste à partir du nom de fichier """
    l = np.loadtxt(nom_fichier)
    return list(l)

def listMat(l1,l2):
        """ retourne une matrice à partir de deux listes """
        m=[l1,l2]
        return m

print("\nCalcul erreur de discrétisation locale EMu :\n")

# Chargement des données fichier résultats uh_max(M)
uh=ficList("resultats_uh_max.txt")

print("\nListe des déplacements axiaux uh en mm " \
      "\nau point M avec RDM6 : \n \nuh = ", uh)

# Affichage uh_maillage
print("\nLes résultats en déplacement uh(M) en mm "\
      "\nde la modélisation RDM6 des 7 maillages,\n "\
      "\nuh_numéro_maillage :")

for i in range(len(uh)):
    print("\nuh_{} = {}".format(i+1,round(uh[i],5)))

# Fonction erreur de discrétisation locale
def ErreurLoc(uh,u_ref):
    for u in uh:
        el=(np.abs(u-u_ref))/(np.abs(u_ref))
        e_loc.append(round(el,5))
    return e_loc

e_loc=ErreurLoc(uh,u_ref)

# Affichage erreurs locales
print("\nLes erreurs de discrétisation locales calculées " \
      "\nsont regroupées dan la liste ci-dessous : \n \nerreurs_locales =",e_loc)


print("\nTracé de la courbe erreur_locale en fonction" \
      "\nde la taille moyenne des éléments h : EMu(h)")

h=ficList("taille_moy_h.txt")
print("\nh = ",h)

eloc1=e_loc[0:3]
print("eloc1=",eloc1)
eloc2=e_loc[3:6]
print("eloc2=",eloc2)


# On trace les courbes et les points el(h) pour TRI3 et TRI6 

def Trace_eloc_h(eloc,h,c):
    plt.plot(h,eloc, marker = 'o',color=c)
    plt.xlabel ("h ")
    if eloc==eloc1 :
        plt.title("Erreur locale en fonction de la taille moyenne - Element triangle à 3 noeuds TRI3")
        plt.ylabel(" erreur locale 1 - TRI3")
        plt.savefig("Graphe1- Erreur locale (h) - TRI3")
    else :
        plt.title("Erreur locale en fonction de h - Element triangle à 6 noeuds TRI6")
        plt.xlabel ("taille moyenne h en mm ")
        plt.ylabel(" erreur locale 2 - TRI6")
        plt.savefig("Graphe2-Erreur locale (h)- TRI6")
    
    plt.show()
    
Trace_eloc_h(eloc1,h,"green")
Trace_eloc_h(eloc2,h,"orange")


# On trace les graphes el(h) pour TRI3 et TRI6 à partir de l'équation A*hexp(B)

# Calcul des constantes A et B 

el1=e_loc[0]
el2=e_loc[1]

h1=h[0]
h2=h[1]

# Fonction de calcul de la constante B    
def Calcul_B(el1,el2,h1,h2):
    B=(np.log10(el1/el2))/(np.log10(h1/h2))
    return B 

# Fonction de calcul de la constante A
def Calcul_A(el,h,B):
    A=el/pow(h,B)
    return A

# Affichages de A et B 

B=Calcul_B(el1,el2,h1,h2) 
print("\nB = ",round(B,3))

A=Calcul_A(el1,h1,B)
print("\nA = ",round(A,3))

X=[]
Y1=[]
Y2=[]

for i in range(len(h)) :
    x=np.log10(A)+((B+1)*np.log10(h[i]))
    X.append(x)

for i in range(len(eloc1)) :
    y1=np.log10(eloc1[i])
    Y1.append(y1)

for i in range(len(eloc2)) :
    y2=np.log10(eloc2[i])
    Y2.append(y2)


def courbe_Puissance(x,y,c):
    plt.plot(x,y, marker = 'o',color=c)
    plt.xlabel ("log h ")
    
    if y==Y1 :
        plt.title("Erreur locale en fonction de h - Element triangle à 3 noeuds TRI3")
        plt.ylabel(" log eloc1 ")
        plt.savefig("Courbe_Puissance_1-Erreur locale (h)- TRI3")
    else:
        plt.title("Erreur locale en fonction de h - Element triangle à 6 noeuds TRI6")
        plt.ylabel(" log eloc2 ")
        plt.savefig("Courbe_Puissance_2-Erreur locale (h)- TRI6")
    
    plt.show()

# Appel de fonction courbe_Puissance
courbe_Puissance(X,Y1,"b")
courbe_Puissance(X,Y2,"r")





    

#print("\nCalcul erreur de discrétisation globale ES_xx_max\n")

#sh=file_list("liste_sh_max.txt")
#print("\nListe des contraintes axiales max sh avec RDM6 :\n \nsh = ", sh)

## Fonction erreur de discrétisation globale
#def erreur_glob(sh,s_ref):
#    for s in sh:
#        eg=(np.abs(s-s_ref))/(np.abs(s_ref))
#        e_glob.append(round(eg,5))
#    return e_glob

#e_glob=erreur_glob(sh,s_ref)

#print("\nLes erreurs de discrétisation globales " \
#      "\nsont regroupées dan la liste ci-dessous : \n \nerreurs_globales =",e_glob)