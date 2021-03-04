from fractions import Fraction
import argparse
import copy
import numpy as np

import parseur
import verif

def variable(n):
	return "x_"+str(n+1)

class Lp:
	def __init__(self, *args):
		# basic initialization
		self.n = args[0]
		self.m = args[1]
		self.objfun = args[2]
		self.b = args[3]
		self.a = args[4]
		self.result = 0
		self.row_size = self.m + self.n # easier to do the pivot

		# the slack variable is n + k for the k eme constraints
		# we add m zeros to the objective function
		self.objfun += [0]*self.m
		# we add the identity martrix to A
		for i in range(self.m):
			row = [0]*self.m
			row[i] = 1 
			self.a[i] += row

		self.basic = [False]*self.n + [True]*self.m
		# this slack variable is associated to the k eme constraints
		self.associated = [i for i in range(self.n, self.n + self.m)]
		self.true_objfun = [] # useful for the phase I : keep the original objfun
		self.true_result = 0
		self.phaseI = False # useful to decide if we have to update true_objfun



	def print(self):
		# Print the associated tableau
		def print_row(l):
			for x in l:
				print('{!s:9}'.format(x), end = "")
		print_row(self.objfun)
		print (" | ", end="")
		print(self.result)
		print("---------"*self.row_size)
		for i in range(len(self.b)):
			print_row(self.a[i])
			print (" | ", end="")
			print(self.b[i])
		print()

	def presentation(self):
		# print the presentation of the problem
		print("Maximize ", end = " ")
		objective = ""
		for i in range(self.n):
			if i != 0 and self.objfun[i]>0:
				print("+", end = "")
			print(self.objfun[i], end = "")
			print(variable(i), end = " ")
		print()
		print("Such that :")
		for i in range(self.m) :
			for j in range(self.n) :
				print(self.a[i][j], end = "")
				print(variable(j), end = " ")
				if j != self.n - 1:
					if self.a[i][j+1]>=0:
						print("+ ", end="")
			print(" <= ", end = "")
			print(self.b[i])
		for i in range(self.n):
			print(variable(i), end=" ")
		print("are non-negative")



	def pivot(self, entering, leaving, row):
		# normalize the row of the pivot
		norm = self.a[row][entering]
		for j in range(self.row_size):
			self.a[row][j] /= norm 
		self.b[row]/= norm

		# pivot to have the identity matrix for basic variable
		for i in range(self.m) :
			if i == row:
				continue
			for j in range(self.row_size):
				if j == entering :
					continue
				self.a[i][j] -= self.a[i][entering]*self.a[row][j]
			self.b[i] -= self.a[i][entering]*self.b[row] 
			self.a[i][entering]=Fraction()

		# same pivot operation for the objective function and the result
		for j in range(self.row_size):
			if j == entering:
				continue
			self.objfun[j] -= self.objfun[entering]*self.a[row][j]
		self.result -= self.objfun[entering]*self.b[row]
		self.objfun[entering] = Fraction()

		# same for the true objective function in phase I
		if self.phaseI : 
			for j in range(self.row_size):
				if j == entering:
					continue
				self.true_objfun[j] -= self.true_objfun[entering]*self.a[row][j]
			self.true_result -= self.true_objfun[entering]*self.b[row]
			self.true_objfun[entering] = Fraction()

		# update the set of basic variables
		self.basic[entering] = True
		self.basic[leaving] = False

	def infinite(self):
		# decide if there exist a column with the objective function > 0 and the column negative
		for i in range(self.row_size):
			if self.objfun[i] > 0:
				negative = True
				for j in range(self.m):
					if self.a[j][i] > 0:
						negative = False
						break
				if negative :
					return True
		return False

	def value_associated(self,ind):
		# return the value of a variable for the tableau it it is in the basis, and -1 otherwise
		row = -1
		for i in range(self.m):
			if self.associated[i] == ind :
				return self.b[i]
		return 0

	def row_associated(self,ind):
		# retrun the row associated to the variable
		for i in range(self.m):
			if self.associated[i]==ind :
				return i



