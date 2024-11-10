import numpy as np
import math
#1: calculer les vectors de direction V moyen
#2: tourner l'axes pour que X axis soit parallel a V
#3: création de la variable P qui est le debut et la fin des points du segments de C
#4: trier les Point de P en fonction de X'-valeur
#5:Pour chaque p dans P:
#6:      on creer la variable nump qui = la ligne de segments qui contient X'-valeur du point p    
#7:      si nump est >= minLns
#8:            diff = la différence de X'-valeur entre p and son point précedent         
#9:            si diff >= gamma
#10:               calculer les coord moyenne avg'_p
#11:               supprimer la rotation et récuperer le point avg_p
#12:               ajouter avg_p a la fin de RTR_i

# Une trajectoire représentative est une séquence de points RTRi = p1p2p3 · · · pj · · · p len i (1 ≤ i ≤ numclus)
def length(v):
    return np.sqrt(np.dot(v, v))
#La fonction angle retourne l'angle entre 2 vecteurs
def angle(v1, v2):
    return np.arccos(np.dot(v1, v2) / (length(v1) * length(v2)))
#minls = 
#gamma =
#c = 
def representative_Trajectory_Generation(c,minls,gamma):
    #1: calculer les vectors de direction V moyen
    if np.array_equal(c,np.array([])):
        return np.array([])
    Vmoy = np.mean(c, axis=0)
    #2: tourner l'axes pour que X axis soit parallel a V
    phi = angle(Vmoy, np.array([1,0]))
    Crot = np.array([[np.cos(phi),np.sin(phi)],[-np.sin(phi),np.cos(phi)]])@c.T
    Crot = Crot.T
    #3: création de la variable P qui est le debut et la fin des points du segments de C
    P = np.array([Crot[0],Crot[-1]])
    #4: trier les Point de P en fonction de X'-valeur
    P = np.sort(P,axis=0)
    #5:Pour chaque point p dans P
    # On calcule le nombre de segments qui contiennent la valeur X' de p
    RTR_i = []
    for i, p in enumerate(P):
        #6:on creer la variable nump qui = la ligne de segments qui contient X'-valeur du point p
        nump = np.sum(np.abs(p - P[:i]))
        #7: si nump est >= minLns
        if nump >= minls:
            #8:diff = la différence de X'-valeur entre p and son point précedent
            diff = nump - P[i-1] if i > 0 else 0 # peut-etre temporaire
            #9: si diff >= gamma
            if np.all(diff >= gamma): # vérifier si tous les éléments de diff sont supérieurs ou égaux à gamma
                #10: calculer les coord moyenne avg'_p
                avgp = p/np.sum(P) # temporaire
                #11: supprimer la rotation et récuperer le point avg_p
                avgp = avgp@np.array([[np.cos(-phi),np.sin(-phi)],[-np.sin(-phi),np.cos(-phi)]]).T
                #12: ajouter avgp a la fin de RTR_i
                RTR_i.append(avgp) 
    return np.array(RTR_i)


if __name__ == '__main__':
    c = np.array([[0, 2], [1, 0],[5, 2], [1, 0]])
    c2 = np.array([[2,8], [1, 3]])
    c3 = np.array([[24561,8], [1, 3],[222, 111], [999, 256],[5, 444], [333, 666],[24561,8], [1, 3],[222, 111], [999, 256],[5, 444], [333, 666]])
    c4 = np.array([[1, 3],[5, 444], [1, 3],[5, 444]])

    Vmoy = np.mean(c)
    print("means: ",Vmoy)
    phi = angle(Vmoy, 1)
    print("phi: ",phi)
    minls = 0.5
    gamma = 0.2
    RTR_i = representative_Trajectory_Generation(c, minls, gamma)
    print(RTR_i)
    RTR_i = representative_Trajectory_Generation(c2, minls, gamma)
    print(RTR_i)
    RTR_i = representative_Trajectory_Generation(c3, minls, gamma)
    print(RTR_i)
    RTR_i = representative_Trajectory_Generation(c4, minls, gamma)
    print(RTR_i)