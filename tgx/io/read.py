import pandas as pd
import csv
import numpy as np
from typing import Optional, Union
# from tgx.datasets.data_loader import read_dataset


#  data: Optional[object] = None,
#  is_discretized: bool = False,
#  discretize: bool = False,
#  time_scale: Union[str, int, None] = None,

def read_csv(fname: Union[str, object] = None, 
             header: bool = False,
             index: bool = False,
             t_col: int = 2,) -> dict:
    
    """
    Read temporal edgelist and store it in a dictionary.
    Parameters:
        fname: directory of a dataset in .csv format or data object created from loading dgb/tgb datasets 
        header: whether first line of data file is header
        index: whether the first column is row indices
        t_col: column indext for timestamps (0 or 2)
        ts_sorted: if data are sorted based on timestamp

    Returns:
        temp_edgelist: A dictionary of edges and their frequency at each time interval
    """
    
    start_col = 0
    if index:
        start_col = 1
        t_col += 1

    if t_col < 2:
        u_col = t_col + 1
    else:
        u_col = start_col
    v_col = u_col + 1

    cols_to_read = [u_col, v_col, t_col]

    if (isinstance(fname, str)):
        return _load_edgelist(fname, cols_to_read, header=header)
    elif isinstance(fname, type) or isinstance(fname, object):
        return _datasets_edgelist_loader(fname.data) 
    else:
        raise TypeError("Invalid input")


def _load_edgelist(fname, columns, header):
    """
    read edges from the file and store them in a dictionary
    Parameters:
        fname: file address
        columns: order of the nodes and timestamp
        header: Whether the data file contains header
    """
    try:
        edgelist = open(fname, "r")
    except:
        raise FileNotFoundError("No such file or directory.")
    edgelist.readline()
    lines = list(edgelist.readlines())
    edgelist.close()

    u_idx, v_idx, ts_idx = columns
    temp_edgelist = {}
    unique_edges = {}
    edges_list = []
    total_edges = 0
    sorted = True
    previous_t = 0
    if header:
        first_line = 1
    else:
        first_line = 0
    for i in range(first_line, len(lines)):
        line = lines[i]
        values = line.split(',')
        t = int(float(values[ts_idx]))
        u = values[u_idx].strip()
        v = values[v_idx].strip()
        
        if i == first_line:
            curr_t = t

        # Check if the dataset is sorted
        if t < previous_t:
            sorted = False
        previous_t = t

        if t not in temp_edgelist:
            temp_edgelist[t] = {}
        if (u, v) not in temp_edgelist[t]:
            temp_edgelist[t][(u, v)] = 1
        else:
            temp_edgelist[t][(u, v)] += 1

        # temp_edgelist[t].append((u, v))
        if (u,v) not in unique_edges:
            unique_edges[(u, v)] = 1
        total_edges += 1
    # temp_edgelist[curr_t] = edges_list
    
    if sorted is False:
        print("edgelist not sorted, sorting dataset...")
        myKeys = list(temp_edgelist.keys())
        myKeys.sort()
        temp_edgelist = {i: temp_edgelist[i] for i in myKeys}
        
    print("Number of loaded edges: " + str(total_edges))
    print("Number of unique edges:" , len(unique_edges.keys()))
    print("Available timestamps: ", len(temp_edgelist.keys()))
    return temp_edgelist

def _datasets_edgelist_loader(data) -> dict:
    """
    load built-in datasets and tgb datasets
    """
    temp_edgelist = {}
    total_edges = 0
    unique_edges = {}
    first_line = 0
    previous_t = 0
    edges_list = []
    sorted = True
    for line in data:
        u = line[0]
        v = line[1]
        t = int(float(line[2]))
        if first_line == 0:
            curr_t = t
            first_line += 1

        # Check if the dataset is sorted
        if t < previous_t:
            sorted = False
        previous_t = t

        if t != curr_t:
            temp_edgelist[curr_t] = edges_list
            edges_list = []
            curr_t = t

        edges_list.append((u, v))
        if (u,v) not in unique_edges:
            unique_edges[(u, v)] = 1
        total_edges += 1
    temp_edgelist[curr_t] = edges_list
    
    if sorted is False:
        print("Sorting dataset...")
        myKeys = list(temp_edgelist.keys())
        myKeys.sort()
        temp_edgelist = {i: temp_edgelist[i] for i in myKeys}

    print("Number of loaded edges: " + str(total_edges))
    print("Number of unique edges:" + str(len(unique_edges.keys())))
    print("Available timestamps: ", len(temp_edgelist.keys()))
    
    return temp_edgelist


def _load_edgelist_with_discretizer(
        fname : str, 
        columns : list, 
        time_scale : Union[str , int] = 86400, 
        header : Optional[bool] = True) -> dict:
    """
    load temporal edgelist into a dictionary
    assumption: the edges are ordered in increasing order of their timestamp
    '''
    the timestamp in the edgelist is based cardinal
    more detail see here: https://github.com/srijankr/jodie
    need to merge edges in a period of time into an interval
    86400 is # of secs in a day, good interval size
    '''
    """
    # print("Info: Interval size:", interval_size)
    edgelist = open(fname, "r")
    edgelist.readline()
    lines = list(edgelist.readlines())
    edgelist.close()

    
    u_idx, v_idx, ts_idx = columns

    if isinstance(time_scale, str):
        if time_scale == "daily":
            interval_size = 86400
        elif time_scale == "weekly":
            interval_size = 86400 * 7
        elif time_scale == "monthly":
            interval_size = 86400 * 30
        elif time_scale == "yearly":
            interval_size = 86400* 365
    elif isinstance(time_scale, int):
            last_line = lines[-1]
            values = last_line.split(',')
            total_time = float(values[ts_idx])
            interval_size = int(total_time / (time_scale-1))
    else:
        raise TypeError("Invalid time interval")

    temporal_edgelist = {}
    total_n_edges = 0
    
    if header:
        first_line = 1
    else:
        first_line = 0


    for i in range(first_line, len(lines)):
            line = lines[i]
            values = line.split(',')

            total_n_edges += 1
            # values = line.strip().split(',')
            u = values[u_idx]  # source node
            v = values[v_idx]  # destination node
            ts = float(values[ts_idx])  # timestamp
            ts_bin_id = int(ts / interval_size)
            if ts_bin_id not in temporal_edgelist:
                temporal_edgelist[ts_bin_id] = {}
                temporal_edgelist[ts_bin_id][(u, v)] = 1
            else:
                if (u, v) not in temporal_edgelist[ts_bin_id]:
                    temporal_edgelist[ts_bin_id][(u, v)] = 1
                else:
                    temporal_edgelist[ts_bin_id][(u, v)] += 1

    print("Loading edge-list: Maximum timestamp is ", ts)
    print("Loading edge-list: Maximum timestamp-bin-id is", ts_bin_id)
    print("Loading edge-list: Total number of edges:", total_n_edges)
    return temporal_edgelist




