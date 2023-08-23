from tgx.utils.plotting_utils import plot_for_snapshots, plot_nodes_edges_per_ts

__all__ = ["average_degree_per_ts",
           "nodes_per_ts",
           "edges_per_ts",
           "nodes_and_edges_per_ts"]


def average_degree_per_ts(graph: list, 
                          total_nodes: int, 
                          plot_path: str, 
                          network_name: str) -> None:
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting average degree per timestamp")
    ave_degree = _calculate_average_degree_per_ts(graph, total_nodes)
    filename = f"{network_name}_ave_degree_per_ts"
    plot_for_snapshots(ave_degree, plot_path, filename, "Average degree")
    print("Plotting Done!")
    return 


def nodes_per_ts(graph: list, 
                 plot_path: str, 
                 network_name: str) -> None:
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting number of nodes per timestamp")
    active_nodes = _calculate_node_per_ts(graph)
    filename = f"{network_name}_nodes_per_ts"
    plot_for_snapshots(active_nodes, plot_path, filename, "Number of nodes")
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
                           plot_path: list, 
                           network_name: list):
    
    edges = _calculate_edge_per_ts(graph)
    nodes = _calculate_node_per_ts(graph)
    ts = list(range(0, len(graph)))

    return plot_nodes_edges_per_ts(edges, nodes, ts, plot_path, network_name)
    

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


