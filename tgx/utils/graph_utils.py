import numpy as np
from typing import Union, Optional


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
        nodes = _node_list(graph)
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

def _node_list(dict_edgelist: dict) -> list:
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