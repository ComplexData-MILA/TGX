import datetime
import pandas as pd
import matplotlib.pyplot as plt

def create_ts_list(start, end, metric=None, interval=None):
    if metric == "Unix" or metric == "unix" or metric == "UNIX":
        start = datetime.datetime.fromtimestamp(start).date()
        end = datetime.datetime.fromtimestamp(end).date()
        if interval == 'daily':
            date_list = pd.date_range(start = start, end = end, freq="D") 
        elif interval == "month":
            date_list = pd.date_range(start = start, end = end, freq="M")
        elif interval == "year":
            date_list = pd.date_range(start = start, end = end, freq="Y") 
        timelist = []
        for dates in date_list:
            timelist.append(dates.strftime("%Y/%m/%d"))
    else:
        timelist = list(range(start, end, interval))
    # print(timelist)
    return timelist

    

def plot_nodes_edges_per_ts(edges: list,
                            nodes: list, 
                            ts: list,
                            network_name: str, 
                            plot_path: str = None, 
                            ylabel_1 = 'Edges per Timestamp',
                            ylabel_2 = 'Nodes per Timestamp'):

    fig = plt.figure(facecolor='w', figsize=(11, 6))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    c1, = ax1.plot(ts, edges, color='black', lw=3, label=ylabel_1)
    c2, = ax2.plot(ts, nodes, color='gray', linestyle='dashed', lw=3, label=ylabel_2)
    curves = [c1, c2]
    ax1.legend(curves, [curve.get_label() for curve in curves], fontsize = 18)
    ax1.set_xlabel('Time', fontsize=20)
    ax1.set_ylabel(ylabel_1, fontsize=20)
    ax2.set_ylabel(ylabel_2, fontsize=20)
    ax1.tick_params(labelsize=20)
    ax2.tick_params(labelsize=20)
    ax1.set_ylim(0)
    ax2.set_ylim(0)
    ax1.set_xlim(0, len(ts)-1)
    if plot_path is not None:
        filename = f"{network_name}_node&edge_per_ts"
        plt.savefig(f'{plot_path}/{filename}')
    plt.show()

def plot_for_snapshots(data,  filename, y_title, plot_path = None,):
    '''
    plot
    '''
    ts = list(range(0, len(data)))

    fig = plt.figure(facecolor='w', figsize=(9,6))
    ax = fig.add_subplot(111)
    ax.plot(ts, data, color='black', lw=3)

    ax.set_xlabel('Time', fontsize=20)
    ax.set_ylabel(y_title, fontsize=20)
    ax.tick_params(labelsize=20)
    ax.set_ylim(0, 5)
    ax.set_xlim(0, len(ts)-1)
    if plot_path is not None:
        plt.savefig(f'{plot_path}/{filename}')
    plt.show()

if __name__ == "__main__":
    create_ts_list(86400, 86400*365, "unix", "month")
    create_ts_list(2015, 2022, interval=2)