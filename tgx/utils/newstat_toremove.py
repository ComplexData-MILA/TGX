from tgx.utils.plotting_utils import plot_for_snapshots, plot_nodes_edges_per_ts, plot_density_map
import networkx as nx
import numpy as np
from tgx.utils.graph_utils import train_test_split
from typing import List, Dict

__all__ = ["connected_components_per_ts", 
           "size_connected_components",
           "get_avg_node_engagement", 
           "degree_density"]


def degree_density(graph_edgelist: dict, k: int = 10, network_name: str = None, plot_path: str = None) -> None:
    r"""
    Plot density map of node degrees per time window
    Parameters:
        graph_edgelist: Dictionary containing graph data
        k: number of time windows
        network_name: name of the graph to be used in the output file name
        plot_path: path to save the output figure
    """
    degrees_by_k_list = []
    temp = []
    temp_idx = 0
    unique_ts = list(graph_edgelist.keys())
    for ts in unique_ts:
        e_at_this_ts = graph_edgelist[ts]
        G = nx.MultiGraph()
        for e, repeat in e_at_this_ts.items():
            G.add_edge(e[0], e[1], weight=repeat)
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
        filename = f"{network_name}_get_degree_density"
    else:
        filename = "_get_degree_density"
    plot_density_map(degrees_by_k_list, filename, "Node Degree", plot_path = plot_path)
    print("Plotting Done!")
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


def connected_components_per_ts(graph: list,  
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
    for t in range(len(graph)):
        parent = list(range(graph[t].number_of_nodes))

        for _, edge_data in graph[t].edgelist.items():
            for (u, v), _ in edge_data.items():
                _merge(u, v, parent)

        num = 0
        for u in graph[t].nodes():
            if parent[u] == u:
                num += 1
        num_components.append(num)   

    if network_name is not None:
        filename = f"{network_name}_connected_components_per_ts"
    else:
        filename = "_connected_components_per_ts"
    plot_for_snapshots(num_components, filename, "Number of connected components", plot_path = plot_path)
    print(num_components)
    print("Plotting Done!")

    return 


def size_connected_components(graph: list) -> List[Dict]: 
    r"""
    Calculate the sizes of connected components per timestamp
    Returns:
        list: A list containing the sizes of connected components in each timestamp.
    """
    component_sizes = []
    for t in range(len(graph)):
        parent = list(range(graph[t].number_of_nodes))

        for _, edge_data in graph[t].edgelist.items():
            for (u, v), _ in edge_data.items():
                _merge(u, v, parent)

        component_sizes_t = {}
        for u in graph[t].nodes():
            root = _find(u, parent)
            if root not in component_sizes_t:
                component_sizes_t[root] = 0  
            component_sizes_t[root] += 1  

        component_sizes.append(component_sizes_t)

    return component_sizes


def get_avg_node_engagement(graph_edgelist: dict) -> List[int]: 
    r"""
    Calculate the average node engagement per timestamp,
        the average number of distinct nodes that establish
        at least one new connection.
    Parameters:
        graph_edgelist: Dictionary containing graph data
    """
    engaging_nodes = []
    previous_edges = set()
    for ts, e_list in graph_edgelist.items():
        node_set = set()
        new_edges = {(u, v) for (u, v), _ in e_list.items() if frozenset({u, v}) not in previous_edges}
        for u, v in new_edges:
            if u not in node_set:
                node_set.add(u)
            if v not in node_set:
                node_set.add(v)
        engaging_nodes.append(len(node_set))
        previous_edges = {frozenset({u, v}) for (u, v), _ in e_list.items()}        # Update the set of previous edges for the next timestamp
    return engaging_nodes