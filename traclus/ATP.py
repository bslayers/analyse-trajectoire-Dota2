import math
import numpy as np
'''
@author Favier Hugo
Regroupe les fonction permetant d'obtenir des partitions approximatives d' une tragectoire
'''

def ProjectionPoint(p1,p2,P3):
    vecteur_12=(p2[0] - p1[0], p2[1] - p1[1])
    vecteur_13=(p3[0] - p1[0], p3[1] - p1[1])
    
    dot = vecteur_13[0] * vecteur_12[0] + vecteur_13[1] * vecteur_12[1]
    
    ps = [0, 0]
    
    norm = vecteur_12[0]**2 + vecteur_12[1]**2
    ps[0] = p1[0] + (dot / norm) * vecteur_12[0]
    ps[1] = p1[1] + (dot / norm) * vecteur_12[1]
    return ps

def PerpendicularDistance(Li,Lj):
    si = Li.start_point
    ei = Li.end_point
    sj = Lj.start_point
    ej = Lj.end_point
"""
   Cette fonction donne LD(H)
   @param H est une liste de points
   @return log2(distance(pointInitial,pointFinal))
"""
def L_D(H):
    total_distance = 0
    
    for i in range(1,len(H)): #peut etre avoir a retirer 1
        for j in range(i+1,len(H)):
            distance_ij = math.dist(H[i], H[j])
            total_distance += distance_ij
    
    return total_distance

"""
   Cette fonction donne L(H) soit log2(distance(pointInitial,pointFinal))
   @param H est une liste de points
   @return log2(distance(pointInitial,pointFinal))
"""
def L(H):
    if len(H) >= 2 and math.dist(H[0], H[-1])!=0:
        #print(math.dist(H[0], H[-1]))
        return math.log2(math.dist(H[0], H[-1]))
    else:
        
        return 0

"""
   Cette fonction donne la Minimum Description Lengh(MDL) avec le partitionnement
   @param p est une liste de points
   @param start est un indice dans p utilisé avec end pour échantillonner une partie de p 
   @param end est un indice dans p utilisé avec start
   @return la MDL de start à end
"""
def MDL_par(p,start = 0,end = -1):
    H = p[start:end]
    res = L(H) + L_D(H)
    return res
"""
   Cette fonction donne la Minimum Description Lengh(MDL) sans le partitionnement
   @param p est est une liste de points
   @param start est un indice dans p utilisé avec end pour échantillonner une partie de p 
   @param end est un indice dans p utilisé avec start
   @return la MDL de start à end
"""
def MDL_nopar(p,start = 0, end = -1):
    H = p[start:end]
    res = L(H)
    return res


"""
   Cette fonction correspond au partitionnement aproximatif de trajectoires.
    certains nom ont été abrégés pour simplifier l'algorithme.
        p => points
        cP => characteristicPoints correspond aux points retenu par l'algorithme

   @param p est une liste de points representant des trajectoires
   @return CP une liste des points characteristique de p
"""
def ATP(p):
    zero = np.zeros(p.shape)
    if np.array_equal(p,zero):
        return np.array([])
    cP = [p[0]]
    startIndex, length = 1, 1
    #print("start")
    
    while startIndex + length < len(p):
        currIndex = startIndex + length
        cost_par = MDL_par(p,startIndex, currIndex)
        #print("mDLpar")
        cost_nopar = MDL_nopar(p,startIndex, currIndex)
        #print("MDLnoPar")
        
        if cost_par > cost_nopar and cost_nopar!=0:
            cP.append(p[currIndex - 1])
            startIndex = currIndex - 1
            length = 1
            #print("cost")
        else:
            length += 1
            #print("pas cost")
    
    cP.append(p[-1])
    return np.array(cP)

