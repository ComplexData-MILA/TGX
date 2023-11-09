import tgx


data_path = '/network/scratch/r/razieh.shirzadkhani/'
Plot_path = "./docs/gallery/node_edge"

dataset = tgx.builtin.reddit(root = data_path)
G = tgx.Graph(dataset)
new_G = G.discretize(intervals=dataset.intervals)
# new_G.count_freq()
# tgx.TEA(G, filepath = Plot_path, network_name=dataset.name)
# tgx.TET(G, filepath = Plot_path, network_name=dataset.name)
# tgx.degree_over_time(new_G, filepath= Plot_path, network_name=dataset.name)
tgx.nodes_and_edges_over_time(new_G, filepath= Plot_path, network_name=dataset.name)