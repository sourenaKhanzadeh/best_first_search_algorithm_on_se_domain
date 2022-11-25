import os
import sys

# add the path to the parent directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


ALG_BENCHMARK_PATH = "../experiments/se_experiments/se_files/alg_benchmarks"
PLOTS_PATH = "results/plots"

__ALL__FILES__ = []

for file in os.listdir(ALG_BENCHMARK_PATH):
    if file.endswith(".csv"):
        __ALL__FILES__.append(file)

def plot_cost_vs_expansions():
    # plot all the files in one plot
    dfs = [os.path.join(ALG_BENCHMARK_PATH, file) for file in __ALL__FILES__]
    dfs = [pd.read_csv(file) for file in dfs]
    df = pd.concat(dfs, ignore_index=True)
    print(df.head())

    cols = ["AStar_n_expansions", "IDAStar_n_expansions", "GBFS_n_expansions", "AStar_cost", "IDAStar_cost", "GBFS_cost"]
    # plot the line chart
    sns.set(style="darkgrid")
    
    # plot the number of node expansions
    plt.figure(figsize=(10, 10))
    
    for col1, col2 in zip(cols[3:], cols[:3]):
        sns.lineplot(x=col1, y=col2, label=col1.replace("_cost", ""), data=df)
    

    plt.xlabel("Cost")
    plt.ylabel("Number of Node Expansions")
    plt.title("Cost vs Number of Node Expansions")
    plt.legend()
    plt.savefig(os.path.join(PLOTS_PATH, "cost_vs_n_expansions_algs.png"))

def plot_matrix_of_expansions_vs_costs():
    dfss = [os.path.join(ALG_BENCHMARK_PATH, file) for file in __ALL__FILES__]
    dfs = [pd.read_csv(file) for file in dfss]

    # make many figures side by side
    fig, axs = plt.subplots(len(dfs)//4, len(dfs)//5, figsize=(10, 10))

    for i in range(5):
        for j in range(4):
            df = dfs[i*4 + j]
            # get the axes
            ax = axs[i, j]
            # plot the line chart of node expansions vs cost
            sns.lineplot(x="AStar_cost", y="AStar_n_expansions", label="A*", data=df, ax=ax)
            sns.lineplot(x="IDAStar_cost", y="IDAStar_n_expansions", label="IDA*", data=df, ax=ax)
            sns.lineplot(x="GBFS_cost", y="GBFS_n_expansions", label="GBFS", data=df, ax=ax)
            ax.set_xlabel("Cost")
            ax.set_ylabel("N_Expansions")
            ax.legend(prop={'size': 6})
            
            # make scale log
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_title(dfss[i*4 + j].split("/")[-1][:8])
    # give more space between the plots
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, "matrix_of_expansions_vs_costs.png"))

def main():
    # plot_cost_vs_expansions()
    plot_matrix_of_expansions_vs_costs()

if __name__ == "__main__":
    main()