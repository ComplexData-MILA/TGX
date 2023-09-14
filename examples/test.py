import tgx
import time
import numpy as np
from tgx.utils.subsampling import graph_subsampling
from tgx.utils.graph_stat import *

start_time = time.time()


# data_path = '/network/scratch/r/razieh.shirzadkhani/'
data_path = './'


dataset = tgx.data.wikipedia(root=data_path)
# dataset = tgx.data.tgb("tgbl-review")
# data = tgx.read_edgelist(data=dataset, discretize=True, intervals=51)
data = tgx.read_edgelist(data=dataset)

G = tgx.Graph(data)

get_avg_e_per_ts(G.edgelist)
get_avg_degree(G.edgelist)
# get_num_timestamps(G.edgelist)  # not needed!
get_num_unique_edges(G.edgelist)
get_reoccurrence(G.edgelist, test_ratio=0.15)
get_surprise(G.edgelist, test_ratio=0.15)
get_avg_node_activity(G.edgelist)

# total_nodes = G.number_of_nodes()
# plot_path = "./examples/plots/"
# new_edges = graph_subsampling(G, random_selection=True, N=1000)
# G.subsampled_graph = G._generate_graph(new_edges)
# tgx.nodes_and_edges_per_ts(G.subsampled_graph, plot_path, network_name=dataset.name)
# tgx.average_degree_per_ts(G.subsampled_graph, total_nodes, plot_path, network_name=dataset.name)


# TEA_path = "./examples/plots/TEA/"

# tgx.TEA(new_edges, TEA_path, network_name=dataset.name)
# TET_path = "./examples/plots/TET/"
# tgx.TET(data, TET_path, network_name=dataset.name)

print("--- Total elapsed time: %s seconds ---" % (time.time() - start_time))


# tgx.nodes_per_timestamp(G.discrite_graph, plot_path, network_name=dataset.name)
# tgx.edges_per_timestamp(G.subsampled_graph, plot_path, network_name=dataset.name)
