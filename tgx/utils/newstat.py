from tgx.utils.plotting_utils import plot_for_snapshots, plot_nodes_edges_per_ts, plot_density_map
import networkx as nx
import numpy as np
from tgx.utils.graph_utils import train_test_split
from typing import List, Dict

__all__ = ["connected_components_per_ts", 
           "size_connected_components",
           "get_avg_node_engagement", 
           "degree_density"]


def degree_density(graph: tuple, k: int = 10, network_name: str = None, plot_path: str = None) -> None:
    r"""
    Plot density map of node degrees per time window
    Parameters:
        graph_edgelist: Dictionary containing graph data
        k: number of time windows
        network_name: name of the graph to be used in the output file name
        plot_path: path to save the output figure
    """
    graph_edgelist = graph.data
    degrees_by_k_list = []
    temp = []
    temp_idx = 0
    unique_ts = list(graph_edgelist.keys())

    for ts in unique_ts:
        e_at_this_ts = graph_edgelist[ts]
        G = nx.MultiGraph()

        for e in e_at_this_ts:
            G.add_edge(e[0], e[1])

        nodes = G.nodes()
        degrees = [G.degree[n] for n in nodes]

        if temp_idx<k:
            temp.extend(degrees)
            temp_idx += 1
        else: 
            degrees_by_k_list.append(temp)
            temp = degrees
            temp_idx = 1

    if temp:
        degrees_by_k_list.append(temp)

    if network_name is not None:
        filename = f"{network_name}_degree_density"
    else:
        filename = "_degree_density"

    plot_density_map(degrees_by_k_list, filename, "Node Degree", plot_path = plot_path)
    return 


def _find(x, parent):
    if parent[x] == x:
        return x
    parent[x] = _find(parent[x], parent)  
    return parent[x]


def _merge(x, y, parent):
    root_x = _find(x, parent)
    root_y = _find(y, parent)

    if root_x != root_y:
        parent[root_x] = root_y  


def connected_components_per_ts(graph: tuple,  
                 network_name: str = None,
                 plot_path: str = None) -> None:
    r"""
    Plot number of connected components per timestamp
    Parameters:
        graph: a list containing graph snapshots
        network_name: name of the graph to be used in the output file name
        plot_path: path to save the output figure
    """
    num_components = []
    for t in range(len(graph.data)):
        edgelist_t = graph.data[t]
        nodes_t = graph.edgelist_node_list(edgelist_t)
        parent = {node: node for node in nodes_t} 

        for edge in edgelist_t:
            (u, v) = edge
            _merge(u, v, parent)

        num = 0
        for u in nodes_t:
            if parent[u] == u:
                num += 1       
        num_components.append(num)  

    if network_name is not None:
        filename = f"{network_name}_connected_components_per_ts"
    else:
        filename = "_connected_components_per_ts"

    plot_for_snapshots(num_components, filename, "Number of connected components", plot_path = plot_path)
    return 


def size_connected_components(graph: tuple) -> List[List]: 
    r"""
    Calculate the sizes of connected components per timestamp
    Returns:
        list[list]: A list containing lists of sizes of connected components for each timestamp.
    """
    component_sizes = []
    for t in range(len(graph.data)):
        edgelist_t = graph.data[t]
        nodes_t = graph.edgelist_node_list(edgelist_t)
        parent = {node: node for node in nodes_t} 

        for edge in edgelist_t:
            (u, v) = edge
            _merge(u, v, parent)

        component_sizes_t = {}
        for u in nodes_t:
            root = _find(u, parent)
            if root not in component_sizes_t:
                component_sizes_t[root] = 0  
            component_sizes_t[root] += 1  
            
        component_sizes_t_list = list(component_sizes_t.values())
        component_sizes.append(component_sizes_t_list)

    return component_sizes


def get_avg_node_engagement(graph: tuple) -> List[int]: 
    r"""
    Calculate the average node engagement per timestamp,
        the average number of distinct nodes that establish
        at least one new connection.
    Parameters:
        graph_edgelist: Dictionary containing graph data
    """
    engaging_nodes = []
    previous_edges = set()

    for ts in range(len(graph.data)):
        edgelist_t = graph.data[ts]
        new_nodes = set()

        for edge in edgelist_t:
            (u, v) = edge
            if frozenset({u, v}) not in previous_edges:
                if u not in new_nodes:
                    new_nodes.add(u)
                if v not in new_nodes:
                    new_nodes.add(v)   
                    
        engaging_nodes.append(len(new_nodes))
        previous_edges = {frozenset({u, v}) for (u, v) in edgelist_t}        # Update the set of previous edges for next timestamp

    return engaging_nodes