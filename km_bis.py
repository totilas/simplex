import time
import cyfferssimplex
import sys
import matplotlib.pyplot as plt 
import numpy as np 


def genere_lp(d):
	s = ""
	s += str(d)+"\n"
	s += str(d)+"\n"
	for i in range(d):
		s += str(10**(d-i-1)) + " "
	s += "\n"

	cons = 1
	for i in range(d):
		s += str(cons) + " "
		cons *= 100
	s += "\n"

	for i in range(d):
		for j in range(d):
			if j< i:
				s += str(2 * 10**(i-j))+" "
			elif j == i :
				s += str(1) + " "
			else :
				s += str(0) + " "
		s += "\n"

	return s




def single_run(nom, d, methode):
	sol = "tests/c-interesting/km_bis"+methode+str(d)+".out"
	sys.stdout = open(sol,'wt')
	begin_t = time.time()
	number_pivot, incorrect = cyfferssimplex.simplex(nom, method=methode, verbose = False, verification = True)
	end_t = time.time()
	t = end_t - begin_t
	sys.stdout = sys.__stdout__
	if incorrect :
		print("allez voir", nom)
	else :
		return number_pivot, t





random_p = []
Bland_p = []
maxcoef_p = []
myrule_p = []

random_t = []
Bland_t = []
maxcoef_t = []
myrule_t = []

for d in range(2,10):
	nom = "tests/c-interesting/kleeminty_bis"+str(d)+".dat"
	with open(nom, "w") as f:
		f.write(genere_lp(d))
	n_rand, t_rand = single_run(nom, d, "random")
	n_bland, t_bland = single_run(nom, d, "Bland")
	n_max, t_max = single_run(nom, d, "maxcoef")
	n_myrule, t_myrule = single_run(nom, d, "myrule")

	random_t.append(t_rand)
	random_p.append(n_rand)
	Bland_t.append(t_bland)
	Bland_p.append(n_bland)
	maxcoef_t.append(t_max)
	maxcoef_p.append(n_max)
	myrule_t.append(t_myrule)
	myrule_p.append(n_myrule)



X = [i for i in range(2,10)]
plt.figure(figsize=(10,5))
plt.title("Comparaison du temps d'execution pour les instances de Klee-Minty")
plt.xlabel("Nombre de variable")
plt.ylabel("Temps")
plt.plot(X, random_t, label="random", color='b')
plt.plot(X, Bland_t, label="Bland", color='r')
plt.plot(X, maxcoef_t, label="maxcoef", color='g')
plt.plot(X, myrule_t, label= "my rule", color='c')
plt.legend()
plt.savefig("temps_km_bis.png")

plt.figure(figsize=(10,5))
plt.title("Comparaison du nombre de pivot pour les instances de Klee-Minty")
plt.xlabel("Nombre de variable")
plt.ylabel("Nombre de pivots")
plt.plot(X, random_p, label="random", color='b')
plt.plot(X, Bland_p, label="Bland", color='r')
plt.plot(X, maxcoef_p, label="maxcoef", color='g')
plt.plot(X, myrule_p, label= "my rule", color='c')
plt.legend()
plt.savefig("pivot_km_bis.png")

plt.show()



