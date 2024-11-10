import matplotlib.pyplot as plt
import numpy as np
import random as rd
from coordKMeans.coord import *
'''
@author Laloux Loic
Classe cluster qui associe une liste des points qui lui sont assigné et modifie son point en fonction
'''
class cluster_coord:

    '''
    Constructeur de la classe cluster
    i est l'indice du cluster dans la liste de tout les cluster
    coord est la plage de coord que la classe va utiliser
    '''
    def __init__(self,i,coord):
        self.coord = coord
        self.i = i
        self.point = self.coord.l[i]
        self.liste=np.array([])

    
    '''
    méthode qui associe les coordonnee a ce cluster en fonction de la distance entre le centre su cluster et les differente coordonnée
    PC est les points caractéristique du joueur
    player est l(indice +1 du joueur dans les fichiers coordinates/coord....csv
    algo est pour désigner l'algo qui l'utilisera et change certain chose
    '''
    def association_coord(self,PC,player,algo="k_means"):
        plage=[]
        if player ==2: #Selection de la plage
            plage = self.coord.j2
        elif player ==3:
            plage = self.coord.j3
        elif player ==4:
            plage = self.coord.j4
        elif player ==5:
            plage = self.coord.j5
            
        elif player ==6:
            plage = self.coord.j6
        elif player ==7:
            plage = self.coord.j7
        elif player ==8:
            plage = self.coord.j8
        elif player ==9:
            plage = self.coord.j9
        elif player ==10:
            plage = self.coord.j10
        else:
            plage = self.coord.j1
        dist =np.sqrt(np.sum((self.point-plage[:,:])**2,axis=1))#La distance entre un point $x$ et un ensemble de points $x_i$ consister à calculer: 
                                                            #$$\forall i\ \ \ d(x,x_i)^2 = \|x_i -x \|^2 = \sum_k (x_{i,k}-x_k)^2 . $$
        if algo=="affin":
            dist = dist[:]*-1#pour l'algo affin la distance est en négatif me demander pas pourquoi
        
        dist = np.argsort(dist)
        dist=dist[:100]
        
        #print(self.point)
        #print(dist)
        self.liste=np.append(self.liste,plage[dist])
        plage[dist]=0
        self.liste = np.array(list(zip(self.liste[::2], self.liste[1::2])))#Pour avoir une liste de forme [[x1,y1],[x2,y2],...,[xn,yn]] au lieu de [x1,y1,x2,y2,...,xn,yn]
        return self.liste,dist

    '''
    méthode qui modifie le point centrale du cluster en faisant la moyenne entre les distance de ses points associé
    '''
    def moyenneK_means(self):
        verif = self.point
        if self.liste.shape[0]==0:
            print("dist deja pris par un autre")
            return True
        self.point = [np.mean(self.liste[:,0]),np.mean(self.liste[:,1])]#on veut que le poin central soit [moyenne(x),moyenne(y)]
        self.coord.l[self.i]=0
        #print(self.coord.l[self.i])
        self.coord.l[self.i]=self.point
        if self.point == verif:
            return True
        return False
     


class cluster:
    def __init__(self,point,plage):
        self.plage = plage
        self.point = point
        self.liste = np.array([])

    
    def association(self,algo="k_means"):
        
        dist =np.sqrt(np.sum((self.point-self.plage[:,:])**2,axis=1))#La distance entre un point $x$ et un ensemble de points $x_i$ consister à calculer: 
                                                            #$$\forall i\ \ \ d(x,x_i)^2 = \|x_i -x \|^2 = \sum_k (x_{i,k}-x_k)^2 . $$
        if algo=="affin":
            dist = dist[:]*-1#pour l'algo affin la distance est en négatif me demander pas pourquoi
        
        dist = np.argsort(dist)
        dist=dist[:100]
        
        #print(self.point)
        #print(dist)
        self.liste=np.append(self.liste,self.plage[dist])
        self.plage[dist]=0
        self.liste = np.array(list(zip(self.liste[::2], self.liste[1::2])))#Pour avoir une liste de forme [[x1,y1],[x2,y2],...,[xn,yn]] au lieu de [x1,y1,x2,y2,...,xn,yn]
        return self.liste,dist

    def moyenneK_means(self):
        verif = self.point
        if self.liste.shape[0]==0:
            print("dist deja pris par un autre")
            return True
        self.point = [np.mean(self.liste[:,0]),np.mean(self.liste[:,1])]#on veut que le poin central soit [moyenne(x),moyenne(y)]
        #print(self.point)
        #if self.point == verif:
         #   return True
        return False

   
        
