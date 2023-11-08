from tgx.data.tgb import tgb_data
from tgx.data.builtin import builtin
from tgx.io.read import read_csv
from tgx.classes.graph import *
from tgx.viz.TEA import TEA
from tgx.viz.TET import TET
from tgx.utils.stat import degree_over_time, nodes_over_time


data_path = '/network/scratch/r/razieh.shirzadkhani/'
Plot_path = "./examples"

dataset = builtin.uci(root = data_path)
G = Graph(dataset)
G.discretize(intervals=dataset.intervals)
G.count_freq()
TEA(G, filepath = Plot_path, network_name=dataset.name)
TET(G, filepath = Plot_path, network_name=dataset.name)
degree_over_time(G, filepath= Plot_path, network_name=dataset.name)
nodes_over_time(G, filepath= Plot_path, network_name=dataset.name)