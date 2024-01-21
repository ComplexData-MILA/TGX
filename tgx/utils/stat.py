from tgx.utils.plotting_utils import plot_for_snapshots, plot_nodes_edges_per_ts, plot_density_map
import networkx as nx
import numpy as np
from typing import List

__all__ = ["degree_over_time",
           "nodes_over_time",
           "edges_over_time",
           "nodes_and_edges_over_time",
           "get_avg_e_per_ts",
           "get_avg_degree",
           "get_num_timestamps",
           "get_num_unique_edges",
           "get_reoccurrence",
           "get_surprise",
           "get_novelty",
           "get_avg_node_activity",
           "connected_components_per_ts", 
           "size_connected_components",
           "get_avg_node_engagement", 
           "degree_density"]

#* helper functions
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


def degree_over_time(graph: object,  
                    network_name: str,
                    filepath: str = "./") -> None:
    r'''
    Plot average degree per timestamp.
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
     network_name: name of the graph to be used in the output file name
     filepath: path to save the output figure
    '''
    ave_degree = _calculate_average_degree_per_ts(graph)

    if network_name is not None:
        filename = f"{network_name}_ave_degree_per_ts"
    else:
        filename = "ave_degree_per_ts"
    plot_for_snapshots(ave_degree, y_title= "Average degree", filename=filepath+filename)    
    return 



def nodes_over_time(graph: object,  
                 network_name: str,
                 filepath: str = "./") -> None:

    r'''
    Plot number of active nodes per timestamp.
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
     network_name: name of the graph to be used in the output file name
     filepath: path to save the output figure
    '''
    active_nodes = _calculate_node_per_ts(graph)
    if network_name is not None:
        filename = f"{network_name}_nodes_per_ts"
    else:
        filename = "nodes_per_ts"
    plot_for_snapshots(active_nodes, y_title="Number of nodes", filename=filepath+filename)
    return 

def edges_over_time(graph: object, 
                 network_name: str = None,
                 filepath: str = "./") -> None:
    r'''
    Plot number of edges per timestamp.
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
     network_name: name of the graph to be used in the output file name
     filepath: path to save the output figure
    '''
    active_edges = _calculate_edge_per_ts(graph)
    if network_name is not None:
        filename = f"{network_name}_edges_per_ts"
    else:
        filename = "_edges_per_ts"
    plot_for_snapshots(active_edges, y_title="Number of edges", filename=filepath+filename)
    return 

def nodes_and_edges_over_time(graph: object, 
                           network_name: str ,
                           filepath: str = "./"):
    r"""
    Plot number of nodes per timestamp and number of edges per timestamp in one fiugre.
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
     network_name: name of the graph to be used in the output file name
     filepath: path to save the output figure
    """
    print("Plotting number of nodes and edges per timestamp.")
    edges = _calculate_edge_per_ts(graph)
    nodes = _calculate_node_per_ts(graph)
    ts = list(range(0, len(graph.data)))
    if network_name is not None:
        filename = f"{network_name}_node_and_edges_per_ts"
    else:
        filename = "node_and_edges_per_ts"
    return plot_nodes_edges_per_ts(edges, nodes, ts, filename=filepath+filename)

    

def _calculate_average_degree_per_ts(graph):
    total_nodes = graph.total_nodes()
    total_ts = len(graph.data)
    ave_degree = []
    for ts in range(total_ts):
        num_edges = len(graph.data[ts])
        ave_degree.append(num_edges*2/ total_nodes)
    return ave_degree


def _calculate_node_per_ts(graph):
    active_nodes = []
    for ts in range(len(graph.data)):
        active_nodes.append(graph.edgelist_node_count(graph.data[ts]))
    return active_nodes

def _calculate_edge_per_ts(graph):
    active_edges = []
    for ts in range(len(graph.data)):
        active_edges.append(len(graph.data[ts]))
    return active_edges

