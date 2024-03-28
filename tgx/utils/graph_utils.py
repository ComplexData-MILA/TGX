import numpy as np
from typing import Union, Optional

__all__ = ["train_test_split",
           "discretize_edges",
           "subsampling",
           "node_list",
           "is_discretized",
           "frequency_count"]

SEC_IN_MIN = 60
SEC_IN_HOUR = 3600
SEC_IN_DAY = 86400
SEC_IN_WEEK = 86400 * 7
SEC_IN_MONTH = 86400 * 30
SEC_IN_YEAR = 86400 * 365
SEC_IN_BIYEARLY = 86400 * 365 * 2

# helper function to do ceiling divison, i.e. 5/2 = 3
def ceiling_division(n, d):
    q, r = divmod(n, d)
    return q + bool(r)



def discretize_edges(edgelist: dict,
                    time_scale: Union[int,str],
                    store_unix: Optional[bool] = False,
                    freq_weight: Optional[bool] = False) -> list:
    """
    util function for discretizing edgelist, expected timestamp on edges are unixtimestamp
    this func supports discretization of edge timestamp 
    1. by providing the number of intervals (int), it will equally divide the data into that number of intervals. Note that the last bin can have less duration than others.
    2. by providing a time granularity (str), it will divide the data into intervals based on the given granularity, i.e. "hourly", "daily", "weekly", "monthly", "yearly", the starting time of the dataset is consider the start of the first interval
    Parameters:
        edgelist: dict, dictionary of edges
        time_scale: int or str, time interval to discretize the graph
        store_unix: bool, whether to return the converted timestamps in unix format
        freq_weight: bool, whether to weight the edges based on their frequency
    Returns:
        output list: the first item in the list is always the updated edgelist (dict, dictionary of edges with discretized timestamps) and the second item is the converted timestamps in unix format (list) if store_unix is True
    """
    unique_ts = list(edgelist.keys())        
    total_time = unique_ts[-1] - unique_ts[0]

    if time_scale is not None:
        if isinstance(time_scale, int):
            interval_size = total_time // time_scale  #integer timestamp of the bin, discounting any bin that has a smaller duration than others
        elif isinstance(time_scale, str): 
            if time_scale == "minutely":
                interval_size = SEC_IN_MIN
            elif time_scale == "hourly":
                interval_size = SEC_IN_HOUR
            elif time_scale == "daily":
                interval_size = SEC_IN_DAY
            elif time_scale == "weekly":
                interval_size = SEC_IN_WEEK
            elif time_scale == "monthly":
                interval_size = SEC_IN_MONTH
            elif time_scale == "yearly":
                interval_size = SEC_IN_YEAR
            elif time_scale == "biyearly":
                interval_size = SEC_IN_BIYEARLY
        else:
            raise TypeError("Invalid time interval")
    else:
        raise TypeError("Please provide a time interval")
    
    num_time_scale = ceiling_division(total_time, interval_size)    
    print(f'Discretizing data to {num_time_scale} timestamps...')

    updated_edgelist = {}

    if (store_unix):
        unix_dict = []
        start_time = int(unique_ts[0])

    for ts, edges_list in edgelist.items():
        bin_ts = ceiling_division(ts, interval_size)  #will correctly put edges into the last bin

        for edge in edges_list:
            if bin_ts not in updated_edgelist:
                updated_edgelist[bin_ts] = {edge: 1}
            else:
                if (not freq_weight):
                    updated_edgelist[bin_ts][edge] = 1
                else:
                    if (edge in updated_edgelist[bin_ts]):
                        updated_edgelist[bin_ts][edge] += 1
                    else:
                        updated_edgelist[bin_ts][edge] = 1
        
        if (store_unix):
            #! should use bin_ts here
            unix_ts = start_time + bin_ts * interval_size
            # unix_ts = start_time + int(ts // interval_size) * interval_size #round to the nearest start time
            unix_ts = int(unix_ts)
            unix_dict.extend([unix_ts] * len(edges_list))
    
    output = [updated_edgelist]
    if (store_unix):
        output.append(unix_dict)
    return output

def subsampling(graph: object, 
                node_list: Optional[list] = [], 
                selection_strategy: str = "random", 
                N: Optional[int] = 100
                ) -> dict:
    """
    Subsampling a part of graph by only monitoring the contacts from specific nodes' list

    Parameters:
        graph: graph object
        node_list: list, a set of nodes to extract their contacts from the graph
        selection_strategy: str, currently supports random sampling
        N: int, number of nodes to be randomly sampled from graph
    
    Returns:
        new_edgelist: dict, a dictionary of edges corresponding to nodes in the node_list
    """
    print("Generate graph subsample...")
    edgelist = graph.data
    nodes = graph.nodes_list()

    if (len(node_list) == 0): #decide on selection strategy if nodelist not provided
        if (selection_strategy == "random"):
            node_list = list(np.random.choice(nodes, size = N, replace = False))
        else:
            raise ValueError("Selection strategy not supported", selection_strategy)

    new_edgelist = {}
    for t, edge_data in edgelist.items():
                for (u,v), f in edge_data.items():
                    if u in node_list or v in node_list:
                        if t not in new_edgelist:
                            new_edgelist[t] = {}
                            new_edgelist[t][(u, v)] = f
                        else:
                            new_edgelist[t][(u, v)] = f
    return new_edgelist

