import os
import sys

# add the path to the parent directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import itertools


WA_BENCHMARK_PATH = "../experiments/se_experiments/se_files/se_wa_sol.csv"
PLOTS_PATH = "results/plots"

def plot_n_expansions():
    df = pd.read_csv(WA_BENCHMARK_PATH)
    print(df.head())
    x = np.arange(0, 100, 1)

    # plot the number of node expansions
    plt.figure(figsize=(10, 10))
    sns.lineplot(x=x, y="1_n_expansions", label="W = 1", data=df)
    sns.lineplot(x=x, y="5_n_expansions", label="W = 5", data=df)
    sns.lineplot(x=x, y="10_n_expansions", label="W = 10", data=df)
    sns.lineplot(x=x, y="25_n_expansions", label="W = 25", data=df)
    sns.lineplot(x=x, y="50_n_expansions", label="W = 50", data=df)
    # log scale
    plt.yscale("log")
    
    plt.xlabel("No of Problems")
    plt.ylabel("Number of Node Expansions")
    plt.title("Number of Node Expansions for WA*")
    plt.legend()
    plt.savefig(os.path.join(PLOTS_PATH, "n_expansions_wa.png"))


def plot_scatter_n_expansions():
    df = pd.read_csv(WA_BENCHMARK_PATH)
    print(df.head())

    n_of_nodes = [1, 5, 10, 25, 50]
    len_of_prod = len(list(itertools.product(n_of_nodes, n_of_nodes)))
    print(len_of_prod)
    # make nxm figures side by side
    fig, axs = plt.subplots(5, 1, figsize=(10, 10))
    for i in range(5):
        for j in range(1):
            # get the axes
            ax = axs[i]
            # plot the line chart of node expansions vs cost
            for k in range(5):
                sns.lineplot(x=f"{n_of_nodes[i]}_n_expansions", y="{}_n_expansions".format(n_of_nodes[k]), label="W = {}".format(n_of_nodes[k]), data=df, ax=ax)
            ax.set_xlabel(f"W = {n_of_nodes[i]}")
            ax.set_ylabel(f"W = {n_of_nodes[j]}")
            ax.set_title(f"W = {n_of_nodes[i]} vs W = {n_of_nodes[j]}")
            ax.legend()
            #make legend tiny
            ax.legend(fontsize='xx-small')
            # tight layout
            plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, "matrix_n_expansions_wa_2.png"))
    # plot the number of node expansions
    
    # plt.figure(figsize=(10, 10))
    # sns.lineplot(x="1_n_expansions", y="1_n_expansions", label="W = 1", data=df)
    # sns.lineplot(x="1_n_expansions", y="5_n_expansions", label="W = 5", data=df)
    # sns.lineplot(x="1_n_expansions", y="10_n_expansions", label="W = 10", data=df)
    # sns.lineplot(x="1_n_expansions", y="25_n_expansions", label="W = 25", data=df)
    # sns.lineplot(x="1_n_expansions", y="50_n_expansions", label="W = 50", data=df)

    # plt.xlabel("w = 1 No of Node Expansions")
    # plt.ylabel("Number of Node Expansions")
    # plt.title("Number of Node Expansions for WA*")
    # plt.legend()
    # plt.savefig(os.path.join(PLOTS_PATH, "scatter_n_expansions_wa.png"))

def main():
    # plot_n_expansions()
    plot_scatter_n_expansions()


if __name__ == "__main__":
    main()