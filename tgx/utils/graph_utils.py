import numpy as np
from typing import Union, Optional

__all__ = ["train_test_split",
           "edgelist_discritizer",
           "subsampling",
           "node_list",
           "is_discretized"]


def edgelist_discritizer(edgelist,
                         unique_ts = None,
                         time_interval = None,
                         max_intervals = 200):
    if unique_ts is None:
        unique_ts = list(edgelist.keys())
        
    total_time = unique_ts[-1] - unique_ts[0]
    if time_interval is not None:
        if isinstance(time_interval, str):
            if time_interval == "daily":
                interval_size = 86400
            elif time_interval == "weekly":
                interval_size = 86400 * 7
            elif time_interval == "monthly":
                interval_size = 86400 * 30
            elif time_interval == "yearly":
                interval_size = 86400* 365
            if int(total_time / interval_size) > max_intervals:
                user_input = input("Too many timestamps, discretizing data to 200 timestamps, do you want to proceed?(y/n): ")
                if user_input.lower() == 'n':
                    print('Cannot proceed to TEA and TET plot')
                    exit()
                else:
                    interval_size = max_intervals
        elif isinstance(time_interval, int):
            if time_interval > max_intervals:
                raise ValueError(f"The maximum number of time intervals is {max_intervals}.")
            else:
                interval_size = int(total_time / (time_interval))
                
        else:
            raise TypeError("Invalid time interval")
    else:
        user_input = input(f"discretizing data to {max_intervals} timestamps, do you want to proceed?(y/n): ")
        if user_input.lower() == 'n':
            print('Cannot proceed to TEA and TET plot')
            exit()
        else:
            interval_size = int(total_time / 100)
    num_intervals = int(total_time/interval_size)
    print(f'Discretizing data to {num_intervals} timestamps...')
    if num_intervals == 0:
        print("Warning! Only one timestamp exist in the data.")
    updated_edgelist = {}
    new_ts = {}
    curr_t = 0
    for ts, edge_data in edgelist.items():
        bin_ts = int(ts / interval_size)
        if bin_ts >= num_intervals:
            bin_ts -= 1

        if bin_ts not in new_ts:
            new_ts[bin_ts] = curr_t
            curr_t += 1
        
        if new_ts[bin_ts] not in updated_edgelist:
            updated_edgelist[new_ts[bin_ts]] = {}

        for (u,v), n in edge_data.items():
            if (u, v) not in updated_edgelist[new_ts[bin_ts]]:
                updated_edgelist[new_ts[bin_ts]][(u, v)] = n
            else:
                updated_edgelist[new_ts[bin_ts]][(u, v)] += n
    print("Descritization Done..!")
    return updated_edgelist

def subsampling(graph: Union[object, dict], 
                      node_list: Optional[list] = [], 
                      random_selection: Optional[bool] = False, 
                      N: Optional[int] = 100
                      ) -> dict:
    """
    Subsampling a part of graph by only monitoring the contacts from specific nodes' list

    Parameters:
        graph: graph object or edgelist dict
        node_list: list, a set of nodes to extract their contacts from the graph
        random_selection: bool, wether randomly subsample a set of nodes from graph
        N: int, number of nodes to be randomly sampled from graph
    
    Returns:
        new_edgelist: dict, a dictionary of edges corresponding to nodes in the node_list
    """
    print("Generate graph subsample...")
    if isinstance(graph, dict):
        edgelist = graph
        nodes = node_list(graph)
    else:
        edgelist = graph.edgelist
        nodes = graph.nodes()
        # print(nodes[10])
        

    if random_selection:
        node_list = list(np.random.choice(nodes, size = N, replace = False))
        # print(node_list)

    new_edgelist = {}
    for t, edge_data in edgelist.items():
                # print("t",t)
                for (u,v), f in edge_data.items():
                    # print(u)
                    if u in node_list or v in node_list:
                        if t not in new_edgelist:
                            new_edgelist[t] = {}
                            new_edgelist[t][(u, v)] = f
                        else:
                            new_edgelist[t][(u, v)] = f
    # print(new_edgelist)
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
                   max_timestamps: Optional[int] = 400) -> bool:
    r"""
    Check if an edgelist is discretized or not.
    """
    timestamps = list(edgelist.keys())
    discretized = True
    if len(timestamps) > max_timestamps:
        discretized = False
    
    return discretized