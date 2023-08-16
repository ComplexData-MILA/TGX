import matplotlib.pyplot as plt

__all__ = ["average_degree",
           "nodes_per_timestamp",
           "edges_per_timestamp"]


def average_degree(graph, plot_path, network_name):
    '''
    input: a list containing graph snapshots
    return: list of average degree per snapshot
    '''
    total_ts = len(graph)
    ave_degree = []
    for t1 in range(total_ts):
        num_edges = graph[t1].number_of_edges()
        ave_degree.append(num_edges*2/ graph[t1].number_of_nodes())
    filename = f"{network_name}_ave_degree_per_ts"
    plot_for_snapshots(ave_degree, plot_path, filename, "Average degree")
    return ave_degree

def nodes_per_timestamp(graph, plot_path, network_name):
    '''
    input: a list containing graph snapshots
    return: list of number of nodes per snapshot
    '''
    active_nodes = []
    for ts in range(len(graph)):
        active_nodes.append(graph[ts].number_of_nodes())
    filename = f"{network_name}_nodes_per_ts"
    plot_for_snapshots(active_nodes, plot_path, filename, "Number of nodes")
    return active_nodes

def edges_per_timestamp(graph, plot_path, network_name):
    '''
    input: a list containing graph snapshots
    return: list of number of edges per snapshot
    '''
    active_edges = []
    for ts in range(len(graph)):
        active_edges.append(graph[ts].number_of_edges())
    filename = f"{network_name}_edges_per_ts"
    plot_for_snapshots(active_edges, plot_path, filename, "Number of edges")
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