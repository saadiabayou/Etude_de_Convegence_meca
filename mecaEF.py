# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 15:20:07 2021

@author: Saadia Bayou
"""

""" TP2  """

# imports bibliothèques Python
import numpy as np
import matplotlib.pyplot as plt 


# Données d'entrées
u_ref=0.12015
ur=[u_ref]*3
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

def Log10(v):
    "applique le log base 10 aux elments d'une liste"
    w=[]
    for i in v:
        if i==0 :
            print("pas de log10 pour :", i)
        else:
            n=np.log10(i)
            w.append(round(n,5))
    return w


print("\nCalcul erreur de discrétisation locale EMu :\n")

# Chargement des données fichier résultats uh_max(M)
uh=ficList("uh_max.txt")

print("\nListe des déplacements axiaux uh en mm " \
      "\nau point M avec RDM6 : \n \nuh = ", uh)

# Affichage uh_maillage
print("\nLes résultats en déplacement uh(M) en mm "\
      "\nde la modélisation RDM6 des 7 maillages,\n "\
      "\nuh_numéro_maillage :")

for i in range(len(uh)):
    print("\nuh_{} = {}".format(i+1,round(uh[i],5)))

# Fonction erreur de discrétisation locale
def erreurLoc(uh,u_ref):
    for u in uh:
        el=(np.abs(u-u_ref))/(np.abs(u_ref))
        e_loc.append(round(el,5))
    return e_loc

e_loc=erreurLoc(uh,u_ref)


# Affichage erreurs locales
print("\nLes erreurs de discrétisation locales calculées " \
      "\nsont regroupées dan la liste ci-dessous : \n \nerreurs_locales =",e_loc)


print("\nTracé de la courbe erreur_locale en fonction" \
      "\nde la taille moyenne des éléments h : EMu(h)")

t_moy=ficList("taille_moy_h.txt")
h=Log10(t_moy)
print("\nh = ",h)

uh1=uh[0:3]
print("\nuh1=",uh1)
uh2=uh[3:6]
print("\nuh2=",uh2)

def trace_uh_h(uh,h,c):
    plt.plot(h,ur,"r--",marker = 'o',label="solution de reference")
    plt.plot(h,uh, marker = 'o',color=c,label="solution numérique")
    plt.xlabel ("taille moyenne en mm ")
    
    if uh==uh1 :
        plt.title("déplacement locale en fonction de la taille moyenne - Element triangle à 3 noeuds TRI3")
        plt.ylabel(" uh_1 - TRI3")
        plt.savefig("Graphe- uhM(h) en mm - TRI3")
    else :
        plt.title("déplacement locale en fonction de la taille moyenne - Element triangle à 6 noeuds TRI6")
        plt.ylabel(" uh_2 - TRI6")
        plt.savefig("Graphe-uhM(h) en mm - TRI6")
    
    plt.legend()
    plt.show()
    
trace_uh_h(uh1,t_moy,"c")
trace_uh_h(uh2,t_moy,"b")


# On trace les courbes et les points el(h) pour TRI3 et TRI6 

elocal1=e_loc[0:3]
eloc1=Log10(elocal1)
print("\neloc1=",eloc1)

elocal2=e_loc[3:6]
eloc2=Log10(elocal2)
print("\neloc2=",eloc2)


def traceEloc_h(eloc,h,c,label):
    plt.plot(h,eloc, marker = 'o',color=c,label=label)
    plt.legend()
    plt.xlabel (" log taille moyenne : log10_h ")
    plt.title("Echelle logaritmique - Erreurs locales en fonction de la taille moyenne")
    plt.ylabel(" log erreurs locales : log10_e_u(M)")
    plt.savefig("Graphe- Erreur locale (h) - TRI3-et TRI6")
    
traceEloc_h(eloc1,h,"g","Erreur locale e_u - TRI3")
traceEloc_h(eloc2,h,"orange","Erreur locale e_u - TRI6")
plt.show() 
  


# Calcul de A et B et tracé des courbes des tendances

# Calcul des constantes A et B 



# Fonction de calcul de la constante B    
def Calcul_B(e1,e2,t1,t2):
    B=(np.log10(e1/e2))/(np.log10(t1/t2))
    return B 

# Fonction de calcul de la constante A
def Calcul_A(e,t,B):
    A=e/pow(t,B)
    return A

el1=e_loc[0]
el2=e_loc[1]

h1=h[0]
h2=h[1]

# Affichages de A1 et B1 

B1=Calcul_B(el1,el2,h1,h2) 
print("\nB1 = ",round(B1,3))

A1=Calcul_A(el1,h1,B1)
print("\nA1 = ",round(A1,3))

# Initialisations
X1=[]

for hi in h :
    x1=np.log10(A1)+((B1+1)*hi)
    X1.append(x1)

print("\nX1= ",X1)

def courbeTendance_uh(x,y,c):
    plt.plot(x,y, marker = 'o',color=c)    
    plt.xlabel ("log h ")    
    
    if y==eloc1 :
        plt.title("Courbe de tendance fonction de log h - Element triangle à 3 noeuds TRI3")
        plt.ylabel(" log eloc1 ")
        plt.savefig("Courbe_de_tendance_1-Erreur locale (h)- TRI3")
    else:
        plt.title("Courbe de tendance en fonction de log h - Element triangle à 6 noeuds TRI6")
        plt.ylabel(" log eloc2 ")
        plt.savefig("Courbe_de_tendance_2-Erreur locale (log h)- TRI6")
    
    plt.show()

# Appel de fonction courbe_de tendance
courbeTendance_uh(X1,eloc1,"b")
courbeTendance_uh(X1,eloc2,"r")



print("\nCalcul erreur de discrétisation globale ES_xx_max\n")

# Chargement des données fichier résultats uh_max(M)
sh_max=ficList("sh_max.txt")

print("\nListe des contraintes axiales sh " \
      "\n avec RDM6 : \n \nsh_max = ", sh_max)

# Affichage uh_maillage
print("\nLes résultats en contraintes axiales sh_max "\
      "\nde la modélisation RDM6 des 7 maillages,\n "\
      "\nsh_max_numéro_maillage :")

for i in range(len(sh_max)):
    print("\nsh_max_{} = {}".format(i+1,round(sh_max[i],5)))


# Fonction erreur de discrétisation locale
def erreurGlob(sh_max,s_ref):
    for s in sh_max:
        eg=(np.abs((s-s_ref)))/(np.abs(s_ref)) 
        e_glob.append(round(eg,5))
    return e_glob

e_glob=erreurGlob(sh_max,s_ref)

# Affichage erreurs globales
print("\nLes erreurs de discrétisation globales calculées " \
      "\nsont regroupées dan la liste ci-dessous : \n \nerreurs_globales =",e_glob)


print("\nTracé de la courbe erreur_globale en fonction" \
      "\nde la taille moyenne des éléments h : E_sxx(h)")


eglob1=e_glob[0:3]
print("\neglob1=",eglob1)
eglob2=e_glob[3:6]
print("\neglob2=",eglob2)


# On trace les courbes et les points el(h) pour TRI3 et TRI6 
def traceEglob_h(eglob,h,c,label):
    plt.plot(h,eglob, marker = 'o',color=c,label=label)
    plt.legend()
    plt.xlabel ("taille moyenne h ")
    plt.title("Erreurs globales en fonction de la taille moyenne")
    plt.ylabel(" erreurs globales e_sigma")
    plt.savefig("Graphe- Erreur globale (h) - TRI3 et TRI6")
    
traceEglob_h(eloc1,h,"b","Erreur globale e_sigma - TRI3")
traceEglob_h(eloc2,h,"c","Erreur globale e_sigma - TRI6")
plt.show() 


def compareErr(h,y,z,c1,c2,lab1,lab2):
    plt.subplot(211)
    plt.xlabel(" taille moyenne h ")
    plt.ylabel(" erreurs de discrétisations ")
    plt.plot(y,h,marker="o",label=lab1,color=c1)
    plt.plot(z,h,marker="o",label=lab2,color=c2)
    
    if y==eloc1 and z==eglob1:
        
        
        plt.title("Erreur globale et locale en fonction de h - TRI3")
        plt.savefig("Erreurs-locale-et-globale (h)- TRI3")
    else:
        
        plt.title("Erreur globale et locale en fonction de h - TRI6")
        plt.savefig("Erreurs-locale-et-globale (h)- TRI6")
    plt.legend()
    plt.show()


compareErr(h,eloc1,eglob1,"r","b",lab1="erreur locale TRI3",lab2="erreur globale TRI3")   
compareErr(h,eloc2,eglob2,"orange","c",lab1="erreur locale TRI6",lab2="erreur globale  TRI6")












#plt.subplot(loc1,glob1)
# Courbes de puissance :

# Initialisations
X2=[]
Z1=[]
Z2=[]

for i in range(len(h)) :
    x2=np.log10(A)+(B*np.log10(h[i]))
    X2.append(x2)

for i in range(len(eglob1)) :
    z1=np.log10(eglob1[i])
    Z1.append(z1)

for i in range(len(eglob2)) :
    z2=np.log10(eglob2[i])
    Z2.append(z2)


def courbe_Puissance_sh(x,z,c):
    plt.plot(x,z, marker = 'o',color=c)
    plt.xlabel ("log h ")
    
    if z==Z1 :
        plt.title("Erreur globale en fonction de h - Element triangle à 3 noeuds TRI3")
        plt.ylabel(" log eglob1 ")
        plt.savefig("Courbe_Puissance_1-Erreur globale (h)- TRI3")
    else:
        plt.title("Erreur globale en fonction de h - Element triangle à 6 noeuds TRI6")
        plt.ylabel(" log eglob2 ")
        plt.savefig("Courbe_Puissance_2-Erreur globale (h)- TRI6")
    
    plt.show()

# Appel de fonction courbe_Puissance
courbe_Puissance_sh(X2,Z1,"g")
courbe_Puissance_sh(X2,Z2,"b")







