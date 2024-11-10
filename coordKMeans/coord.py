import matplotlib.pyplot as plt
import numpy as np
import random as rd
'''
@author Laloux Loic
Classe coord qui récupère les données des parties les sépare en différents atributs et renvoie plusieurs méthode 
'''
class coord:

    '''
    Constructeur de la classe 
    path est le chemin d'accès au fichier
    '''
    def __init__(self,path):
        self.path=path
        self.var= np.genfromtxt(path, delimiter=",", skip_header=1)
        self.coordT= self.var[1:,[3,4,7,8,11,12,15,16,19,20,23,24,27,28,31,32,35,36,39,40]] #colonne des coordonnées des joueur
        self.col1 = np.arange(0,(self.coordT.shape[1]-1)//2,2)
        self.j1 = self.var[1:,[3,4]] #Coordonnées du joueur1
        self.j2 = self.var[1:,[7,8]] #Coordonnées du joueur2
        self.j3 = self.var[1:,[11,12]] #Coordonnées du joueur3
        self.j4 = self.var[1:,[15,16]] #Coordonnées du joueur4
        self.j5 = self.var[1:,[19,20]] #Coordonnées du joueur5
        self.xEquip1 = self.coordT[1:,self.col1[:]] #Abscisse de toute l'equipe 1
        self.yEquip1 = self.coordT[1:,self.col1[:]+1] #Ordonnée de toute l'equipe 1
        self.coordEquip1 = np.concatenate((self.xEquip1,self.yEquip1),axis=1) #Coordonnées de toute l'équipe 1
        self.col2 = np.arange(self.coordT.shape[1]//2,self.coordT.shape[1]-1,2)
        self.j6 = self.var[1:,[23,24]] #Coordonnées du joueur6
        self.j7 = self.var[1:,[27,28]] #Coordonnées du joueur7
        self.j8 = self.var[1:,[31,32]] #Coordonnées du joueur8
        self.j9 = self.var[1:,[35,36]] #Coordonnées du joueur9
        self.j10 = self.var[1:,[39,40]] #Coordonnées du joueur10
        self.xEquip2 = self.coordT[1:,self.col2[:]] #Abscisse de toute l'equipe 2
        self.yEquip2 = self.coordT[1:,self.col2[:]+1] #Ordonnée de toute l'equipe 2
        self.coordEquip2 = np.concatenate((self.xEquip2,self.yEquip2),axis=1) #Coordonnées de toute l'équipe 2
        self.xmax = np.max(self.coordT)
        self.l = [] #Liste contenant les points aléatoire


    '''
    Affiche en graphique les données de tout les joueurs ou de l'équipe
    @param equip equipe d'ou l'on veut afficher equip=1 pour l'equipe 1 equip=2 pour l'equipe 2 equip=0 par défault toute les equipes
    '''
    def show(self,equip=0):
        if equip!=2:
            plt.plot(self.xEquip1, self.yEquip1, "g")
        if equip!=1:
            plt.plot(self.xEquip2, self.yEquip2, "b")
        if self.l != []:
            for i in range (len(self.l)):
                plt.plot(self.l[i][0], self.l[i][1],"or")

    '''
    choisis un point aléatoire en fonction des données de tout les joueurs ou de l'équipe
    @param equip equipe d'ou l'on veut afficher equip=1 pour l'equipe 1 equip=2 pour l'equipe 2 equip=0 par défault toute les equipes
    '''
    
    def randPoint(self,equip=0):
        plage = np.ones(1)
        if equip==1:
            plage = self.coordEquip1
        if equip==2:
            plage = self.coordEquip2
        else:
            plage = self.coordT
        c = rd.randrange(1,plage.shape[1]-1,2)
        l = rd.randint(0,plage.shape[1]-1)
        xrand = plage[c,l]
        while xrand == 0 :
            c = rd.randrange(1,plage.shape[1]-1,2)
            l = rd.randint(0,plage.shape[1]-1)
            xrand = plage[c,l]
        c = rd.randrange(1,plage.shape[1]-1,2)
        l = rd.randint(0,plage.shape[1]-1)
        yrand = plage[c,l]
        while yrand == 0:
            c = rd.randrange(1,plage.shape[1]-1,2)
            l = rd.randint(0,plage.shape[1]-1)
            yrand = plage[c,l]
        randl = []
        randl.append(xrand)
        randl.append(yrand)
        self.l.append(randl)

    '''
    remets la liste de points aléatoires a 0
    '''
    def clear(self):
        self.l=[]

    '''
    choisis k point aléatoires selon tout les joueurs ou les joueurs de chaque equipe
    @param k le nombre de point aléatoire
    @param equip equipe d'ou l'on veut afficher equip=1 pour l'equipe 1 equip=2 pour l'equipe 2 equip=0 par défault toute les equipes
    '''
    def kpoint(self,k,equip=0):
        self.clear()
        for i in range(k):
            if equip==1:
                self.randPoint(1)
            elif equip==2:
                self.randPoint(2)
            else:
                self.randPoint()

    def getl(self):
        return self.l
