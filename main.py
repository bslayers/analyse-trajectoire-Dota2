import numpy as np
from k_means import *
from traclus.traclus import *
from propa_affin.Propagation_affinite import *
import time
import sys
from test_code.Test_traclus import *



a = recup("coordinates/coord_4080601137.csv")
if len(sys.argv)==2:

	if sys.argv[1]=="propa_affin":
		start = time.time()
		for i in range(1,11):
			b = [plageDeDonnee(a,i) for i in range(i,i+1)]
			descriptor = traclus(b)
			propa_res = (propagation_affinite(np.array(descriptor),10,0.1))
			print("--------------------")
			print(propa_res.shape)
			print(propa_res)
			print("--------------------")

		end = time.time()
		elapsed = (end - start)
		print(f'Temps d\'exécution : {elapsed}ms')
	elif sys.argv[1]== "k_means":
		start = time.time()
		lsave = []
		llc = []
		for pl in range(1,11,1):
		    save,lc = k_moyenne(a,6,player=pl,N=10)
		    lsave.append(save)
		    llc.append(lc)
		
		end = time.time()
		for pl in range(len(lsave)):
			affichagek_means(lsave[pl],llc[pl])
		elapsed = (end - start)

		print(f'Temps d\'exécution : {elapsed}ms')
	else:
		test = Test_traclus(recup("coordinates/coord_4080601137.csv"))
		test.test_ATP()
		test.test_LSC()
		test.test_RTG()
		test.tests_traclus()
		test.tests_K_means()

else:
	test = Test_traclus(recup("coordinates/coord_4080601137.csv"))
	test.test_ATP()
	test.test_LSC()
	test.test_RTG()
	test.tests_traclus()
	test.tests_K_means()
