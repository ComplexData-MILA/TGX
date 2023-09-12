import tgx
import time
import numpy as np
from tgx.utils.subsampling import graph_subsampling
start_time = time.time()

data_path = '/network/scratch/r/razieh.shirzadkhani/'
dataset = tgx.data.mooc(root=data_path)
data = tgx.read_edgelist(data=dataset, discretize=True, intervals=30)
G = tgx.Graph(data)
plot_path = "./examples/plots/"
tgx.nodes_and_edges_per_ts(G.discrite_graph, plot_path=plot_path , network_name=dataset.name)
# total_nodes = G.number_of_nodes()
# tgx.average_degree_per_ts(G.discrite_graph, total_nodes, plot_path=plot_path, network_name=dataset.name)

# G = tgx.Graph(data)
# total_nodes = G.number_of_nodes()
# plot_path = "./examples/plots/"
# new_edges = graph_subsampling(G, random_selection=True, N=1000)
# G.subsampled_graph = G._generate_graph(new_edges)
# tgx.nodes_and_edges_per_ts(G.subsampled_graph, plot_path, network_name=dataset.name)
# tgx.average_degree_per_ts(G.subsampled_graph, total_nodes, plot_path, network_name=dataset.name)


# TEA_path = "./examples/plots/TEA/"
# tgx.TEA(data, filepath=TEA_path, network_name=dataset.name)
# TET_path = "./examples/plots/TET/"
# tgx.TET(data, filepath=TET_path, network_name=dataset.name)

print("--- %s seconds ---" % (time.time() - start_time))


# tgx.nodes_per_timestamp(G.discrite_graph, plot_path, network_name=dataset.name)
# tgx.edges_per_timestamp(G.subsampled_graph, plot_path, network_name=dataset.name)
