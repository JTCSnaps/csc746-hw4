"""

E. Wes Bethel, Copyright (C) 2022

October 2022

Description: This code loads the basic DGEMM runtime-max CSV, calculates thread speedup, and saves it to "myplot.png"

Inputs: the named file "basic-flops-dp-runtime-max.csv"

Outputs: displays a chart with matplotlib

Dependencies: matplotlib, pandas modules

Assumptions: developed and tested using Python version 3.8.8 on macOS 11.6

"""

import pandas as pd
import matplotlib.pyplot as plt

plot_fname = "myplot.png"

fname = "blocked-flops-dp-runtime-max.csv"
df = pd.read_csv(fname, comment="#")
print(df)

required_columns = {"problem_size", "concurrency", "runtime_max_s"}
missing_columns = required_columns.difference(df.columns)
if missing_columns:
    raise ValueError(f"Missing required CSV columns: {sorted(missing_columns)}")

runtime_by_threads = df.pivot(
    index="problem_size", columns="concurrency", values="runtime_max_s"
).sort_index()
thread_counts = [1, 4, 16, 64]
missing_thread_counts = [
    threads for threads in thread_counts if threads not in runtime_by_threads.columns
]
if missing_thread_counts:
    raise ValueError(
        f"CSV is missing runtime data for concurrency levels: {missing_thread_counts}"
    )

problem_sizes = runtime_by_threads.index.tolist()
time_1thread = runtime_by_threads[1]
speedups = {
    threads: (time_1thread / runtime_by_threads[threads]).tolist()
    for threads in thread_counts
}

plt.figure()

plt.title("Blocked DGEMM Thread Speedup")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

plt.plot(speedups[1], "r-o")
plt.plot(speedups[4], "b-x")
plt.plot(speedups[16], "g-^")
plt.plot(speedups[64], "m-s")


plt.xlabel("Problem Size")
plt.ylabel("Speedup")

varNames = ["1 thread", "4 threads", "16 threads", "64 threads"]
plt.legend(varNames, loc="best")

plt.grid(axis='both')

plt.savefig(plot_fname, dpi=300)


plt.show()

# EOF
