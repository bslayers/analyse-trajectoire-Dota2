from coordKMeans.coord import *
from traclus.ATP import *
from cluster import cluster_coord
from cluster import cluster
from traclus.traclus import * 
import math
import numpy as np
import copy
'''
author Loic Laloux
'''


'''
recupère le dossier contenant les fichier et renvoie une instance de coord
path est le chemin du fichier contenant les coordonnee
'''
def recup(path):
    c = coord(path)
    return c
#t=recup("coordinates/coord_4080601137.csv")

'''
affiche les coordonnées sur un tableau
c est la variable a afficher
plot est pour avoir un tableau avec seulement une variable 
si autre chose est marqué les tableau seront cumulé les un sur les autres
'''
def show(c,plot="show"):
    if isinstance(c,coord):
        c.show()
    elif isinstance(c,np.ndarray):
        plt.scatter(c[:,0],c[:,1])
    elif c==None:
        print("nul")
    if plot =="show":
        plt.show()
    
#show(t)

'''
méthode qui selectionne la plage de données en fonction du joueur
renvoie la plage correspondant a celle du joueur
'''
def plageDeDonnee(c,player):
    plage = np.ones(1)
    if player ==2: #Selection de la plage
        plage = c.j2
    elif player ==3:
        plage = c.j3
    elif player ==4:
        plage = c.j4
    elif player ==5:
        plage = c.j5
        
    elif player ==6:
        plage = c.j6
    elif player ==7:
        plage = c.j7
    elif player ==8:
        plage = c.j8
    elif player ==9:
        plage = c.j9
    elif player ==10:
        plage = c.j10
    else:
        plage = c.j1
    return plage

'''
renvoie le tableau de point caractéristique selon les joueurs par défault renvoie le tableau des points caractéristique du joueur 1 par défault
'''
def pointCaract(c,player=1):
    
    plage = plageDeDonnee(c,player)
    res = ATP(plage) #tableau de points caractéristique
    return res


'''
implementation de l'algorithme k moyenne
c sont les données transformée par la classe coord
k est le nombre de cluster
player est le joueur dont on veut les k-moyenne cluster
N est le nombre d'iteration
'''

def k_moyenne_coord(c,k,player=1,N=1):
    c.kpoint(k)#sélection aléatoire des points centraux des cluster
    lc= []
    plage = plageDeDonnee(c,player)
    coordonnee=coord(c.path)#copie des données de départ qui va être modifiés au fur et a mesure
    save = copy.deepcopy(coordonnee)#copie des données de départ qui sert de sauvegarde pour coordonnées et qui seront les données renvoyé a la fin
    coordonnee.l=c.getl()#mise des points aléatoires précédement calculé dans la copie que l'on va utiliser
    lrandpoint = np.array(coordonnee.getl())#transformation de la liste en liste numpy
    pC = pointCaract(c,player)#tableau des points caractéristique
    if not isinstance(pC,np.ndarray):
        print("le joueur n'est pas en train de jouer")
        return False,False
    zero = np.zeros(pC.shape)#création d'un tableau de même taille rempli de zéro pour vérifier le contenue
    '''
    print("initiale")
    show(c)
    '''
    if np.array_equal(pC,zero):#vérification si les deux sont égaux le joueur n'est pas actif donc on sort de la fonction
        print("le joueur n'est pas en train de jouer")
        return False,False
    for n in range(N):#entrée dans la boucle principale
        liste = coordonnee.getl()#récupération de la liste modifié par les autres algorithmes
        coordonnee = copy.deepcopy(save)#mise a zero de coordonnées avec les données de départ
        coordonnee.l= liste#mise des (nouveaux) points dans la copie que l'on va utilisé
        #print(n)
        for i in range(len(lrandpoint)):#boucle de création et d'assignation des cluster
            clus = cluster_coord(i,coordonnee)
            lc.append(clus)       
            #print(i)
            #print(lrandpoint[i],"\n")
            dist,asso=clus.association_coord(pC,player)
            '''
            plt.scatter(plage[:,0],plage[:,1])
            plt.scatter(plage[asso,0],plage[asso,1])
            plt.scatter(lrandpoint[i][0],lrandpoint[i][1],color='r')
            plt.show()'''
            '''
            if dist.shape[0]==0:
                print("pas de dist")
            else:
                
                plt.scatter(dist[:,0],dist[:,1])#affiche les points associe au cluster
                #plt.scatter(plage[asso],plage[asso])
                plt.scatter(lrandpoint[i][0],lrandpoint[i][1]) #affiche le point central du cluster
                plt.show()
            return asso,lrandpoint[i]
            #print(dist,"\n")
            #print(dist.shape,"\n\n")
            #'''
        #print("Moyenne\n\n\n\n")
        for i in range(len(lrandpoint)):#boucle de modification des points centraux
            #print(i)
            lc[i].moyenneK_means()
            lrandpoint[i]=lc[i].point
            #show(coordonnee)
        if n<=N-2:#reset la liste des cluster tantqu'il n'est pas a la derniere boucle
            lc=[]
        #show(coordonnee)
    save.l=coordonnee.getl()#mise des points centraux des cluster finaux
    return save,lc


