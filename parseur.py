from fractions import Fraction


def lp_parse(filename):
	with open(filename, "r") as f:
		n = int(f.readline())
		m = int(f.readline())
		c = list(map(Fraction, f.readline().split()))
		if len(c) != n :
			print("Bad number of coefficients in the objective function")
			return 1
		b = list(map(Fraction, f.readline().split()))
		if len(b) != m :
			print("Bad number of constraints")
			return 1
		a = []
		for i in range(m):
			a_row = list(map(Fraction, f.readline().split()))
			if len(a_row) != n :
				print("Bad number of coefficients in the row ", i)
				return 1
			a.append(a_row)
	return n,m,c,b,a

	

