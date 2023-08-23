import numpy as np
from typing import Union
def graph_subsampling(graph: Union[object, dict], node_list:list =[], random_selection=False, N=100) -> dict:
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