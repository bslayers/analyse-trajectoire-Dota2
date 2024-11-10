#python3 -m traclus.traclus   permet de lancer le progamme tout en restant à la racine
import numpy as np
from traclus.ATP import *
from traclus.representative_Trajectory_Generation import *
from traclus.LSC import *
from k_means import *

#Algorithm TRACLUS (TRAjectory CLUStering)
#Input: A set of trajectories I = {T R1, · · · , T Rnumtra }
#Output: (1) A set of clusters O = {C1, · · · , Cnumclus }
#(2) A set of representative trajectories
#Algorithm:
#/* Partitioning Phase */
#01: for each (T R ∈ I) do
#/* Figure 8 */
#02: Execute Approximate Trajectory Partitioning;
#Get a set L of line segments using the result;
#03: Accumulate L into a set D;
#/* Grouping Phase */
#/* Figure 12 */
#04: Execute Line Segment Clustering for D;
#Get a set O of clusters as the result;
#05: for each (C ∈ O) do
#/* Figure 15 */
#06: Execute Representative Trajectory Generation;
#Get a representative trajectory as the result;

def traclus(trajectories,minl = 100):
    #/* Partitioning Phase */
    d = []
    for tr in trajectories:
        #02: Execute Approximate Trajectory Partitioning;
        #03: Accumulate L into a set D;
        d.append(ATP(tr))
    #04: Execute Line Segment Clustering for D;
    
    a=0
    o = []
    for i in d:
        a+=1
        o.append(LSC(i,0.1,minl))

    #05:
    res = np.array([])
    for i,elt in enumerate(o):
        tmp = np.array([])
        for line in elt:#partie modifiée dernierement, peut causer des bugs
            rtg = representative_Trajectory_Generation(line,minl,0)
            tmp = np.append(tmp,np.array(rtg))
        res = np.append(res,tmp)
    return (o,res)

if __name__ == '__main__':
    re = recup("coordinates/coord_3841665963.csv")
    b = [plageDeDonnee(re,i) for i in range(1,2)]
    print("traclus",traclus(b,3))
