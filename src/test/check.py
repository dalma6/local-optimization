# This program checks if our optimizator gives the correct result and measures the time difference between the optimized and non-optimized code.

import time

start_nonopt = time.time()
# non_optimized = the non optimized program
end_nonopt = time.time()

start_opt = time.time()
# optimized = the optimized program
end_opt = time.time()

if non_optimized != optimized:
	print "The program may be optimized, but it does not give the correct result!"
	exit()
	
time_nonopt = end_nonopt - start_nonopt
time_opt = end_opt - start_opt
if time_opt > time_nonopt:
	print "Congratulations! You've optimized a 3-address-code program!"
elif time_opt == time_nonopt:
	print "Nice try, but the execution time of your so-called optimized program is the as the one of the original program."
else:
	print "This doesn't look vey well. You've managed to slow down the program even more... You need to put some serious thought in your work."