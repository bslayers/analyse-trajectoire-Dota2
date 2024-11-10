import numpy as np
from propa_affin.Propagation_affinite import *
from traclus.traclus import *
from traclus.ATP import *
from traclus.representative_Trajectory_Generation import *
from k_means import *
from traclus.LSC import *
class Test_traclus:
    
    def __init__(self,coord):
        self.coord = coord
        self.test_trajectories = [plageDeDonnee(self.coord,2)]
        
    def tests_traclus(self):
        result = traclus(self.test_trajectories)
        assert type(result) == tuple, "TRACLUS:Le résultat doit être un tuple"
        assert type(result[0]) == list, "TRACLUS:Le résultat[0] doit être une liste"
        assert type(result[1]) == np.ndarray, "TRACLUS:Le résultat[1] doit être une liste numpy"

        assert np.array(result[0]).shape[0] == 1, "TRACLUS:Le nombre de joueur testé doit etre 1"#teste si le nombre de joueur testé est bien 1
        assert np.array(result[0]).shape[1] >= 0, "TRACLUS:Il doit y a voir un résultat" #teste si il y a un resultat
        assert np.array(result[0]).shape[2] == 2, "TRACLUS:Le format est incorrect" #teste si le format des coordonées est corect

        #voir pour des tests pour result[1]

        print("TRACLUS:Test réussi")
    
    def tests_K_means(self):
        empty_result = k_moyenne(recup("coordinates/coord_4080601137.csv"),5)#test avec un joueur absent
        result = k_moyenne(self.coord,5,2)#take the player given for the test
        assert empty_result == (False,False), "K_mean:Donner une liste vide en entré ne renvoi pas le bon resultat"

        assert type(result) == tuple, "K_means:Le résultat doit être un tuple"
        assert type(result[0]) == np.ndarray, "K_means:Le résultat[0] doit être une liste numpy"
        assert type(result[1]) == list, "K_means:Le résultat[1] doit être une liste"

        print("K_means:Test réussi")
    
    def tests_propa_affin(self):
        return
    
    def test_ATP(self):
        result = ATP(self.test_trajectories[0])#take the player given for the test
        assert type(result) == np.ndarray, "ATP:Le résultat doit être une liste numpy"
        assert result.shape[0] >= 0, f"ATP:Il doit y a voir un résultat,{result[0].shape[0]} est donné" #teste si il y a un resultat
        assert result.shape[1] == 2, f"ATP:Le format est incorrect,{result[0].shape[1]} est donné" #teste si le format des coordonées est corect
        print("ATP:Test réussi")
    
    def test_LSC(self):
        result = LSC(ATP(self.test_trajectories[0]))#take the player given for the test, then apply ATP
        assert type(result) == np.ndarray, "LSC:Le résultat doit être une liste numpy"
        assert result.shape[0] >= 0, f"LSC:Il doit y a voir un résultat,{result[0].shape[0]} est donné" #teste si il y a un resultat
        assert result.shape[1] == 2, f"LSC:Le format est incorrect,{result[0].shape[1]} est donné" #teste si le format des coordonées est corect
        print("LSC:Test réussi")
    
    def test_RTG(self):
        result = representative_Trajectory_Generation(LSC(ATP(self.test_trajectories[0])),0,0)#take the player given for the test, then apply ATP
        assert type(result) == np.ndarray, "RTG:Le résultat doit être une liste numpy"
        assert result.shape[0] >= 0, f"RTG:Il doit y a voir un résultat,{result[0].shape[0]} est donné" #teste si il y a un resultat
        assert result.shape[1] == 2, f"RTG:Le format est incorrect,{result[0].shape[1]} est donné" #teste si le format des coordonées est corect
        print("RTG:Test réussi")
    
    