def choose_entering(tb, method):
	# return the leaving variable, or -1 if all variables are negative -> end of the algo
	if method == "Bland":
		# we choose the first element with a positve value in the objective function
		for i in range(tb.row_size):
			if tb.objfun[i] > 0 and tb.basic[i] == False:
				return i
		return -1

	if method == "maxcoef":
		cand = -1
		local = -1
		for i in range(tb.row_size):
			if tb.objfun[i] > local and tb.objfun[i]>0:
				cand = i
				local = tb.objfun[i]
		return cand

	if method == "myrule":
		# random but with a better probability
		proba = []
		candidates = []
		sum_proba = 0
		for i in range(tb.row_size):
			if tb.objfun[i]>0:
				candidates.append(i)
				proba.append(tb.objfun[i])
				sum_proba += tb.objfun[i]
		if len(candidates)>0:
			probi = np.array(proba, dtype = float)/float(sum_proba)
			return np.random.choice(candidates, p = probi)
		else :
			return -1

	if method == "random":
		# we chose at random in the possible candidates
		candidates = []
		for i in range(tb.row_size):
			if tb.objfun[i]>0:
				candidates.append(i)
		if len(candidates)>0:
			return np.random.choice(candidates)
		else:
			return -1





def choose_leaving(tb, entering):
	# we calculate the ratio for each row : ratio of entry in solution column and entry in pivot column
	ratio = [-1] * tb.m
	for i in range(tb.m):
		if tb.a[i][entering]==0 or (tb.a[i][entering]<0 and tb.b[i]==0) : #no condition on the entering variable for this row
			continue
		ratio[i] = tb.b[i] / tb.a[i][entering]
	# we select the row we the minimum positive ratio
	row = -1
	best_ratio = -1
	for i in range(tb.m):
		if ratio[i]>=0 and row == -1:
			best_ratio = ratio[i]
			row =i
		elif ratio[i]>=0 and best_ratio>ratio[i]:
			best_ratio = ratio[i]
			row = i
	# we find the corresponding leaving variable of the row
	leaving = tb.associated[row]
	tb.associated[row] = entering
	# update the association

	#non-basic variable with smallest non-negative ratio is departing variable, and
	# corresponding row is pivot row
	return leaving, row



def one_step(lp, method, verbose):
	# a step of the simplex
	a = choose_entering(lp, method = method)
	if a == -1:
		return False
	b, row = choose_leaving(lp, a)
	if verbose:
		print("The entering variable is ", a)
		print("The leaving variable is ", b)
	lp.pivot(a,b,row)
	if verbose : 
		lp.print()
	return True

def solving(mylp, method, verbose):
	number_pivot = 0
	rotation = True
	unbounded = False
	bornesup = mylp.row_size ** 2
	while rotation:
		#if number_pivot == bornesup :
		#	method = "Bland"
		if mylp.infinite():
			unbounded = True
			break
		rotation = one_step(mylp, method, verbose)

		number_pivot+=1
	return unbounded, number_pivot-1

def final_result(mylp, method, number_pivot, unbounded):
	if unbounded :
		print("The solution is unbounded")
	else :
		print("An optimal solution is: ")
		for i in range(mylp.n):
			print(variable(i), " = ", mylp.value_associated(i), " ")
		print("The objective value for this solution is: ", - mylp.result)
		print("The number of pivot is: ", number_pivot)
		print("The pivot rule used: ", method)


