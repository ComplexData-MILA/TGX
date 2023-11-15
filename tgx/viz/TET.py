# TET Plot
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm
from typing import Union, Optional
import matplotlib.pyplot as plt
from tgx.utils.graph_utils import edgelist_discritizer


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

def TET(temp_edgelist : Union[object, dict],
        filepath: Optional[str] = ".", 
        intervals : Union[str, int] = None,
        network_name : str = None,
        add_frame : bool = True,
        test_split : bool = False,
        figsize : tuple = (9, 5),
        axis_title_font_size : int = 20,
        ticks_font_size : int = 20,
        max_intervals : int = 200,
        show: bool = True):
    r"""
    Generate TET plots
    Args:
        temp_edgelist: a dictionary of temporal edges or a dataset object.
        filepath: Path to save the TEA Plot.
        figsize: Size of the figure to save.
        axis_title_font_size: The font size of xis titles.
        ticks_font_size: Size of the text in the figure.
        add_frame: Add the frame to the plot.
        network_name: Name of the dataset to be used in the TEA plot file.
        intervals: intervals for discretizing data if already not done.
        test_split: Whether show the test split on the plot.
        max_intervals: Maximum number of intervals to discretize data.
        show: Whether to show the plot.
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
    
    edge_last_ts = generate_edge_last_timestamp(temp_edgelist)
    edge_idx_map = generate_edge_idx_map(temp_edgelist, edge_last_ts)
    idx_edge_map = {v: k for k, v in edge_idx_map.items()}  # key: edge index; value: actual edge (source, destination)
    print("Info: Number of distinct edges (from index-edge map): {}".format(len(idx_edge_map)))

    unique_ts_list = list(temp_edgelist.keys())
    e_presence_mat = generate_edge_presence_matrix(unique_ts_list, idx_edge_map, edge_idx_map, temp_edgelist)
    print("Info: edge-presence-matrix shape: {}".format(e_presence_mat.shape))
    # print(np.unique(e_presence_mat, return_counts=True))
    e_presence_mat, test_split_ts_value = process_presence_matrix(e_presence_mat, test_ratio_p=0.85)
    print("Info: edge-presence-matrix shape: {}".format(e_presence_mat.shape))
    # print(np.unique(e_presence_mat, return_counts=True))
    fig_param = set_fig_param(network_name, 
                              fig_name = filepath,
                              figsize = figsize,
                              axis_title_font_size = axis_title_font_size,
                              ticks_font_size = ticks_font_size)

    plot_edge_presence_matrix(e_presence_mat, test_split_ts_value, unique_ts_list, list(idx_edge_map.keys()),
                              fig_param, test_split = test_split, add_frames=add_frame, show=show)
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
    '''
    Returns presence matrix with values 0 and 1 which indicate:
    value = 0 : edge is not present in this timestamp
    value = 1 : edge is present in this timestamp

    shape: (ts, total number of edges)
    '''
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

    # generating timestamp list for train and test:
    test_split_ts_value = int(np.quantile(ts_idx_list, test_ratio_p))
    train_ts_list = [ts for ts in ts_idx_list if ts <= test_split_ts_value]  # any timestamp in train/validation split
    test_ts_list = [ts for ts in ts_idx_list if ts > test_split_ts_value]  # test_split_ts_value is in train

    # first level processing: differentiate train set edges: 1) Only in train set, 2) in train & test set
    print("First level processing: ")
    print("Detecting edges present in train & test sets")
    for tr_ts in tqdm(train_ts_list):
        for eidx in range(num_unique_edges):
            if e_presence_matrix[num_unique_ts - tr_ts - 1, eidx] == E_PRESENCE_GENERAL:
                for test_ts_idx in range(test_split_ts_value + 1, num_unique_ts):
                    if e_presence_matrix[num_unique_ts - test_ts_idx - 1, eidx] == E_PRESENCE_GENERAL:  # if seen in
                        # the test set
                        e_presence_matrix[num_unique_ts - tr_ts - 1, eidx] = E_TRAIN_AND_TEST
                        break

    # differentiate test set edges: 1) transductive (seen in train, repeating in test), 2) inductive (only in test)
    print("Detecting transductive edges (seen in train, repeating in test)")
    for ts in tqdm(test_ts_list):
        for eidx in range(num_unique_edges):
            if e_presence_matrix[num_unique_ts - ts - 1, eidx] == E_PRESENCE_GENERAL:
                for prev_ts_idx in range(test_split_ts_value, -1, -1):
                    if e_presence_matrix[num_unique_ts - prev_ts_idx - 1, eidx] == E_TRAIN_AND_TEST:  # if seen in
                        # the training set
                        e_presence_matrix[num_unique_ts - ts - 1, eidx] = E_TRANSDUCTIVE
                        break

    # second level processing
    print("Second level processing:")
    print("Detecting edges 1) Only in train set, 2) only in test (inductive)")
    for ts in tqdm(range(num_unique_ts)):
        for eidx in range(num_unique_edges):
            if ts <= test_split_ts_value:
                if e_presence_matrix[num_unique_ts - ts - 1, eidx] == E_PRESENCE_GENERAL:
                    e_presence_matrix[num_unique_ts - ts - 1, eidx] = E_ONLY_TRAIN
            else:
                if e_presence_matrix[num_unique_ts - ts - 1, eidx] == E_PRESENCE_GENERAL:
                    e_presence_matrix[num_unique_ts - ts - 1, eidx] = E_INDUCTIVE

    return e_presence_matrix, test_split_ts_value


def plot_edge_presence_matrix(e_presence_mat, 
                              test_split_ts_value, 
                              unique_ts_list,
                              idx_edge_list, 
                              fig_param, 
                              test_split = False, 
                              add_frames=True,
                              show=False):
    print("Info: plotting edge presence heatmap for {} ...".format(fig_param.fig_name))

    fig, ax = plt.subplots(figsize=fig_param.figsize)
    plt.subplots_adjust(bottom=0.3, left=0.2)

    # colors = ['white',  # E_ABSENCE
    #           '#67a9cf',  # E_ONLY_TRAIN
    #           '#ef8a62',  # E_TRAIN_AND_TEST
    #           '#ef8a62',  # E_TRANSDUCTIVE
    #           '#b2182b'  # E_INDUCTIVE
    #           ]
    if test_split:
        colors = ['white',  # E_ABSENCE
                '#018571',  # E_ONLY_TRAIN    2c7bb6
                '#fc8d59',  # E_TRAIN_AND_TEST
                '#fc8d59',  # E_TRANSDUCTIVE
                '#b2182b'  # E_INDUCTIVE
                ]
    else:
        colors = ['white',
                  '#ca0020',
                  '#ca0020',
                  '#ca0020',
                  '#ca0020',]
    # print(sns.color_palette(colors, as_cmap=True))
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
    if add_frames and test_split:
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
    
    elif add_frames:
        ax.add_patch(plt.Rectangle((0, 0), x_length, y_length+1,
                                          fill=False, linewidth=2, edgecolor=frame_color))
    # test split horizontal line
    if test_split:
        plt.axhline(y=test_split_idx_value, color=time_split_color, linestyle="--", linewidth=2, label='x')
        plt.text(x=0, y=test_split_idx_value, s='x', color=time_split_color, va='center', ha='center',
                fontsize=y_font_size, fontweight='heavy')

    if fig_param.fig_name is not None:
        # print("Info: file name: {}".format(fig_param.fig_name))
        plt.savefig(f"{fig_param.fig_name}/{fig_param.network_name}.pdf")
    plt.show()
    print("Info: plotting done!")

def set_fig_param(network_name, fig_name = None,
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