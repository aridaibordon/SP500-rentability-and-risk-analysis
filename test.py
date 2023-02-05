import matplotlib.pyplot as plt
import numpy.random as rd


x = range(1, 10)
y = [8 + rd.random() for _ in x]
yerr = [20*rd.random() for _ in x]



plt.errorbar(x, y, yerr=yerr, fmt=".r")

plt.title("Returns for the SP500 over different time periods")
plt.xlabel("Investment time (in weeks)")
plt.ylabel("Yearly return (%)")

plt.savefig("test.png")