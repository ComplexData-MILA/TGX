import tgx
import time
import numpy as np
from tgx.utils.subsampling import graph_subsampling
start_time = time.time()

data_path = '/network/scratch/r/razieh.shirzadkhani/'
dataset = tgx.data.uci(root=data_path)
# dataset = tgx.data.tgb("tgbl-review")
data = tgx.read_edgelist(data=dataset, discretize=True, intervals=51)


G = tgx.Graph(data)

total_nodes = G.number_of_nodes()
plot_path = "./examples/plots/"
# print(type(G))
# new_edges = graph_subsampling(G, random=True, N=100)
# G.subsampled_graph = G._generate_graph(new_edges)
# tgx.edges_per_timestamp(G.discrite_graph, plot_path, network_name=dataset.name)
tgx.plot_nodes_edges_per_ts(G.discrite_graph, plot_path, network_name=dataset.name)
# tgx.average_degree(G.discrite_graph, total_nodes, plot_path, network_name=dataset.name)

# tgx.nodes_per_timestamp(G.discrite_graph, plot_path, network_name=dataset.name)


TEA_path = "./examples/plots/TEA/"
# tgx.TEA(data, TEA_path, network_name=dataset.name)
# TET_path = "./examples/plots/TET/"
# TET(data, TET_path, network_name=ntw)

print("--- %s seconds ---" % (time.time() - start_time))


# start_time = time.time()
# data_path = '/network/scratch/r/razieh.shirzadkhani/'
# dataset = tgx.data.mooc(root=data_path)
# data = tgx.read_edgelist(data=dataset)
# TEA_path = "./examples/plots/TEA/"
# tgx.TEA(data, TEA_path, network_name=dataset.name, intervals=30)
# print("--- %s seconds ---" % (time.time() - start_time))