def simplex(input_file, method, verbose = True, verification = False):
	# initial printing
	print("The input linear program is:")
	print()
	n,m,c,b,a = parseur.lp_parse(input_file)

	if verification:
		c_forverfi = c.copy()
		b_forverif = b.copy()
		a_forverif = []
		for i in range(m):
			a_forverif.append(a[i].copy())

	mylp = Lp(n,m,c,b,a)
	mylp.presentation()

	negatif = False
	for x in mylp.b :
		if x < 0 :
			negatif = True

	if not negatif :
		if verbose :
			print("The initial tableau is:")
			mylp.print()

		# iteration
		unbounded, number_pivot = solving(mylp, method, verbose)

		# final result
		final_result(mylp, method, number_pivot, unbounded)
		
		
	else :
		if verbose:
			print("We have to use Phase I/II method")
			print("Phase I")
		# we create the A and b modified, with two phases
		artificial_lp = Lp(0,0,[],[],[])
		# first phase : detection of problematic rows
		modified = [False]*m
		ajout = 0
		constraints = []
		for i in range(m):
			if b[i]<0 :
				modified[i] = True
				constraints.append(-b[i])
				ajout += 1
			else :
				constraints.append(b[i])
		artificial_lp.b = constraints
		# second phase : we inverse those row, and completed the matrix
		cran = 0
		artificial_lp.a = []
		for i in range(m):
			row = []
			if modified[i]:
				for k in range(n) :
					row.append(-a[i][k])
				row += [0]*(m+ajout)
				row[n+i]=-1
				row[n+m+cran]=1
				cran+=1
			else :
				for k in range(n) :
					row.append(a[i][k])
				row += [0]*(m+ajout)
				row[n+i]=1
			artificial_lp.a.append(row)

		artificial_lp.row_size = n+m+ajout
		basich = [False]*(n+m) + [True]*ajout
		for i in range(m):
			# n + i if i non modified, and cran i otherwise
			if artificial_lp.a[i][i+n]==1 :
				basich[i+n] = True
		artificial_lp.basic = basich		
		assoc = []
		cran = 0
		for i in range(m):
			if artificial_lp.a[i][i+n]==1:
				assoc.append(n+i)
			else :
				assoc.append(n+m+cran)
				cran += 1
		artificial_lp.associated = assoc
		artificial_lp.result = 0
		c = [0]*(n+m)+[-1]*ajout
		artificial_lp.objfun = c

		# we keep the initial oblective function
		artificial_lp.m = mylp.m
		obj = mylp.objfun[:n]+(m+ajout)*[0]
		artificial_lp.true_objfun = obj
		artificial_lp.true_result = 0
		artificial_lp.phaseI = True
		if verbose:
			artificial_lp.print()

		# we add the rows corresponding to artificial variables to the objective function
		for i in range(m):
			if artificial_lp.objfun[artificial_lp.associated[i]] == -1:
				# print(i)
				for j in range(artificial_lp.row_size):
					artificial_lp.objfun[j]+=artificial_lp.a[i][j]
				artificial_lp.result += artificial_lp.b[i]
		if verbose :
			artificial_lp.print()

		unbounded, number_pivot1 = solving(artificial_lp, method, verbose)




		if artificial_lp.result != 0:
			number_pivot = number_pivot1 # just to have number pivot defined in this case for the verification
			print("The problem is unfeasible.")
		else :
			# check degeneracy :
			real_variables = artificial_lp.row_size - ajout
			for i in range(ajout):
				if artificial_lp.basic[real_variables+i]: # there is a problem of degeneracy !
					row = artificial_lp.row_associated(real_variables+i)
					for j in range(real_variables):
						if artificial_lp.a[row][j] != 0 :
							artificial_lp.pivot(j, real_variables, row)
							break
			if verbose :
				artificial_lp.print()

			if verbose :
				print("We have a feasible solution in ", number_pivot1, " steps")
				for i in range(mylp.n):
					print(variable(i), " = ", mylp.value_associated(i), " ")
				print("So now we do phase II")

			for i in range(mylp.m):
				mylp.a[i] = artificial_lp.a[i][:mylp.row_size]
			mylp.b = artificial_lp.b
			mylp.basic = artificial_lp.basic
			mylp.associated = artificial_lp.associated
			mylp.objfun = artificial_lp.true_objfun[:mylp.row_size]
			mylp.result = artificial_lp.true_result

			if verbose :
				mylp.print()

			# solving the true Lp
			unbounded, number_pivot = solving(mylp, method, verbose)
			number_pivot += number_pivot1 # add the pivot used in phase I
			final_result(mylp, method, number_pivot, unbounded)

	if verification:
		return number_pivot, verif.comparaison(c_forverfi, b_forverif, a_forverif, mylp.result)



# simplex("custom_molder.dat", "Bland", verbose = True, verification = True)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose",action = "store_true", help = "print the tabeau at each step and the entering and leaving variables")
	parser.add_argument("file", help = "input data")
	parser.add_argument("-c","--check",  action = "store_true", help="run the simplex method of python and compare the result")
	parser.add_argument("--method",default = "Bland", help = "Select the method : by default Bland, otherwise maxcoef or random or myrule")

	args = parser.parse_args()
	method_dict = {"Bland", "maxcoef", "random", "myrule"}
	if args.method in method_dict:
		simplex(args.file, args.method, verbose = args.verbose, verification = args.check)
	else :
		print("This method is not available")



