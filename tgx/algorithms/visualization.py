import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from tgx.utils.edgelist import edgelist_discritizer


def TEA(
        temp_edgelist, 
        filepath,
        fig_size = (7,5),
        font_size = 20, 
        network_name=None,
        density = False,
        intervals = None
        ):
    
    # check number of unique timestamps:
    unique_ts = list(temp_edgelist.keys())
    if unique_ts > 100 or intervals is not None:
        edgelist_discritizer()


    ts_edges_dist, ts_edges_dist_density, edge_frequency_dict = TEA_process_edgelist_per_timestamp(temp_edgelist)
    
    TEA_plot_edges_bar(ts_edges_dist, 
                       filepath, 
                       fig_size = fig_size, 
                       font_size = font_size, 
                       network_name=network_name)

    if density:
        return ts_edges_dist_density, edge_frequency_dict



def TEA_process_edgelist_per_timestamp(temp_edgelist):
    # generate distribution of the edges history
    unique_ts = list(temp_edgelist.keys())
    # unique_ts.sort()
    print(f"There are {len(unique_ts)} timestamps.")

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
            print(curr_t)
        # if curr_t < 63072000:
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
            # print(len(edges_in_prev_ts))
            # print(len(curr_ts_edge_list))
            # print(edge_frequency_dict)
            # break
    return ts_edges_dist, ts_edges_dist_density, edge_frequency_dict


def TEA_plot_edges_bar(ts_edges_dist, 
                   filepath, 
                   fig_size = (7,5),
                   font_size = 20,
                   network_name = None):
    

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
    ticks_font_size = 18

    duration = ts_edges_dist_df['ts'].tolist()
    timestamps = [i for i in range(len(duration))]
    print(timestamps[int(0.85 * len(timestamps))])
    # timestamps = ts_edges_dist_df['ts'].tolist()
    
    new = ts_edges_dist_df['new'].tolist()
    repeated = ts_edges_dist_df['repeated'].tolist()

    # plotting stuffs
    # bar plot
    plt.bar(timestamps, repeated, label='Repeated', color='#404040', alpha=0.4)
    plt.bar(timestamps, new, label='New', bottom=repeated, color='#ca0020', alpha=0.8, hatch='//')
    # test split line
    plt.axvline(x=(timestamps[int(0.85 * len(timestamps))]), color="blue", linestyle="--", linewidth=2)
    plt.text((timestamps[int(0.85 * len(timestamps))]), 0,
             'x', va='center', ha='center', fontsize=font_size, fontweight='heavy', color='blue')

    plt.margins(x=0)
    plt.xlabel("Timestamp", fontsize=font_size)
    plt.ylabel("Number of edges", fontsize=font_size)
    plt.legend()
    plt.savefig(f"{filepath}/{network_name}.png")
    plt.close()


# TET Plot

# some parameters to be used for drawing
E_ABSENT = 0
E_PRESENCE_GENERAL = 1
E_SEEN_IN_TRAIN = 2
E_IN_TEST = 3
E_NOT_IN_TEST = 4

TEST_RATIO = 0.15

# new color controlling parameters; Date: Dec. 22, 2021
E_ONLY_TRAIN = 10
E_TRAIN_AND_TEST = 20
E_TRANSDUCTIVE = 30
E_INDUCTIVE = 40

def TET(temp_edgelist, 
        filepath, 
        network_name=None,
        add_frame = True,
        figsize = (9, 5),
        axis_title_font_size = 20,
        ticks_font_size = 22,
        axis_tick_gap = 20,
        timestamp_split_cross_mark_offset = 1) -> pd.DataFrame:
    
    edge_last_ts = generate_edge_last_timestamp(temp_edgelist)
    edge_idx_map = generate_edge_idx_map(temp_edgelist, edge_last_ts)
    idx_edge_map = {v: k for k, v in edge_idx_map.items()}  # key: edge index; value: actual edge (source, destination)
    print("Info: Number of distinct edges (from index-edge map): {}".format(len(idx_edge_map)))

    unique_ts_list = list(temp_edgelist.keys())
    e_presence_mat = generate_edge_presence_matrix(unique_ts_list, idx_edge_map, edge_idx_map, temp_edgelist)
    e_presence_mat, test_split_ts_value = process_presence_matrix(e_presence_mat, test_ratio_p=0.85)
    print("Info: edge-presence-matrix shape: {}".format(e_presence_mat.shape))

    fig_param = set_fig_param(network_name, filepath,
                              figsize = figsize,
                              axis_title_font_size = axis_title_font_size,
                              ticks_font_size = ticks_font_size,
                              axis_tick_gap = axis_tick_gap,
                              timestamp_split_cross_mark_offset = timestamp_split_cross_mark_offset)

    plot_edge_presence_matrix(e_presence_mat, test_split_ts_value, unique_ts_list, list(idx_edge_map.keys()),
                              fig_param, add_frames=add_frame)
    return 