def get_avg_e_per_ts(graph_edgelist: dict) -> float:
    r"""
    Calculate the average number of edges per timestamp
    
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
    """
    sum_num_e_per_ts = 0
    unique_ts = list(graph_edgelist.keys())
    for ts in unique_ts:
        num_e_at_this_ts = 0
        edge_at_this_ts = graph_edgelist[ts]
        for e, repeat in edge_at_this_ts.items():
            num_e_at_this_ts += repeat
        sum_num_e_per_ts += num_e_at_this_ts
    avg_num_e_per_ts = (sum_num_e_per_ts * 1.0) / len(unique_ts)

    print(f"INFO: avg_num_e_per_ts: {avg_num_e_per_ts}")
    return avg_num_e_per_ts


def get_avg_degree(graph: object) -> float:
    r"""
    Calculate average degree over the timestamps
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
    """
    graph_edgelist = graph.data
    degree_avg_at_ts_list = []
    unique_ts = list(graph_edgelist.keys())
    for ts in unique_ts:
        e_at_this_ts = graph_edgelist[ts]
        G = nx.MultiGraph()
        for e, repeat in e_at_this_ts.items():
            G.add_edge(e[0], e[1], weight=repeat)
        nodes = G.nodes()
        degrees = [G.degree[n] for n in nodes]
        degree_avg_at_ts_list.append(np.mean(degrees))

    print(f"INFO: avg_degree: {np.mean(degree_avg_at_ts_list)}")
    return np.mean(degree_avg_at_ts_list)


def get_num_timestamps(graph_edgelist:dict) -> int:
    r"""
    Calculate the number of timestamps
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
    """
    print(f"INFO: Number of timestamps: {len(graph_edgelist)}")
    return len(graph_edgelist)

def get_num_unique_edges(graph: object) -> int:
    r"""
    Calculate the number of unique edges
    Parameters:
     graph: Graph object created by tgx.Graph containing edgelist
    """
    graph_edgelist = graph.data
    unique_edges = {}
    for ts, e_list in graph_edgelist.items():
        for e in e_list:
            if e not in unique_edges:
                unique_edges[e] = 1
    print(f"INFO: Number of unique edges: {len(unique_edges)}")
    return len(unique_edges)


def _split_data_chronological(graph_edgelist: dict, test_ratio: int):
    r"""
    split the timestamped edge-list chronologically
    """
    # split the temporal graph data chronologically
    unique_ts = np.sort(list(graph_edgelist.keys()))
    test_split_time = list(np.quantile(unique_ts, [1 - test_ratio]))[0]
    
    # make train-validation & test splits
    train_val_e_set, test_e_set = {}, {}
    for ts, e_list in graph_edgelist.items():
        for (u,v) in e_list:
            
            if ts < test_split_time:
                if (u,v) not in train_val_e_set:
                    train_val_e_set[(u,v)] = 1
            else:
                if (u,v) not in test_e_set:
                    test_e_set[(u,v)] = 1
    return train_val_e_set, test_e_set

def find(x, parent):
    if parent[x] == x:
        return x
    parent[x] = find(parent[x], parent)  
    return parent[x]


def merge(x, y, parent):
    root_x = find(x, parent)
    root_y = find(y, parent)

    if root_x != root_y:
        parent[root_x] = root_y  

def get_reoccurrence(graph:object, test_ratio: float=0.15) -> float:
    r"""
    Calculate the recurrence index
    Parameters:
        graph: Graph object created by tgx.Graph containing edgelist
        test_ratio: The ratio to split the data chronologically
    """
    graph_edgelist = graph.data
    train_val_e_set, test_e_set = _split_data_chronological(graph_edgelist, test_ratio)
    train_val_size = len(train_val_e_set)
    # intersect = 0
    # total_train_freq = 0
    # for e, freq in train_val_e_set.items():
    #     if freq > 1:
    #         print(e)
    #     total_train_freq += freq
    #     if e in test_e_set:
    #         intersect += freq

    # print(total_train_freq, intersect)
    # reoccurrence = float(intersect * 1.0 / total_train_freq)
    intersect = 0
    for e in test_e_set:
        if e in train_val_e_set:
            intersect += 1
    reoccurrence = float(intersect * 1.0 / train_val_size)
    print(f"INFO: Reoccurrence: {reoccurrence}")
    return reoccurrence

