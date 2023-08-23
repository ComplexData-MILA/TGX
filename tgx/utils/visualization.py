import matplotlib.pyplot as plt

__all__ = ["average_degree",
           "nodes_per_timestamp",
           "edges_per_timestamp",
           "plot_nodes_edges_per_ts"]


def average_degree(graph, total_nodes, plot_path, network_name):
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting average degree per timestamp")
    ave_degree = _calculate_average_degree_per_ts(graph, total_nodes)
    filename = f"{network_name}_ave_degree_per_ts"
    plot_for_snapshots(ave_degree, plot_path, filename, "Average degree")
    print("Plotting Done!")
    return 


def nodes_per_timestamp(graph, plot_path, network_name):
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting number of nodes per timestamp")
    active_nodes = _calculate_node_per_ts(graph)
    filename = f"{network_name}_nodes_per_ts"
    plot_for_snapshots(active_nodes, plot_path, filename, "Number of nodes")
    print("Plotting Done!")
    return 

def edges_per_timestamp(graph, plot_path, network_name):
    '''
    input: a list containing graph snapshots
    '''
    print("Plotting number of edges per timestamp")
    active_edges = _calculate_edge_per_ts(graph)
    filename = f"{network_name}_edges_per_ts"
    plot_for_snapshots(active_edges, plot_path, filename, "Number of edges")
    print("Plotting Done!")
    return 

def plot_nodes_edges_per_ts(graph, plot_path, network_name):
    edges = _calculate_edge_per_ts(graph)
    nodes = _calculate_node_per_ts(graph)

    ts = list(range(0, len(graph)))
    fig = plt.figure(facecolor='w', figsize=(12, 8))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    c1, = ax1.plot(ts, edges, color='black', lw=3, label="Edges")
    c2, = ax2.plot(ts, nodes, color='gray', linestyle='dashed', lw=3, label="Nodes")
    curves = [c1, c2]
    ax1.legend(curves, [curve.get_label() for curve in curves], fontsize = 20)
    ax1.set_xlabel('time', fontsize=20)
    ax1.set_ylabel('# of Edges per Timestamp', fontsize=20)
    ax2.set_ylabel('# of Nodes per Timestamp', fontsize=20)
    ax1.tick_params(labelsize=20)
    ax2.tick_params(labelsize=20)
    ax1.set_ylim(0)
    ax2.set_ylim(0)
    ax1.set_xlim(0, len(ts)-1)
    filename = f"{network_name}_node&edge_per_ts"
    plt.savefig(f'{plot_path}/{filename}')

def _calculate_average_degree_per_ts(graph, total_nodes):
    total_ts = len(graph)
    ave_degree = []
    for t1 in range(total_ts):
        num_edges = graph[t1].number_of_edges()
        ave_degree.append(num_edges*2/ total_nodes)
    return average_degree


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


def plot_for_snapshots(data, plot_path, filename, y_title):
    '''
    plot
    '''
    ts = list(range(0, len(data)))

    fig = plt.figure(facecolor='w', figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.plot(ts, data, color='black', lw=3)

    ax.set_xlabel('time', fontsize=20)
    ax.set_ylabel(y_title, fontsize=20)
    ax.tick_params(labelsize=20)
    plt.savefig(f'{plot_path}/{filename}')