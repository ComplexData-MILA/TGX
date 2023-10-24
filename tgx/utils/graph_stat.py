from tgx.utils.plotting_utils import plot_for_snapshots, plot_nodes_edges_per_ts
import networkx as nx
import numpy as np
from tgx.utils.graph_utils import train_test_split

__all__ = ["average_degree_per_ts",
           "nodes_per_ts",
           "edges_per_ts",
           "nodes_and_edges_per_ts",
           "get_avg_e_per_ts",
           "get_avg_degree",
           "get_num_timestamps",
           "get_num_unique_edges",
           "get_reoccurrence",
           "get_surprise",
           "get_avg_node_activity"
           ]


def average_degree_per_ts(graph: list, 
                          total_nodes: int, 
                          network_name: str,
                          plot_path: str = None) -> None:
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting average degree per timestamp")
    ave_degree = _calculate_average_degree_per_ts(graph, total_nodes)
    filename = f"{network_name}_ave_degree_per_ts"
    plot_for_snapshots(ave_degree, filename, "Average degree", plot_path = plot_path)
    print("Plotting Done!")
    return 


def nodes_per_ts(graph: list,  
                 network_name: str,
                 plot_path: str = None) -> None:
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting number of nodes per timestamp")
    active_nodes = _calculate_node_per_ts(graph)
    filename = f"{network_name}_nodes_per_ts"
    plot_for_snapshots(active_nodes, filename, "Number of nodes", plot_path = plot_path)
    print("Plotting Done!")
    return 

def edges_per_ts(graph: list, 
                 plot_path: str, 
                 network_name: str) -> None:
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting number of edges per timestamp")
    active_edges = _calculate_edge_per_ts(graph)
    filename = f"{network_name}_edges_per_ts"
    plot_for_snapshots(active_edges, plot_path, filename, "Number of edges")
    print("Plotting Done!")
    return 

def nodes_and_edges_per_ts(graph: list, 
                           network_name: str,
                           plot_path: str = None):
    
    edges = _calculate_edge_per_ts(graph)
    nodes = _calculate_node_per_ts(graph)
    ts = list(range(0, len(graph)))

    return plot_nodes_edges_per_ts(edges, nodes, ts, network_name, plot_path = plot_path)
    

def _calculate_average_degree_per_ts(graph, total_nodes):
    total_ts = len(graph)
    ave_degree = []
    for t1 in range(total_ts):
        num_edges = graph[t1].number_of_edges()
        ave_degree.append(num_edges*2/ total_nodes)
    return ave_degree


def _calculate_node_per_ts(graph):
    active_nodes = []
    for ts in range(len(graph)):
        active_nodes.append(graph[ts].number_of_nodes())
    return active_nodes

def _calculate_edge_per_ts(graph):
    active_edges = []
    for ts in range(len(graph)):
        active_edges.append(graph[ts].number_of_edges())
    return active_edges

