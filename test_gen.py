import random
import time
import cyfferssimplex
import sys
import matplotlib.pyplot as plt 
import numpy as np


def genere_lp(n, m):
	s = ""
	s += str(n)+"\n"
	s += str(m)+"\n"
	for i in range(n):
		s += str(random.randint(-10,20))+" "
	s += "\n"

	for i in range(m): 
		s+= str(random.randint(10, 20))+" "
	s += "\n"

	for i in range(m):
		for j in range(n):
			s += str(random.randint(-10,15))+" "
		s += "\n"
	return s



def trial(n, m):
	nom = "tests/b-random/random"+str(n)+"-"+str(m)+".dat"
	with open(nom, "w") as f:
		f.write(genere_lp(n,m))
	
	sol = "tests/b-random/random"+str(n)+"-"+str(m)+".out"
	sys.stdout = open(sol,'wt')
	begin_t = time.time()
	number_pivot, incorrect = cyfferssimplex.simplex(nom, method="random", verbose = False, verification = True)
	end_t = time.time()
	t = end_t - begin_t
	sys.stdout = sys.__stdout__
	if incorrect :
		print("aller voir ", nom)
	else :
		return number_pivot, t


# tests pour un nombre de variable croissants
T = []
P = []
m = 20
for n in range(5,100):
	p = [0]*10
	t = [0]*10
	for i in range(10):
		p[i], t[i] = trial(n,m)
		"""
	p_mean = np.mean(p)
	t_mean = np.mean(t)
	T.append(t_mean)
	P.append(p_mean)
X = [i for i in range(5,100)]
plt.figure(figsize = (10, 5))


plt.title("Complexité du simplex en fonction du nombre de variables pour 20 contraintes")
plt.xlabel('Nombre de variables')
plt.ylabel('Temps')
plt.plot(X, T)
plt.savefig('comp_temp_var.png')

plt.figure(figsize = (10, 5))
plt.plot(X, P)
plt.ylabel('Nombre de pivots')
plt.title("Complexité du simplex en fonction du nombre de variables pour 20 contraintes")
plt.xlabel('Nombre de variables')
plt.savefig('comp_pivot_var.png')

plt.show()
"""
"""
T = []
P = []
m = 20
for n in range(5,100):
	p = [0]*10
	t = [0]*10
	for i in range(10):
		p[i], t[i] = trial(n,m)
	p_mean = np.mean(p)
	t_mean = np.mean(t)
	T.append(t_mean)
	P.append(p_mean)
X = [i for i in range(5,100)]
plt.figure(figsize = (10, 5))


plt.title("Complexité du simplex en fonction du nombre de variables pour 20 contraintes")
plt.xlabel('Nombre de variables')
plt.ylabel('Temps')
plt.plot(X, T)
plt.savefig('comp_temp_var_max.png')

plt.figure(figsize = (10, 5))
plt.plot(X, P)
plt.ylabel('Nombre de pivots')
plt.title("Complexité du simplex en fonction du nombre de variables pour 20 contraintes")
plt.xlabel('Nombre de variables')
plt.savefig('comp_pivot_var_max.png')

"""