def generate_edge_last_timestamp(edges_per_ts):
    """generates a dictionary containing the last timestamp of each edge"""
    edge_last_ts = {}
    for ts, e_list in edges_per_ts.items():
        for e in e_list:
            if e not in edge_last_ts:
                edge_last_ts[e] = ts
            else:
                edge_last_ts[e] = max(ts, edge_last_ts[e])
    return edge_last_ts


def generate_edge_idx_map(edges_per_ts, edge_last_ts):
    """
    generates index for edges according to two-level sorting policy:
    1. the first level is based on their first appearance timestamp
    2. the second level is based on their last appearance timestamp
    """
    edge_idx_map = {}  # key: actual edge (source, destination), value: edge index
    distinct_edge_idx = 0
    for ts, ts_e_list in edges_per_ts.items():
        e_last_ts_this_timestamp = {}
        for e in ts_e_list:
            e_last_ts_this_timestamp[e] = edge_last_ts[e]
        e_last_ts_this_timestamp = dict(sorted(e_last_ts_this_timestamp.items(), key=lambda item: item[1]))
        for e in e_last_ts_this_timestamp:
            if e not in edge_idx_map:
                edge_idx_map[e] = distinct_edge_idx
                distinct_edge_idx += 1

    return edge_idx_map


def generate_edge_presence_matrix(unique_ts_list, idx_edge_map, edge_idx_map, edges_per_ts):
    num_unique_ts = len(unique_ts_list)
    num_unique_edge = len(idx_edge_map)
    e_presence_mat = np.zeros([num_unique_ts, num_unique_edge], dtype=np.int8)
    unique_ts_list = np.sort(unique_ts_list)

    for x, ts in tqdm(enumerate(unique_ts_list)):
        es_ts = edges_per_ts[ts]
        for e in es_ts:
            e_presence_mat[num_unique_ts - x - 1, edge_idx_map[e]] = E_PRESENCE_GENERAL

    return e_presence_mat

def process_presence_matrix(e_presence_matrix, test_ratio_p):
    """
    there are 4 types of edge presence:
    1. only in train
    2. in train and in test
    3. in test and train (which is the number 2 but in later timestamps)
    4. only in test
    X: timestamp
    Y: edge index
    """
    num_unique_ts = e_presence_matrix.shape[0]
    num_unique_edges = e_presence_matrix.shape[1]
    ts_idx_list = [i for i in range(num_unique_ts)]
    test_split_ts_value = int(np.quantile(ts_idx_list, test_ratio_p))
    train_ts_list = [ts for ts in ts_idx_list if ts <= test_split_ts_value]  # any timestamp in train/validation split
    test_ts_list = [ts for ts in ts_idx_list if ts > test_split_ts_value]  # test_split_ts_value is in train
    # first level processing: differentiate train set edges: 1) Only in train set, 2) in train & test set
    for tr_ts in tqdm(train_ts_list):
        for eidx in range(num_unique_edges):
            if e_presence_matrix[num_unique_ts - tr_ts - 1, eidx] == E_PRESENCE_GENERAL:
                for test_ts_idx in range(test_split_ts_value + 1, num_unique_ts):
                    if e_presence_matrix[num_unique_ts - test_ts_idx - 1, eidx] == E_PRESENCE_GENERAL:  # if seen in
                        # the test set
                        e_presence_matrix[num_unique_ts - tr_ts - 1, eidx] = E_TRAIN_AND_TEST
                        break
    # differentiate test set edges: 1) transductive (seen in train, repeating in test), 2) inductive (only in test)
    for ts in test_ts_list:
        for eidx in range(num_unique_edges):
            if e_presence_matrix[num_unique_ts - ts - 1, eidx] == E_PRESENCE_GENERAL:
                for prev_ts_idx in range(test_split_ts_value, -1, -1):
                    if e_presence_matrix[num_unique_ts - prev_ts_idx - 1, eidx] == E_TRAIN_AND_TEST:  # if seen in
                        # the training set
                        e_presence_matrix[num_unique_ts - ts - 1, eidx] = E_TRANSDUCTIVE
                        break
    # second level processing
    for ts in range(num_unique_ts):
        for eidx in range(num_unique_edges):
            if ts <= test_split_ts_value:
                if e_presence_matrix[num_unique_ts - ts - 1, eidx] == E_PRESENCE_GENERAL:
                    e_presence_matrix[num_unique_ts - ts - 1, eidx] = E_ONLY_TRAIN
            else:
                if e_presence_matrix[num_unique_ts - ts - 1, eidx] == E_PRESENCE_GENERAL:
                    e_presence_matrix[num_unique_ts - ts - 1, eidx] = E_INDUCTIVE

    return e_presence_matrix, test_split_ts_value


