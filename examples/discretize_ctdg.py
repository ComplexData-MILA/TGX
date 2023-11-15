import tgx


# data_path = '/network/scratch/r/razieh.shirzadkhani/'
# Plot_path = ""

dataset = tgx.builtin.uci()
# dataset = tgx.tgb_data("tgbl-wiki")
G = tgx.Graph(dataset)
new_G = G.discretize(intervals=dataset.intervals)
# new_G.count_freq()
tgx.TEA(new_G, network_name=dataset.name)
tgx.TET(new_G, network_name=dataset.name)
# tgx.degree_over_time(new_G, filepath= Plot_path, network_name=dataset.name)
# tgx.nodes_over_time(new_G, filepath= Plot_path, network_name=dataset.name)
# tgx.nodes_and_edges_over_time(new_G, filepath= Plot_path, network_name=dataset.name)
# tgx.get_reoccurrence(new_G)
# tgx.get_surprise(new_G)
# tgx.get_novelty(new_G)
# tgx.get_avg_node_activity(new_G)