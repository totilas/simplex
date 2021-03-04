## Simplex implementation

I have implemented the simplex algorithm in Python3. I use numpy, random, Fraction and scipy because of an option that checks if the result is the same than the one found by Python implementation.

### How to run an instance

to run it on a file, you have to write:
	python3 simplex.py path_of_the_file
In this case, it is the Bland Rule that will be use.

There are several options :
- *verbose mode* : add -v and the tableau is drawn at each step, and there is the entering and the leaving variables.
- *checking mode* : add -c and the python method for the simplex is run and the solutions compared : if they are identical we add "Solution checked at the end of the output"
- *method* : four rules have been implemented :
	-  'Bland' : by default we use Bland rule but we can use other pivot rules. 
	-  'maxcoef' : As demanded, there is the rule 'maxcoef' that select the variable which has the maximum coefficient in the objective function.
	- 'random' : The random rule has been implemented, and used for statistics.
	- 'myrule' : a pondered random. I choose a random rule but with a more relevant distribution that the uniform one. Indeed, we
see that maxcoef is often quicker that Bland rule, so we want to keep this efficacy, but without
the risk of cycling. That’s why we give higher probability to variable with big coefficient, but
keep positive probability for every possible entering variable, so we finish with probability one.
We could have tried other distributions with the same idea, such as Boltzmann distribution.
You can use the help to remember those options.


### format of the input

The simplex solves max sum_1<= i <= n c_i x_i
subject to sum_1<= j <= n a_ji x_i <= b_j
and x_i >= 0

n
m
c1 c2 ... cn
b1 b2 ... bm
a11 a12 ... a1n
a21 a22 ... a2n
...
am1 am2 ... amn


### Organization

#### Simplex

'simplex.py' contains the implementation of the simplex. We define a class Lp for a simplex tableau, with several methods :
	- print : to print the tableau
	- presentation : to print the linear problem
	- pivot : the pivot operation
	- infinite : to detect if the solution is unbounded
	- value_associated : the value of a variable of the basis

Then we define the choices for the pivot with :
	- choose_entering : choice of the entering variable
	- choose_leaving : choice of the leaving variable
	- one_step : do an iteration of the simplex algorithm

So we can define :
	- solving : realize the simplex with b > 0
	- final_result : present the result of the simplex
	- simplex : solve the input problem


#### Parseur

'parseur.py' deals with the output thanks to Python module Fractions.

#### Verification

'verif.py' allows us to check the result of the program by comparing it to Python implementation result. If the option is used, we copy the result of the parsinf, we convert it in float and use scipy.optimize.linprog.

#### Generators

'generator.py' takes m and n as input, and print a linear problem in the good shape, with n variables and m constraints. We only use whole numbers for simplicity reason, with coefficients from -100 to 100 for the objective function, and -20 to 20 for the coefficients (to keep a good proportion of feasible problems). We only use B>0 to avoid a a difference between cases with phase I/II method and the others.

'test_gen.py' is used to generate the instances for statistics. It was ruled with different parameters, (look at the comments) to generate the graph found in the discussion file

'kleeminty.py' and 'km_bis.py' generates instances with exponential time for maxcoef rule.






