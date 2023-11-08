import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, Optional
from tgx.utils.graph_utils import edgelist_discritizer
from tgx.utils.plotting_utils import create_ts_list
__all__ = ["TEA"]

def TEA(
        temp_edgelist : Union[object, dict], 
        filepath : Optional[str] = None,
        fig_size : tuple = (7,5),
        font_size : int = 20, 
        network_name : str =None,
        intervals : Union[str, int] = None, 
        real_dates : bool = None,
        test_split : bool = False,
        max_intervals : int = 1000,
        density : bool = False
        ):
    r"""
    generating TEA plot
    Args:
        temp_edgelist: a dictionary of temporal edges or a dataset object
        filepath: Path to save the TEA Plot
    """
    if isinstance(temp_edgelist, object):
        if temp_edgelist.freq_data is None:
            temp_edgelist.count_freq()
        temp_edgelist = temp_edgelist.freq_data
    
    # check number of unique timestamps:
    unique_ts = list(temp_edgelist.keys())
    if len(unique_ts) > max_intervals:
        inp = input(f"There are {unique_ts} timestamps in the data.\nDo you want to discretize the data to 1000 timestamps?(y/n)").lower()
        if inp == "y":
            temp_edgelist = edgelist_discritizer(temp_edgelist,
                                                unique_ts,
                                                time_interval = max_intervals)
    elif intervals is not None:
        temp_edgelist = edgelist_discritizer(temp_edgelist,
                                            unique_ts,
                                            time_interval = intervals)


    ts_edges_dist, ts_edges_dist_density, edge_frequency_dict = TEA_process_edgelist_per_timestamp(temp_edgelist)
    
    TEA_plot_edges_bar(ts_edges_dist, 
                       filepath = filepath, 
                       fig_size = fig_size, 
                       font_size = font_size, 
                       network_name=network_name,
                       real_dates = real_dates,
                       test_split = test_split)

    if density:
        return ts_edges_dist_density, edge_frequency_dict



def TEA_process_edgelist_per_timestamp(temp_edgelist):
    # generate distribution of the edges history
    unique_ts = list(temp_edgelist.keys())
    # unique_ts.sort()
    # print(f"There are {len(unique_ts)} timestamps.")

    # get node set & total number of nodes
    node_dict = {}
    for t, e_dict in temp_edgelist.items():
        for e, exist in e_dict.items():
            if e[0] not in node_dict:
                node_dict[e[0]] = 1
            if e[1] not in node_dict:
                node_dict[e[1]] = 1
    num_nodes = len(node_dict)
    num_e_fully_connected = num_nodes * (num_nodes - 1)

    edge_frequency_dict = {}  # how many times an edge is seen
    ts_edges_dist = []  # contains different features specifying the characteristics of the edge distribution over time
    ts_edges_dist_density = []
    for curr_t in unique_ts:
            
        # if curr_t < 2:
            # print("curr_t", curr_t)
            prev_ts = [ts for ts in unique_ts if ts < curr_t]
            edges_in_prev_ts = {}
            for bts in prev_ts:
                edges_in_prev_ts.update(temp_edgelist[bts])
            
            curr_ts_edge_list = temp_edgelist[curr_t]
            for e in curr_ts_edge_list:
                if e not in edge_frequency_dict:
                    edge_frequency_dict[e] = 1
                else:
                    edge_frequency_dict[e] += 1

            if len(curr_ts_edge_list) > 0:
                curr_ts_edges_dist = {'ts': curr_t,
                                    'new': len([e for e in curr_ts_edge_list if e not in edges_in_prev_ts]),
                                    'repeated': len([e for e in curr_ts_edge_list if e in edges_in_prev_ts]),
                                    'not_repeated': len([e for e in edges_in_prev_ts if e not in curr_ts_edge_list]),
                                    'total_curr_ts': len(curr_ts_edge_list),
                                    'total_seen_until_curr_ts': len(edges_in_prev_ts) + len(curr_ts_edge_list)
                                    }
                curr_ts_edges_dist_density = {'ts': curr_t,
                                            'new': (curr_ts_edges_dist['new'] * 1.0) / num_e_fully_connected,
                                            'repeated': (curr_ts_edges_dist['repeated'] * 1.0) / num_e_fully_connected,
                                            'not_repeated': (curr_ts_edges_dist[
                                                                'not_repeated'] * 1.0) / num_e_fully_connected,
                                            'total_curr_ts': (curr_ts_edges_dist[
                                                                    'total_curr_ts'] * 1.0) / num_e_fully_connected,
                                            'total_seen_until_curr_ts': (curr_ts_edges_dist[
                                                                            'total_seen_until_curr_ts'] * 1.0) / num_e_fully_connected,
                                            }
            else:
                curr_ts_edges_dist = {'ts': curr_t,
                                    'new': 0,
                                    'repeated': 0,
                                    'not_repeated': 0,
                                    'total_curr_ts': 0,
                                    'total_seen_until_curr_ts': len(edges_in_prev_ts) + len(curr_ts_edge_list)
                                    }
                curr_ts_edges_dist_density = {'ts': curr_t,
                                            'new': 0,
                                            'repeated': 0,
                                            'not_repeated': 0,
                                            'total_curr_ts': 0,
                                            'total_seen_until_curr_ts': 0,
                                            }
            ts_edges_dist.append(curr_ts_edges_dist)
            ts_edges_dist_density.append(curr_ts_edges_dist_density)
    #         print(len(edges_in_prev_ts))
    # print(len(ts_edges_dist))
            # print(edge_frequency_dict)
            # break
    return ts_edges_dist, ts_edges_dist_density, edge_frequency_dict


