import random
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--variables",type = int, help = "number of variables of the simplex")
parser.add_argument("-m", "--constraints", type = int, help = "number of constraints of the simplex")

args = parser.parse_args()
n = args.variables
m = args.constraints

c = []
b = []
for i in range(n):
	c.append(random.randint(0,20))

for i in range(m): 
	b.append(random.randint(10, 20))

a = []
for i in range(m):
	row = []
	for j in range(n):
		row.append(random.randint(0,10))
	a.append(row)


def affiche(l):
	s = ""
	for i in range(len(l)):
		s += str(l[i]) + " "
	print(s)

# print the input of the created simplex
print(n)
print(m)
affiche(c)
affiche(b)
for i in range(m):
	affiche(a[i])



