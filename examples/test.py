import tgx
import time
import numpy as np
# from tgx.utils.graph_utils import subsampling, train_test_split, edgelist_discritizer
from tgx.utils.graph_stat import get_novelty, get_avg_node_activity, get_reoccurrence, get_surprise, get_avg_node_engagement
from tgx.utils.plotting_utils import plot_for_snapshots
data_path = '/network/scratch/r/razieh.shirzadkhani/'
TEA_path = "./docs/gallery/TEA/"
TET_path = "./docs/gallery/TET/"

# dataset = tgx.data.reddit(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)


# dataset = tgx.data.uci(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.mooc(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.lastfm(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.canparl(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.contacts(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset= tgx.data.enron(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.flights(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.unvote(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.uslegis(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# dataset = tgx.data.social_evo(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# print(dataset.name)
# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)



# data_name = ["tgbl-comment"]

# for name in data_name:
#     dataset = tgx.data.tgb(name)
#     data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=12)
#     print(dataset.name)
#     tgx.TEA(data, filepath = TEA_path, network_name=dataset.name)
#     tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# node_engagement = get_avg_node_engagement(data)
# plot_path = "./examples/plots/"
# filename = f"{dataset.name}_ave_node_engagement_per_ts"
# plot_for_snapshots(node_engagement, filename, "node engagement", plot_path=plot_path)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset = tgx.data.lastfm(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset = tgx.data.mooc(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset = tgx.data.canparl(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset = tgx.data.contacts(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset= tgx.data.enron(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset = tgx.data.flights(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)

# dataset = tgx.data.unvote(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset = tgx.data.uslegis(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# dataset = tgx.data.social_evo(root=data_path)
# data = tgx.read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)
# get_avg_node_activity(data)
# print(dataset.name)
# print(dataset.name)
# data = tgx.read_edgelist(data=dataset, discretize=True, intervals=dataset.intervals)
# get_novelty(data)

# total_nodes = G.number_of_nodes()
# plot_path = "./examples/plots/"
# n_sampling = 1000
# new_edges = subsampling(G, random_selection=True, N=n_sampling)
# new_edges = edgelist_discritizer(new_edges, time_interval=50)
# G.subsampled_graph = G._generate_graph(new_edges)
# print(G.number_of_nodes(G.subsampled_graph))
# tgx.nodes_and_edges_per_ts(G.subsampled_graph, plot_path=plot_path, network_name=dataset.name)
# tgx.average_degree_per_ts(G.subsampled_graph, n_sampling, plot_path=plot_path, network_name=dataset.name)


# TEA_path = "./examples/plots/TEA/1"

# tgx.TEA(data, filepath = TEA_path, network_name=dataset.name+'disc')
# tgx.TET(data, filepath = TET_path, network_name=dataset.name)

# print("--- Total elapsed time: %s seconds ---" % (time.time() - start_time))