def TEA_plot_edges_bar(ts_edges_dist, 
                   filepath = None, 
                   fig_size = (9,5),
                   font_size = 20,
                   network_name = None,
                   real_dates = None,
                   intervals = None,
                   test_split = False):
    

    ts_edges_dist_df = pd.DataFrame(ts_edges_dist, columns=['ts', 'new', 'repeated',
                                                            'not_repeated',
                                                            'total_curr_ts',
                                                            'total_seen_until_curr_ts'])
    

    ### Additional Stats ###
    mean = ts_edges_dist_df.mean(axis=0)
    # print("INFO: Network Name:", network_name)
    # print("INFO: AVG. stats. over all timestamps: ", mean)
    # print("INFO: ratio of avg.(new)/avg.(total_curr_ts): {:.2f}".format(mean['new'] / mean['total_curr_ts']))
    ###

    fig, ax = plt.subplots(figsize=fig_size)  # lastfm, mooc, reddit, UNtrade, UNvote
    plt.subplots_adjust(bottom=0.2, left=0.2)
    font_size = font_size
    ticks_font_size = 15
    plt.yticks(fontsize=ticks_font_size)
    plt.xticks(fontsize=ticks_font_size)
    if real_dates is not None:
        start = real_dates[0]
        end = real_dates[1]
        metric = real_dates[2]
        create_ts_list(start, end, metric=metric, interval=intervals)
    else:
        duration = ts_edges_dist_df['ts'].tolist()
        timestamps = [i for i in range(len(duration))]
    
    new = ts_edges_dist_df['new'].tolist()
    repeated = ts_edges_dist_df['repeated'].tolist()
    # print(len(timestamps), repeated, new)
    # plotting stuffs
    # bar plot
    plt.bar(timestamps, repeated, label='Repeated', color='#404040', alpha=0.4)
    plt.bar(timestamps, new, label='New', bottom=repeated, color='#ca0020', alpha=0.8, hatch='//')
    # test split line
    if test_split:
        plt.axvline(x=(timestamps[int(0.85 * len(timestamps))]), color="blue", linestyle="--", linewidth=2)
        plt.text((timestamps[int(0.85 * len(timestamps))]), 0,
                'x', va='center', ha='center', fontsize=font_size, fontweight='heavy', color='blue')

    plt.margins(x=0)
    plt.xlabel("Timestamp", fontsize=font_size)
    plt.ylabel("Number of edges", fontsize=font_size)
    plt.legend(fontsize = 13)
    if filepath is not None:
        plt.savefig(f"{filepath}/{network_name}.png")
    plt.show()
    print("Plotting done!")


