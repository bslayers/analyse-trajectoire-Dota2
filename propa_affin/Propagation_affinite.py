import numpy as np
# Calcule la matrice de disponnibilité (availability en anglais)
# Cette matrice test un coeur de cluster à partir d'un point de donnée
# (dans notre cas, des trajectoires) pour vérifier si il est un bon
# coeur de cluster.
def calcul_matrice_availability(resp, lam):
    if resp.size == 0:
        return np.array([]) 
    Rp = np.maximum(resp,0)
    np.fill_diagonal(Rp,resp.diagonal())
    sRp = np.linalg.norm(Rp,axis=1)
    A = sRp[:,np.newaxis] - Rp
    Amin = np.array([[0,0],[0,0]])
    np.fill_diagonal(A,Amin.diagonal())
    A = (1-lam) * A - lam * A
    return A

# Calcule la matrice de fiabilité (responsability)
# Cette matrice test l'appartenance des points de données à un coeur de cluster
# pour confirmer que le cluster est bien placé.
def calcul_matrice_responsability(sim, av, max_it, conv_it, lam):
    #A = np.zeros(av.shape)
    AS = av + sim[:,np.newaxis]
    if AS.size == 0:
        return np.array([])   
    i, j = np.unravel_index(AS.argmax(), (AS.shape))
    maxval= np.max(AS)
    AS[i][j] = -9999999
    maxval2 = np.max(AS)
    maxAS = np.tile(maxval, AS.shape)
    maxAS[i][j] = maxval2
    R = sim[:,np.newaxis] - maxAS
    R = ((1 - lam) * R) - (lam * R)
    return R

# Calcule de la matrice de similarité
# Cette matrice est la distance euclidienne carré négative.
# Le principe est de faire les calculs sur la moitié supérieure à
# la diagonale pour aller plus vite (puisque la matrice est carré)
# La matrice de similarité va influer tout les autre calculs.
def calcul_matrice_similarite(des):
    if len(des[0][0]) == 0:
        return np.array([])
    return -(np.linalg.norm(np.array(des)[0][0],axis=1))
    
def propagation_affinite(data, it, lam):
    similarite = calcul_matrice_similarite(data)
    availability = np.zeros(data.shape)
    responsability = calcul_matrice_responsability(similarite,availability, 10,10,lam)
    availability = calcul_matrice_availability(responsability,lam)
    i = 0
    if responsability.size == 0 and availability.size == 0:
        return np.array([])
    while i < it:
        responsability = calcul_matrice_responsability(similarite,availability, 10,10,lam)
        availability = calcul_matrice_availability(responsability,lam)
        i+=1
    return responsability + availability


