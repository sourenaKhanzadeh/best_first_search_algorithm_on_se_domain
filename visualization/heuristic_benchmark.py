import os
import sys

# add the path to the parent directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import itertools


WA_BENCHMARK_PATH = "../experiments/se_experiments/se_files/se_heuristic_sol.csv"
PLOTS_PATH = "results/plots"

def plot_n_expansions():
    df = pd.read_csv(WA_BENCHMARK_PATH)
    print(df.head())
    x = np.arange(0, 100, 1)

    heuristics = ["zero_n_expansions", "coupling_n_expansions", "cohesion_n_expansions",
    "AddCouplingCohesion_n_expansions", "MaxCouplingCohesion_n_expansions"]
    # plot the number of node expansions
    plt.figure(figsize=(10, 10))
    for h in heuristics:
        sns.lineplot(x=x, y=h, label=f"H = {h}", data=df)
    # log scale
    plt.yscale("log")
    
    plt.xlabel("No of Problems")
    plt.ylabel("Number of Node Expansions")
    plt.title("Number of Node Expansions for Heuristic A*")
    plt.legend()
    plt.savefig(os.path.join(PLOTS_PATH, "n_expansions_heuristic.png"))


def matrex_plot_n_expansions():
    df = pd.read_csv(WA_BENCHMARK_PATH)
    print(df.head())

    heuristics = ["zero_n_expansions", "coupling_n_expansions", "cohesion_n_expansions",
    "AddCouplingCohesion_n_expansions", "MaxCouplingCohesion_n_expansions"]
    len_of_prod = len(list(itertools.product(heuristics, heuristics)))
    print(len_of_prod)
    # make nxm figures side by side
    fig, axs = plt.subplots(5, 5, figsize=(10, 10))
    for i in range(5):
        for j in range(5):
            # get the axes
            ax = axs[i, j]
            # plot the line chart of node expansions vs cost
            for k in range(5):
                sns.lineplot(x=f"{heuristics[i]}", y="{}".format(heuristics[k]), label="H = {}".format(heuristics[k][0:5]), data=df, ax=ax)
            ax.set_xlabel(f"H = {heuristics[i][0:5]}")
            ax.set_ylabel(f"H = {heuristics[j][0:5]}")
            ax.set_title(f"H = {heuristics[i][0:5]} vs H = {heuristics[j][0:5]}")
            ax.legend()
            #make legend tiny
            ax.legend(fontsize='xx-small')
            # tight layout
            plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, "n_expansions_heuristic_matrix.png"))

def main():
    # plot_n_expansions()
    matrex_plot_n_expansions()


if __name__ == "__main__":
    main()