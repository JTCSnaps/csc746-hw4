"""

E. Wes Bethel, Copyright (C) 2022

October 2022

Description: This code loads a .csv file and creates a 3-variable plot, and saves it to a file named "myplot.png"

Inputs: the named file "sample_data_3vars.csv"

Outputs: displays a chart with matplotlib

Dependencies: matplotlib, pandas modules

Assumptions: developed and tested using Python version 3.8.8 on macOS 11.6

"""

import pandas as pd
import matplotlib.pyplot as plt

plot_fname = "myplot.png"

fname = "blas_64threads_mflops.csv"
df = pd.read_csv(fname, comment="#")
print(df)

var_names = list(df.columns)

print("var names =", var_names)

# split the df into individual vars
# assumption: column order - 0=problem size, 1=BLAS MFLOP/s, 2=64-thread MFLOP/s

problem_sizes = df[var_names[0]].values.tolist()
blas = df[var_names[1]].values.tolist()
openmp64 = df[var_names[2]].values.tolist()

plt.figure()

plt.title("Serial BLAS vs. 64-Thread OpenMP MFLOP/s")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

plt.plot(blas, "r-o")
plt.plot(openmp64, "b-x")

#plt.xscale("log")
#plt.yscale("log")

plt.xlabel("Problem Size")
plt.ylabel("MFLOP/s")

varNames = [var_names[1], var_names[2]]
plt.legend(varNames, loc="best")

plt.grid(axis='both')

# save the figure before trying to show the plot
plt.savefig(plot_fname, dpi=300)


plt.show()

# EOF
