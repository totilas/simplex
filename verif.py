from scipy.optimize import linprog
import numpy as np


def comparaison(c,b,a, result):
	a = np.array(a, dtype=float)
	b = np.array(b, dtype=float)
	c = -np.array(c, dtype=float)

	res = linprog(c,a,b)
	if abs(result-res.fun)>.1 and res.status == 0: 
		print("Oups, something goes wrong")
		print("Real value: ", res.fun)
		print("For the values", res.x)
		return 1
	elif res.status == 2:
		print("Solution unfeasible")
	elif res.status == 3:
		print("Solution unbounded")
	else:
		print("Solution checked")
		return 0