def get_surprise(graph, test_ratio: float = 0.15) -> float:
    r"""
    Calculate the surprise index
    Parameters:
        graph: Graph object created by tgx.Graph containing edgelist
        test_ratio: The ratio to split the data chronologically
    """
    graph_edgelist = graph.data
    train_val_e_set, test_e_set = _split_data_chronological(graph_edgelist, test_ratio)
    test_size = len(test_e_set)

    difference = 0
    # total_test_freq = 0
    # for e, freq in test_e_set.items():
    #     total_test_freq += freq
    #     if e not in train_val_e_set:
    #         difference += freq
    # surprise = float(difference * 1.0 / total_test_freq)

    for e in test_e_set:
        if e not in train_val_e_set:
            difference += 1
    surprise = float(difference * 1.0 / test_size)
    print(f"INFO: Surprise: {surprise}")
    return surprise

def get_novelty(graph : object) -> float:
    r"""
    Calculate the novelty index
    Parameters:
        graph: Graph object created by tgx.Graph containing edgelist
    """
    graph_edgelist = graph.data
    unique_ts = np.sort(list(graph_edgelist.keys()))
    novelty_ts = []
    for ts_idx, ts in enumerate(unique_ts):
        e_set_this_ts = set(list(graph_edgelist[ts]))
        e_set_seen = []
        for idx in range(0, ts_idx):
            e_set_seen.append(list(graph_edgelist[unique_ts[idx]]))
        e_set_seen = set(item for sublist in e_set_seen for item in sublist)
        novelty_ts.append(float(len(e_set_this_ts - e_set_seen) * 1.0 / len(e_set_this_ts)))

    novelty = float(np.sum(novelty_ts) * 1.0 / len(unique_ts))
    print(f"INFO: Novelty: {novelty}")
    return novelty


def get_avg_node_activity(graph: object) -> float:
    r"""
    Calculate the average node activity,
        the proportion of time steps a node is present
    Parameters:
        graph: Graph object created by tgx.Graph containing edgelist
    """
    graph_edgelist = graph.data
    num_unique_ts = len(graph_edgelist)
    node_ts = {}
    for ts, e_list in graph_edgelist.items():
        for e in e_list:
            # source
            if e[0] not in node_ts:
                node_ts[e[0]] = {ts: True}
            else:
                if ts not in node_ts[e[0]]:
                    node_ts[e[0]][ts] = True

            # destination
            if e[1] not in node_ts:
                node_ts[e[1]] = {ts: True}
            else:
                if ts not in node_ts[e[1]]:
                    node_ts[e[1]][ts] = True

    node_activity_ratio = []
    for n, ts_list in node_ts.items():
        node_activity_ratio.append(float(len(ts_list) * 1.0 / num_unique_ts))

    avg_node_activity = float(np.sum(node_activity_ratio) * 1.0 / len(node_activity_ratio))
    print(f"INFO: Node activity ratio: {avg_node_activity}")
    return avg_node_activity


def get_avg_node_engagement(graph: object): 
    r"""
    get the average node engagement over time.
    node engagement represents the average number of distinct nodes that establish
    at least one new connection during each time step.
    """
    graph_edgelist = graph.data
    engaging_nodes = []
    previous_edges = set()
    for ts, e_list in graph_edgelist.items():
        node_set = set()
        new_edges = {(u, v) for (u, v) in e_list if frozenset({u, v}) not in previous_edges}
        for u, v in new_edges:
            if u not in node_set:
                node_set.add(u)
            if v not in node_set:
                node_set.add(v)
        # engaging_nodes.append((ts, len(node_set)))
        engaging_nodes.append(len(node_set))
        previous_edges = {frozenset({u, v}) for (u, v) in e_list}        # Update the set of previous edges for the next timestamp
    return engaging_nodes

def degree_density(graph: tuple, 
                   k: int = 10, 
                   network_name: str = None, 
                   plot_path: str = "./") -> None:
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

    plot_density_map(degrees_by_k_list, y_title="Node Degree", filename = plot_path + filename)
    return 


def connected_components_per_ts(graph: tuple,  
                 network_name: str = None,
                 plot_path: str = "./") -> None:
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

    plot_for_snapshots(num_components, y_title="Number of connected components", filename=plot_path+filename)
    return 


# TODO turn this into a plotting function as well, can return the computed stats
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

# TODO turn this into a plotting function as well, can return the computed stats
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