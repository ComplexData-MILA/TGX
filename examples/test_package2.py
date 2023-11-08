import tgx


data_path = '/network/scratch/r/razieh.shirzadkhani/'
Plot_path = "./docs/gallery/node_edge"

dataset = tgx.builtin.uci(root = data_path)
G = tgx.Graph(dataset)
G.discretize(intervals=2)
G.count_freq()
tgx.TEA(G, filepath = Plot_path, network_name=dataset.name)
tgx.TET(G, filepath = Plot_path, network_name=dataset.name)
tgx.degree_over_time(G, filepath= Plot_path, network_name=dataset.name)
tgx.nodes_over_time(G, filepath= Plot_path, network_name=dataset.name)