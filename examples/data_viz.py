import tgx
from tgx.utils.graph_utils import list2csv

"""
1. load a dataset
2. load into a graph
3. discretize the graph
4. save the graph back to a csv
"""

#! load the datasets
# dataset = tgx.builtin.uci() #built in datasets 
# data_name = "uci"

data_name = "tgbn-token" #"tgbl-wiki" #"tgbl-review" 
dataset = tgx.tgb_data(data_name) #tgb datasets


time_scale =  "daily" #"hourly"
ctdg = tgx.Graph(dataset)
dtdg = ctdg.discretize(time_scale=time_scale)


#! plotting the statistics, works
tgx.degree_over_time(dtdg, network_name=data_name)
tgx.nodes_over_time(dtdg, network_name=data_name)
tgx.edges_over_time(dtdg, network_name=data_name)
tgx.nodes_and_edges_over_time(dtdg, network_name=data_name)

tgx.TET(dtdg, 
        network_name=data_name, 
        figsize = (9, 5),
        axis_title_font_size = 24,
        ticks_font_size = 24)


tgx.TEA(dtdg, 
        network_name=data_name)



#! compute statistics
test_ratio = 0.15
tgx.get_reoccurrence(dtdg, test_ratio=test_ratio)
tgx.get_surprise(dtdg, test_ratio=test_ratio)

#* these two much faster on dtdgs
tgx.get_avg_node_activity(dtdg)
tgx.get_novelty(dtdg)





# #! statistics to be updated and fixed 
# #TODO 
# tgx.degree_density()
# tgx.connected_components_per_ts()
# tgx.size_connected_components()
# tgx.get_avg_node_engagement()