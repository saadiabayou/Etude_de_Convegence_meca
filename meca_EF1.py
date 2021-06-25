# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 19:24:37 2021

@author: Saadia Bayou
"""

""" Etude de convergence 
    Plaque percée en traction  """

# imports bibliothèques Python
import numpy as np
import matplotlib.pyplot as plt 


# Données d'entrées
u_ref=0.12015
ur=[u_ref]*3

s_ref=35.28
sr=[s_ref]*3

# Initialisation
e_u=[] # liste erreur de discrétisation locale - déplacement axiale u_xx(M)
e_s=[] # liste erreur de discrétisation globale - contrainte axiale s_xx 

# Fonctions

def ficList(nom_fichier):
    """ Retourne une liste à partir du nom de fichier 
    fichier -> liste """
    l = np.loadtxt(nom_fichier)
    return list(l)

def Log10(v):
    "applique le log base 10 aux elements d'une liste"
    w=[]
    for i in v:
        if i==0 :
            print("pas de log10 pour :", i)
        else:
            n=np.log10(i)
            w.append(round(n,5))
    return w

# Chargement des données fichier résultats taille_moyenne 
h=ficList("taille_moy_h.txt")
print("\nh = ",h)
# Passage en log10 
logh=Log10(h)
print("\nlogh = ",logh)

print("\nCalcul erreur de discrétisation locale e_u :\n")

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
        e_u.append(round(el,5))
    return e_u

e_u=erreurLoc(uh,u_ref)

# Affichage erreurs locales
print("\nLes erreurs de discrétisation locales calculées " \
      "\nsont regroupées dan la liste ci-dessous : \n \nerreurs_locales : \ne_u = ",e_u)


print("\nTracé de la courbe erreur_locale en fonction" \
      "\nde la taille moyenne des éléments h : e_u(h)")

# Découpage résulats uh_TRI3 et uh_TRI6
uh1=uh[0:3]
print("\nuh1=",uh1)

uh2=uh[3:6]
print("\nuh2=",uh2)

def trace_uh_h(uh,h,c):
    "Fonction trace uh en fonction de h pour TRI3 et TRI6"
    plt.plot(h,ur,"r--",marker = 'o',label="solution de reference")
    plt.plot(h,uh, marker = 'o',color=c,label="solution numérique")
    plt.xlabel ("taille moyenne en mm ")
    
    if uh==uh1 :
        plt.title("Déplacement locale uh(M) en fonction de la taille moyenne h , \nElement triangle à 3 noeuds TRI3")
        plt.ylabel(" uh_1 en mm - TRI3")
        plt.savefig("Graphe- uhM(h) - TRI3")
    else :
        plt.title("Déplacement locale uh(M) en fonction de la taille moyenne h \nElement triangle à 6 noeuds TRI6")
        plt.ylabel(" uh_2 en mm - TRI6")
        plt.savefig("Graphe-uhM(h) - TRI6")
    
    plt.legend()
    plt.show()
    
trace_uh_h(uh1,h,"b")
trace_uh_h(uh2,h,"c")


# Tracé en échelles logaritmique des erreurs locales e_u1 TRI3 et e_u2 TRI6:
print("\nTracé logaritmique des erreurs de discrétisations locales TRI3 et TRI6 : ")

e_u1=e_u[0:3]
log_e_u1=Log10(e_u1)
print("\nlog10 e_u1=",log_e_u1)

e_u2=e_u[3:6]
log_e_u2=Log10(e_u2)
print("\nlog10 e_u2=",log_e_u2)


def traceEloc_h(logh,log_eloc,c,label):
    plt.plot(logh,log_eloc, marker = 'o',color=c,label=label)
    plt.legend()
    plt.xlabel (" log10_h ")
    plt.title("Echelle logaritmique \n Erreurs locales TRI3 TRI6 en fonction de la taille moyenne")
    plt.ylabel(" log10_e_u(M)")
    plt.savefig("Graphe - Log erreurs locales (h) - TRI3-et TRI6")
    
traceEloc_h(logh,log_e_u1,"g","Erreur locale e_u - TRI3")
traceEloc_h(logh,log_e_u2,"orange","Erreur locale e_u - TRI6")
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

print("Tracés courbes des tendances TRI3 et TRI6 ")
# Données 
eu1=e_u[0]
eu2=e_u[1]

h1=h[0]
h2=h[1]

# Affichages de A1 et B1 
B1=Calcul_B(eu1,eu2,h1,h2) 
print("\nB1 = ",round(B1,3))

A1=Calcul_A(eu1,h1,B1)
print("\nA1 = ",round(A1,3))

# Initialisations
X1=[]
# Calcul abscicce courbe tendance
for hi in h :
    x1=np.log10(A1)+((B1+1)*hi)
    X1.append(round(x1,5))
print("\nX1 = log10(A1)+((B1+1)*hi : \nX1=",X1)

def courbeTendance_uh(x,y,c):
    plt.plot(x,y, marker = 'o',color=c)    
    plt.xlabel ("log h ")    
    
    if y==log_e_u1 :
        plt.title("Courbe de tendance fonction de log h \nElement triangle à 3 noeuds TRI3")
        plt.ylabel(" log e_u1 ")
        plt.savefig("Courbe_de_tendance_1-Erreur locale (h)- TRI3")
    else:
        plt.title("Courbe de tendance en fonction de log h \nElement triangle à 6 noeuds TRI6")
        plt.ylabel(" log e_u2 ")
        plt.savefig("Courbe_de_tendance_2-Erreur locale (log h)- TRI6")
    
    plt.show()

# Appel de fonction courbe_de tendance
courbeTendance_uh(X1,log_e_u1,"b")
courbeTendance_uh(X1,log_e_u2,"r")


print("\nCalcul erreur de discrétisation locale e_s :\n")

# Chargement des données fichier résultats uh_max(M)
sh=ficList("sh_max.txt")

print("\nListe des contraintes axiales sh en MPa avec RDM6 : \n \nsh = ", sh)

# Affichage sh_maillage
print("\nLes résultats en contrainte sh_max en MPa "\
      "\nde la modélisation RDM6 des 7 maillages,\n "\
      "\nsh_numéro_maillage :")

for i in range(len(sh)):
    print("\nsh_{} = {}".format(i+1,round(sh[i],5)))

# Fonction erreur de discrétisation locale
def erreurGlob(sh,s_ref):
    for s in sh:
        eg=(np.abs((s-s_ref)))/(np.abs(s_ref)) 
        e_s.append(round(eg,5))
    return e_s

e_s=erreurGlob(sh,s_ref)

# Affichage erreurs locales
print("\nLes erreurs de discrétisation globales calculées " \
      "\nsont regroupées dan la liste ci-dessous : \n \nerreurs_globales : \ne_s = ",e_s)

# Découpage résulats sh_TRI3 et sh_TRI6
sh1=sh[0:3]
print("\nsh1=",sh1)

sh2=sh[3:6]
print("\nsh2=",sh2)

def trace_sh_h(sh,h,c):
    "Fonction trace sh en fonction de h pour TRI3 et TRI6"
    plt.plot(h,sr,"r--",marker = 'o',label="solution de reference")
    plt.plot(h,sh, marker = 'o',color=c,label="solution numérique")
    plt.xlabel ("taille moyenne en mm ")
    
    if sh==sh1 :
        plt.title("Contrainte maximale sh en fonction de la taille moyenne h , \nElement triangle à 3 noeuds TRI3")
        plt.ylabel(" sh_1 en Mpa - TRI3")
        plt.savefig("Graphe- sh(h) - TRI3")
    else :
        plt.title("Contrainte maximale sh en fonction de la taille moyenne h \nElement triangle à 6 noeuds TRI6")
        plt.ylabel(" sh_2 en MPa- TRI6")
        plt.savefig("Graphe-sh(h) - TRI6")
    
    plt.legend()
    plt.show()
    
trace_sh_h(sh1,h,"m")
trace_sh_h(sh2,h,"k")


# Tracé en échelles logaritmique des erreurs globales s_u1 TRI3 et s_u2 TRI6:
print("\nTracé logaritmique des erreurs de discrétisations glbcales TRI3 et TRI6 : ")

e_s1=e_s[0:3]
log_e_s1=Log10(e_s1)
print("\nlog10 e_s1=",log_e_s1)

e_s2=e_s[3:6]
log_e_s2=Log10(e_s2)
print("\nlog10 e_s2=",log_e_s2)


def traceEglob_h(logh,log_eglob,c,label):
    plt.plot(logh,log_eglob, marker = 'o',color=c,label=label)
    plt.legend()
    plt.xlabel (" log10_h ")
    plt.title("Echelle logaritmique \n Erreurs globales TRI3 TRI6 en fonction de la taille moyenne")
    plt.ylabel(" log10_e_s")
    plt.savefig("Graphe - Log erreurs globales (h) - TRI3-et TRI6")
    
traceEloc_h(logh,log_e_s1,"c","Erreur globale e_s - TRI3")
traceEloc_h(logh,log_e_s2,"m","Erreur globale e_s - TRI6")
plt.show()  

print("Tracés courbes des tendances TRI3 et TRI6 ")
# Données 
es1=e_s[0]
es2=e_s[1]

# Affichages de A1 et B1 
B2=Calcul_B(es1,es2,h1,h2) 
print("\nB1 = ",round(B2,3))

A2=Calcul_A(es1,h1,B2)
print("\nA1 = ",round(A2,3))

# Initialisations
X2=[]
# Calcul abscicce courbe tendance
for hi in h :
    x2=np.log10(A2)+(B2*hi)
    X2.append(round(x2,5))
print("\nX2 = log10(A2)+(B2*hi) : \nX2=",X2)

def courbeTendance_sh(x,y,c):
    plt.plot(x,y, marker = 'o',color=c)    
    plt.xlabel ("log h ")    
    
    if y==log_e_s1 :
        plt.title("Courbe de tendance fonction de log h \nElement triangle à 3 noeuds TRI3")
        plt.ylabel(" log e_s1 ")
        plt.savefig("Courbe_de_tendance_1-Erreur globale (h)- TRI3")
    else:
        plt.title("Courbe de tendance en fonction de log h \nElement triangle à 6 noeuds TRI6")
        plt.ylabel(" log e_s2 ")
        plt.savefig("Courbe_de_tendance_2-Erreur globale (log h)- TRI6")
    
    plt.show()

# Appel de fonction courbe_de tendance
courbeTendance_sh(X2,log_e_s1,"g")
courbeTendance_sh(X2,log_e_s2,"m")

print("Graphes comparaisons erreurs locales et globales TRI3 et TRI6  ")

# Graphes comparaisons erreurs locales et globales TRI3 et TRI6 

def compareErr(h,y,z,c1,c2,lab1,lab2):
#    plt.subplot(211)
    plt.xlabel(" taille moyenne h ")
    plt.ylabel(" erreurs de discrétisations ")
    plt.plot(y,h,marker="o",label=lab1,color=c1)
    plt.plot(z,h,marker="o",label=lab2,color=c2)
    
    if y==e_u1 and z==e_s1:
        plt.title("Erreur globale et locale en fonction de h - TRI3")
        plt.savefig("Erreurs-locale-et-globale (h)- TRI3")
    
    elif y==e_u2 and z==e_s2:
        plt.title("Erreur globale et locale en fonction de h - TRI6")
        plt.savefig("Erreurs-locale-et-globale (h)- TRI6")
    
    elif y==e_u1 and z==e_u2:
        plt.title("Erreurs locales en fonction de h - TRI3 et TRI6")
        plt.savefig("Erreurs-locale (h)- TRI3 et TRI6")
    
    else:
        plt.title("Erreurs globales en fonction de h - TRI3 et TRI6")
        plt.savefig("Erreurs globales (h)- TRI3 et TRI6")
    
    plt.legend()
    plt.show()

plt.subplot(211)
compareErr(h,e_u1,e_s1,"r","b",lab1="erreur locale TRI3",lab2="erreur globale TRI3") 

plt.subplot(212) 
compareErr(h,e_u2,e_s2,"orange","c",lab1="erreur locale TRI6",lab2="erreur globale  TRI6")

plt.subplot(211)
compareErr(h,e_u1,e_u2,"k","g",lab1="erreur locale TRI3",lab2="erreur locale TRI6") 

plt.subplot(212)
compareErr(h,e_s1,e_s2,"y","m",lab1="erreur globale TRI3",lab2="erreur globale TRI6") 


