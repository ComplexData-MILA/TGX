import tgx


data_path = '/network/scratch/r/razieh.shirzadkhani/'
Plot_path = "./examples"

dataset = tgx.builtin.uci(root = data_path)
G = tgx.Graph(dataset)
G.discretize(intervals=dataset.intervals)
G.count_freq()
tgx.TEA(G, filepath = Plot_path, network_name=dataset.name)
tgx.TET(G, filepath = Plot_path, network_name=dataset.name)
tgx.degree_over_time(G, filepath= Plot_path, network_name=dataset.name)
tgx.nodes_over_time(G, filepath= Plot_path, network_name=dataset.name)