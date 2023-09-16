import tgx
import time
import numpy as np
from tgx.utils.graph_utils import subsampling, train_test_split
from tgx.utils.graph_stat import get_reoccurrence, get_surprise, get_index_metrics
from tgb.nodeproppred.dataset import NodePropPredDataset

start_time = time.time()

data_path = '/network/scratch/r/razieh.shirzadkhani/'
dataset = tgx.data.social_evo(root=data_path)
# dataset = tgx.data.tgb("tgbl-wiki")
data = tgx.read_edgelist(data=dataset, discretize=True, intervals=49)

# print(get_index_metrics(train_data, test_data))
# r = get_reoccurrence(data)
# r = get_surprise(data)


# G = tgx.Graph(data)
# plot_path = "./examples/plots/"
# tgx.nodes_and_edges_per_ts(G.discrite_graph, plot_path=plot_path , network_name=dataset.name)
# total_nodes = G.number_of_nodes()
# tgx.average_degree_per_ts(G.discrite_graph, total_nodes, plot_path=plot_path, network_name=dataset.name+'2')

# total_nodes = G.number_of_nodes()
# plot_path = "./examples/plots/"
# n_sampling = 1000
# new_edges = graph_subsampling(G, random_selection=True, N=n_sampling)
# G.subsampled_graph = G._generate_graph(new_edges)
# print(G.number_of_nodes(G.subsampled_graph))
# tgx.nodes_and_edges_per_ts(G.subsampled_graph, plot_path=plot_path, network_name=dataset.name)
# tgx.average_degree_per_ts(G.subsampled_graph, n_sampling, plot_path=plot_path, network_name=dataset.name)


TEA_path = "./examples/plots/TEA/"

tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
TET_path = "./examples/plots/TET/"
tgx.TET(data, filepath = TET_path, network_name=dataset.name)

print("--- Total elapsed time: %s seconds ---" % (time.time() - start_time))


# tgx.nodes_per_timestamp(G.discrite_graph, plot_path, network_name=dataset.name)
# tgx.edges_per_timestamp(G.subsampled_graph, plot_path, network_name=dataset.name)