def frequency_count(edgelist: dict):
    new_edgelist = {}

    for t, edges_list in edgelist.items():
        for edge in edges_list:
            (u, v) = edge

            # Check if this is the first edge occurning in this timestamp
            if t not in new_edgelist: 
                new_edgelist[t] = {}
                new_edgelist[t][(u, v)] = 1
                
            else:
                if (u, v) not in new_edgelist[t]:
                    new_edgelist[t][(u, v)] = 1 # If the edge was not occured in this timestamp before
                else:
                    new_edgelist[t][(u, v)] += 1 
    
    return new_edgelist

def node_list(dict_edgelist: dict) -> list:

    """
    create a list of nodes from edgelist dictionary
    """
    node_list = {}
    for _, edge_data in dict_edgelist.items():
        for (u,v), _ in edge_data.items():
            if u not in node_list:
                node_list[u] = 1
            if v not in node_list:
                node_list[v] = 1
    return list(node_list.keys())


def train_test_split(data : dict, 
                     val : bool = False,
                     ratio : list = [85, 15]) -> dict:
    """
    Generate train/test split for the data

    Parameters:
        data:dictionary of data
        val: whether we want to have a validation split as well
        ratio: list indication the ratio of the data in split. Sum of the list components should be 100.

    Returns:
        two (train/test) or three (train/val/test) data dictionaries
    """
    sum = 0
    for i in ratio:
        sum += i
    if sum != 100:
        raise ValueError("invalid train/test split ratio. Sum of the ratios should be 100.")
    
    if val and len(ratio) != 3:
        raise Exception("Provide train/val/test ratio")
    elif not val and len(ratio) == 3:
        print("Warning! Data is being splitted to train and test only!")
    
    data_len = len(data)
    train_split = int(data_len * ratio[0] / 100)
    train_data = {k: v for k, v in data.items() if k < train_split}
    if val:
        val_split = int(data_len * ratio[1] / 100) + train_split
        val_data = {k: v for k, v in data.items() if train_split <= k < val_split}
        test_data = {k: v for k, v in data.items() if val_split <= k <= data_len}
        return train_data, val_data, test_data
    
    else:
        test_data = {k: v for k, v in data.items() if train_split <= k <= data_len}
        return train_data, test_data
    

def is_discretized(edgelist: Optional[dict],
                   max_timestamps: Optional[int] = 10000) -> bool:
    r"""
    Check if an edgelist is discretized or not.
    """
    timestamps = list(edgelist.keys())
    discretized = True
    if len(timestamps) > max_timestamps:
        discretized = False
    
    return discretized

def list2csv(lst: list,
             fname: str,
             delimiter: str = ",",
             fmt: str = '%i'):
    out_list = np.array(lst)
    np.savetxt(fname, out_list, delimiter=delimiter,  fmt=fmt)




# def edgelist_discritizer(edgelist: dict,
#                          time_scale: Union[str, int]):
#     """
#     util function for discretizing edgelist, expected timestamp on edges are unixtimestamp
#     this func supports discretization in two different ways
#     1. by providing the number of intervals (int), it will equally divide the data into that number of intervals. Note that the last bin can have less duration than others.
#     2. by providing a time granularity (str), it will divide the data into intervals based on the given granularity, i.e. "hourly", "daily", "weekly", "monthly", "yearly"
#     In the second way however, the intervals will be based on utc timezone (dividing into days, hours this way) thus both first bin and last bin can have last duration than others.

#     Parameters:
#         edgelist: dict, dictionary of edges
#         time_scale: str or int, time interval to discretize the graph
#     Returns:
#         updated_edgelist: dict, dictionary of edges with discretized timestamps
#     """
    
#     unique_ts = list(edgelist.keys())
        
#     total_time = unique_ts[-1] - unique_ts[0]
#     if time_scale is not None:
#         if isinstance(time_scale, str):
#             if time_scale == "hourly":
#                 interval_size = SEC_IN_HOUR
#             elif time_scale == "daily":
#                 interval_size = SEC_IN_DAY
#             elif time_scale == "weekly":
#                 interval_size = SEC_IN_WEEK
#             elif time_scale == "monthly":
#                 interval_size = SEC_IN_MONTH
#             elif time_scale == "yearly":
#                 interval_size = SEC_IN_YEAR
#         elif isinstance(time_scale, int):
#             interval_size = int(total_time / (time_scale))
#         else:
#             raise TypeError("Invalid time interval")
#     else:
#         raise TypeError("Please provide a time interval")
#     num_time_scale = int(total_time/interval_size)
#     print(f'Discretizing data to {num_time_scale} timestamps...')
#     # if num_time_scale == 0:
#     #     print("Warning! Only one timestamp exist in the data.")

#     updated_edgelist = {}
#     for ts, edges_list in edgelist.items():
#         bin_ts = int(ts / interval_size)
#         if bin_ts >= num_time_scale:
#             bin_ts -= 1

#         for edge in edges_list:
#             if bin_ts not in updated_edgelist:
#                 updated_edgelist[bin_ts] = []
#             updated_edgelist[bin_ts].append(edge)
#     print("Discretization Done..!")
#     return updated_edgelist
