#########################Importation de modules################################
import numpy as np
from math import sin,cos,pi
from scipy.integrate import quad
import os
import string

#########################Fonctions Annexes#####################################
def tritri(L): # Pour trier la liste
    if L == []:
        return []
    else:
        pivot = L[0]
        L1=[]
        L2=[]
        for x in L[1:]:
            if x<pivot:
                L1.append(x)
            else:
                L2.append(x)
        return tritri(L1)+[pivot]+tritri(L2)


def getFloat(s): 
    #Pour recuperer des nombres decimaux dans une chaine de caractères
    value=[]
    for i in s.split():
        word = i.replace(" ", ",")
        try:
            value.append(float(word))
        except:
            pass
    return value

def moy(h,k): #Calcul de yi barre
    return (h+k)/2

def f(x):
    return sin(2*x)+cos(3*x)

########################CREATION D'UNE TABLE###################################

Lascii=string.ascii_uppercase

###############################PROGRAMME PRINCIPAL#############################
#Question 1.1
def EFonctionFichier(nomfichier,f,a,b,n):
    #On suppose egalement que chaque ordonnée correspond a une seule abscisse
    L=[f(a)]+[0]*(n-1)+[f(b)] #Ordonne
    M=[a]+[0]*(n-1)+[b]  #Abscisse
    for i in range(1,n):
        M[i]=M[0]+i*(b-a)/n
        L[i]=f(M[i])
    L1=L
    L=tritri(L) #Fonction annexe
    if L==L1:
        M1=M
    else:
        M1=[]
        for i in range(len(L)):
            s=L1.index(L[i])
            M1+=[M[s]]            
    fichier=open(nomfichier,"x") 
    """x, crée un nouveau fichier et l'ouvre pour écriture"""
    for i in range(len(M)):
        fichier.write("\nUn point '%s,%s' " %(L[i],M1[i]))
    fichier.close()

#Question1.2
def EMesureFichier(nomfichier,L,M):
    #On suppose qu'à chaque ordonnée correspond une seule abscisse
    L1=L
    L=tritri(L)
    M1=[]
    if L==L1:
        M1=M
    else:
        for i in range(len(L)):
            s=L1.index(L[i])
            M1.append(M[s])
    print(len(L),len(M1))
    Mesure=open(nomfichier,"a") 
    """a, pour une ouverture en mode ajout à la fin du fichier (APPEND). 
    Si le fichier n'existe pas python le crée."""
    for i in range(len(M)):
        Mesure.write("\nUn point '%s %s' " %(L[i],M1[i]))
    Mesure.close()
                   
#Question 1.3
def LFichier(nomfichier):
    """On suppose que chaque ligne est enregistré de la facon suivante
    Un point "valeur,valeur". Les 2 espaces sont très importants !"""
    Lx1=[]
    Ly1=[]
    Lfichier=[]
    LxLybis=[]
    global Lascii
    with open(nomfichier, "rb") as fichier:
        #r, pour une ouverture en lecture (READ)
        while 1:
            data=fichier.readline()
            if not data:
                break
            Lfichier.append(data)
    LxLy=[k[10:-1] for k in Lfichier]
    print(len(LxLy))
    print(LxLy)
    for i in LxLy:
        LxLybis+=getFloat(i) #Fonction annexe
    print(LxLybis)
    for i in range(len(LxLybis)):
        if i%2==0:
            Lx1.append(LxLybis[i])
        else:
            Ly1.append(LxLybis[i])
    return Lx1,Ly1
                   
#Question 1.4
def rectangle(x,y):
    S=0
    for i in range(1,len(x)):
        S+=(x[i]-x[i-1])*y[i]
    return S

#Question 1.5
def trapeze(x,y):
    S=0
    for i in range(1,len(x)):
        S+=0.5*(x[i]-x[i-1])*(y[i]-y[i-1])
    return S

#Question 1.6
def msimpson(x,y):
    S=0
    for i in range(1,len(x)):
        S+=(1/6)*(x[i]-x[i-1])*(y[i]+4*moy(y[i],y[i-1])+y[i-1])#Fonction annexe
    return S

#Question 1.7
# Par la methode rectangle approximation de la courbe par des rectangles 
# Par la methode trapeze approximation de la courbe par des trapèzes
# Par la methode msimpson approximation de la courbe par des arcs de parabole

#Question 1.8
def CMethodes(nomfichier):
    Lx,Ly=LFichier(nomfichier)
    T = np.array([[0 for j in range(2)] for i in range(3)])
    methodes=['rectangle','trapeze','msimpson']
    L=[rectangle(Lx,Ly),trapeze(Lx,Ly),msimpson(Lx,Ly)]
    for k in range(len(T)):
        T[k][0]=methodes[k]
        T[k][1]=L[k]
    return T

#Question 1.9 
def Question1_9(nomfichier,func): 
    #ici nomfichier est une chemin menant a un fichier
    M4=np.array([[0,0]]) #On initialise par une ligne de 0
    for n in range(5,21,5):
        EFonctionFichier(nomfichier,func,0,0.5*pi,n)
        M=CMethodes(nomfichier)
        np.append(M4,M,axis=0)
        os.rmdir(nomfichier)
    s,err=quad(func,0,0.5*pi)
    b=np.array([['scipy',s]])
    np.append(M4,b,axis=0)
    return np.delete(M4,0,axis=0) #La premiere ligne etant que des 0
               
#Realisé en 4h45    