def randpoint (o,k):
    randl = []
    for i in range(k):
        c = rd.randrange(1,o.shape[0]-1,2)
        l = rd.randrange(0,o.shape[0]-1)
        xrand = o[c]
        '''while xrand == 0 :
            c = rd.randrange(1,o.shape[0]-1,2)
            l = rd.randrange(0,o.shape[0]-1)
            xrand = o[c]'''
        
        randl.append(xrand)
    return np.array(randl)


def k_moyenne(c,k,player=1,N=1):
    b = [plageDeDonnee(c,player)]
    traclus_o,traclus_res = traclus(b)
    traclus_o = traclus_o[0]
    
    lc= []
    if not isinstance(traclus_o,np.ndarray):
        return False,False
    zero = np.zeros(traclus_o.shape)#création d'un tableau de même taille rempli de zéro pour vérifier le contenue
    '''
    print("initiale")
    show(c)
    '''
    if np.array_equal(traclus_o,zero):#vérification si les deux sont égaux le joueur n'est pas actif donc on sort de la fonction
        return False,False
    save = copy.deepcopy(traclus_o)
    randl = randpoint(traclus_o,k)
    for n in range(N):#entrée dans la boucle principale
        liste = randl#récupération de la liste modifié par les autres algorithmes
        coordonnee = copy.deepcopy(save)#mise a zero de coordonnées avec les données de départ
        #print(n)
        for i in range(randl.shape[0]):#boucle de création et d'assignation des cluster
            clus = cluster(randl[i],coordonnee)
            lc.append(clus)       
            #print(i)
            #print(lrandpoint[i],"\n")
            dist,asso=clus.association()
            '''
            plt.scatter(plage[:,0],plage[:,1])
            plt.scatter(plage[asso,0],plage[asso,1])
            plt.scatter(lrandpoint[i][0],lrandpoint[i][1],color='r')
            plt.show()'''
            '''
            if dist.shape[0]==0:
                print("pas de dist")
            else:
                
                plt.scatter(dist[:,0],dist[:,1])#affiche les points associe au cluster
                #plt.scatter(plage[asso],plage[asso])
                plt.scatter(lrandpoint[i][0],lrandpoint[i][1]) #affiche le point central du cluster
                plt.show()
            return asso,lrandpoint[i]
            #print(dist,"\n")
            #print(dist.shape,"\n\n")
            #'''
        #print("Moyenne\n\n\n\n")
        for i in range(randl.shape[0]):#boucle de modification des points centraux
            #print(i)
            lc[i].moyenneK_means()
            randl[i]=lc[i].point
            #show(coordonnee)
        if n<=N-2:#reset la liste des cluster tantqu'il n'est pas a la derniere boucle
            lc=[]
        #show(coordonnee)
    return save,lc

def affichagek_means_coord(c,lc,player=1):
    if c==False :
        print("aucune donnée")
    else :
        plage = plageDeDonnee(c,player)
        plt.scatter(plage[:,0],plage[:,1])
        for i in range(len(lc)):
            plt.scatter(lc[i].liste[:,0],lc[i].liste[:,1])
            plt.scatter(lc[i].point[0],lc[i].point[1],color='0')
    
        plt.show()

def affichagek_means(plage,lc):
    if not isinstance(plage,np.ndarray) :
        print("aucune donnée")
    else :
        plt.plot(plage[:,0],plage[:,1])
        for i in range(len(lc)):
            plt.scatter(lc[i].point[0],lc[i].point[1],color='0')
            plt.plot(lc[i].liste[:,0],lc[i].liste[:,1])
        plt.show()


















    