def get_avg_e_per_ts(graph_edgelist):
    r"""
    calculate the average number of edges per timestamp
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


def get_avg_degree(graph_edgelist):
    r"""
    get average degree over the timestamps
    """
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


def get_num_timestamps(graph_edgelist):
    r"""
    get number of timestamps
    """
    print(f"INFO: Number of timestamps: {len(graph_edgelist)}")
    return len(graph_edgelist)

def get_num_unique_edges(graph_edgelist):
    r"""
    get the number of unique edges
    """
    unique_edges = {}
    for ts, e_list in graph_edgelist.items():
        for e, repeat in e_list.items():
            if e not in unique_edges:
                unique_edges[e] = 1
    print(f"INFO: Number of unique edges: {len(unique_edges)}")
    return len(unique_edges)


def _split_data_chronological(graph_edgelist, test_ratio):
    r"""
    split the timestamped edge-list chronologically
    """
    # split the temporal graph data chronologically
    unique_ts = np.sort(list(graph_edgelist.keys()))
    test_split_time = list(np.quantile(unique_ts, [1 - test_ratio]))[0]
    
    # make train-validation & test splits
    train_val_e_set, test_e_set = {}, {}
    # for ts, e_list in graph_edgelist.items():
    #     for (u,v), repeat in e_list.items():
            
    #         if ts < test_split_time:
    #             if (u,v) not in train_val_e_set:
    #                 train_val_e_set[(u,v)] = True
    #         else:
    #             if (u,v) not in test_e_set:
    #                 test_e_set[(u,v)] = True

    for ts, e_list in graph_edgelist.items():
        for (u,v), freq in e_list.items():
            
            if ts < test_split_time:
                if (u,v) not in train_val_e_set:
                    train_val_e_set[(u,v)] = freq
            else:
                if (u,v) not in test_e_set:
                    test_e_set[(u,v)] = freq
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


def size_connected_components(graph):
    """
    get the sizes of connected components per timestamp.

    Returns:
    - list: A list containing the sizes of connected components in each timestamp.
    """
    
    component_sizes = []
    for t in range(len(graph)):
        parent = list(range(graph[t].number_of_nodes))

        for _, edge_data in graph[t].edgelist.items():
            for (u, v), _ in edge_data.items():
                merge(u, v, parent)

        component_sizes_t = {}
        for u in graph[t].nodes():
            root = find(u, parent)
            if root not in component_sizes_t:
                component_sizes_t[root] = 0  
            component_sizes_t[root] += 1  

        component_sizes.append(component_sizes_t)

    return component_sizes
        

def num_connected_components_per_ts(graph: list,  
                 network_name: str,
                 plot_path: str = None) -> None:
    """
    
    plot the number of connected components per timestamp.

    """

    num_components = []
    for t in range(len(graph)):
        parent = list(range(graph[t].number_of_nodes))

        for _, edge_data in graph[t].edgelist.items():
            for (u, v), _ in edge_data.items():
                merge(u, v, parent)

        num = 0
        for u in graph[t].nodes():
            if parent[u] == u:
                num += 1
        num_components.append(num)   

    filename = f"{network_name}_num_connected_components_per_ts"
    plot_for_snapshots(num_components, filename, "Number of connected components", plot_path = plot_path)
    print(num_components)
    print("Plotting Done!")

    return 


def get_reoccurrence(graph_edgelist, test_ratio=0.15):
    r"""
    get the recurrence index
    """
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

def get_surprise(graph_edgelist, test_ratio=0.15):
    r"""
    get the surprise index
    """
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

def get_novelty(graph_edgelist):
    r"""
    get novelty index
    """
    unique_ts = np.sort(list(graph_edgelist.keys()))
    novelty_ts = []
    for ts_idx, ts in enumerate(unique_ts):
        e_set_this_ts = set(list(graph_edgelist[ts].keys()))
        e_set_seen = []
        for idx in range(0, ts_idx):
            e_set_seen.append(list(graph_edgelist[unique_ts[idx]].keys()))
        e_set_seen = set(item for sublist in e_set_seen for item in sublist)
        novelty_ts.append(float(len(e_set_this_ts - e_set_seen) * 1.0 / len(e_set_this_ts)))

    novelty = float(np.sum(novelty_ts) * 1.0 / len(unique_ts))
    print(f"INFO: Novelty: {novelty}")
    return novelty


def get_avg_node_activity(graph_edgelist):
    r"""
    get average node activity
        the proportion of time steps a node is present
    """
    num_unique_ts = len(graph_edgelist)
    node_ts = {}
    for ts, e_list in graph_edgelist.items():
        for e, repeat in e_list.items():
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


def get_avg_node_engagement(graph_edgelist): 
    r"""
    get the average node engagement over time.
    node engagement represents the average number of distinct nodes that establish
    at least one new connection during each time step.
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
        engaging_nodes.append((ts, len(node_set)))
        previous_edges = {frozenset({u, v}) for (u, v), _ in e_list.items()}        # Update the set of previous edges for the next timestamp
    return engaging_nodes
