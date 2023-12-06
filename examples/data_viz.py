import tgx
from tgx.utils.graph_utils import list2csv

"""
1. load a dataset
2. load into a graph
3. discretize the graph
4. save the graph back to a csv
"""

#! load the datasets
# dataset = tgx.builtin.uci()

data_name = "tgbl-wiki" #"tgbl-review" 
dataset = tgx.tgb_data(data_name)


ctdg = tgx.Graph(dataset)
# ctdg.save2csv("ctdg")

time_scale = "hourly" #"monthly" #"weekly" #"daily"  #"hourly" #"minutely" 
dtdg, ts_list = ctdg.discretize(time_scale=time_scale, store_unix=True)
print ("discretize to ", time_scale)
print ("there is time gap, ", dtdg.check_time_gap())
list2csv(ts_list, data_name + "_ts" + "_" + time_scale + ".csv")



