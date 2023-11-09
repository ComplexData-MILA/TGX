import tgx
from tgx.io.read import read_edgelist
from tgx.data import builtin

data_path = '/network/scratch/r/razieh.shirzadkhani/'


dataset = builtin.data.uci(root=data_path)
data = read_edgelist(data=dataset, discretize=dataset.discretize, intervals=dataset.intervals)



#! external csv
from tgx.io.read import read_csv
data = read_csv (.....)


#! for built in dataset
from tgx.data.builtin import builtin
data = builtin.uci()


#! for tgx datasets
from tgx.data.tgb import tgb_data
data = tgb_data("tgbl-wiki")


#! visualization

from tgx.viz.TEA import TEA
from tgx.utils.stat import nodes_and_edges_per_ts


TEA(data)

from tgx.utils.stat import nodes_over_time
from tgx.utils.stat import edge_over_time




#! for the future
from tgx.utils.stat import combine
#* combine function takes in a list of plot functions and generate a master figure where each subfigure is specified from the list
combine([nodes_over_time])  # same as node plot
combine([nodes_over_time, edge_over_time])




# Load data into dictionary
G = read_csv(fname)
G.discretize(options)

TEA(G) #create the temp dictionary here by going through the edges
TET(G) #check if the temp dict is created, if not, create it 
nodes_over_time(G)