def plot_edge_presence_matrix(e_presence_mat, test_split_ts_value, unique_ts_list,
                              idx_edge_list, fig_param, add_frames=True):
    print("Info: plotting edge presence heatmap for {} ...".format(fig_param.fig_name))

    fig, ax = plt.subplots(figsize=fig_param.figsize)
    plt.subplots_adjust(bottom=0.3, left=0.2)

    # colors = ['white',  # E_ABSENCE
    #           '#67a9cf',  # E_ONLY_TRAIN
    #           '#ef8a62',  # E_TRAIN_AND_TEST
    #           '#ef8a62',  # E_TRANSDUCTIVE
    #           '#b2182b'  # E_INDUCTIVE
    #           ]
    colors = ['white',  # E_ABSENCE
              '#018571',  # E_ONLY_TRAIN    2c7bb6
              '#fc8d59',  # E_TRAIN_AND_TEST
              '#fc8d59',  # E_TRANSDUCTIVE
              '#b2182b'  # E_INDUCTIVE
              ]

    frame_color = "grey" # "#bababa"
    time_split_color = "black"
    axis_title_font_size = fig_param.axis_title_font_size
    x_font_size = fig_param.ticks_font_size
    y_font_size = fig_param.ticks_font_size

    ax = sns.heatmap(e_presence_mat, cmap=sns.color_palette(colors, as_cmap=True), cbar=False)

    # processing x-axis
    x_gaps = np.linspace(0, len((idx_edge_list)), num=5)
    x_labels = x_gaps / len(idx_edge_list)
    x_labels = [int(100*x) for x in x_labels]
    plt.xticks(x_gaps, x_labels, rotation=0, fontsize=x_font_size)

    # processing y-axis
    t_gaps = np.linspace(0, len(unique_ts_list), num=5)
    t_labels = [int(len(unique_ts_list) - tidx) for tidx in t_gaps]
    plt.yticks(t_gaps, t_labels, rotation=90, fontsize=y_font_size)

    # axis & title
    # plt.margins(x=0)
    plt.xlabel("Percentage of observed edges", fontsize=axis_title_font_size)
    plt.ylabel("Timestamp", fontsize=axis_title_font_size)

    # requirements for additional features
    x_length = e_presence_mat.shape[1] - 1
    y_length = e_presence_mat.shape[0] - 1
    test_split_idx_value = y_length - test_split_ts_value
    e_border_idx = 0
    for e_idx in range(e_presence_mat.shape[1] - 1, -1, -1):
        if e_presence_mat[y_length - test_split_ts_value, e_idx] != E_ABSENT:
            e_border_idx = e_idx
            break

    # rectangle for different parts of the dataset
    if add_frames:
        print("Info: Border edge index:", e_border_idx)
        print("Info: Test split timestamp value:", test_split_ts_value)
        rect_train = plt.Rectangle((0, y_length - test_split_ts_value + 0.085), e_border_idx, test_split_ts_value + 0.9,
                                   fill=False, linewidth=2, edgecolor=frame_color)
        rect_test_mayseen = plt.Rectangle((0, 0), e_border_idx, y_length - test_split_ts_value - 0.1,
                                          fill=False, linewidth=2, edgecolor=frame_color)
        rect_test_new = plt.Rectangle((e_border_idx, 0), x_length - e_border_idx,
                                      y_length - test_split_ts_value - 0.1,
                                      fill=False, linewidth=2, edgecolor=frame_color)
        ax = ax or plt.gca()
        ax.add_patch(rect_train)
        ax.add_patch(rect_test_mayseen)
        ax.add_patch(rect_test_new)

    # test split horizontal line
    plt.axhline(y=test_split_idx_value, color=time_split_color, linestyle="--", linewidth=2, label='x')
    plt.text(x=0, y=test_split_idx_value, s='x', color=time_split_color, va='center', ha='center',
             fontsize=y_font_size, fontweight='heavy')

    if fig_param.fig_name != "":
        # print("Info: file name: {}".format(fig_param.fig_name))
        plt.savefig(f"{fig_param.fig_name}/{fig_param.network_name}.png")
        plt.close()

    plt.show()
    print("Info: plotting done!")

def set_fig_param(network_name, fig_name,
                  figsize = (9, 5),
                  axis_title_font_size = 20,
                  ticks_font_size = 22,
                  axis_tick_gap = 20,
                  timestamp_split_cross_mark_offset = 1):

    # if network_name in ['US Legislative', 'Canadian Vote', 'UN Trade', 'UN Vote']:
    #     axis_tick_gap = axis_tick_gap * 0.35

    # elif network_name in ['Reddit', 'Wikipedia', 'UCI', 'Social Evo.', 'Flights', 'LastFM', 'MOOC']:
    #     axis_tick_gap = axis_tick_gap * 0.5

    # elif network_name in ['Enron']:
    #     axis_tick_gap = axis_tick_gap * 0.4

    fig_param = Fig_Param(network_name,
                          fig_name,
                          figsize, 
                          axis_title_font_size,
                          ticks_font_size,
                          axis_tick_gap,
                          timestamp_split_cross_mark_offset)

    return fig_param

class Fig_Param:
    def __init__(self, network_name, fig_name, figsize, axis_title_font_size, ticks_font_size, axis_tick_gap,
                 timestamp_split_cross_mark_offset):
        self.network_name = network_name
        self.fig_name = fig_name
        self.figsize = figsize
        self.axis_title_font_size = axis_title_font_size
        self.ticks_font_size = ticks_font_size
        self.axis_tick_gap = axis_tick_gap
        self.timestamp_split_cross_mark_offset = timestamp_split_cross_mark_offset