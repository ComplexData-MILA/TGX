import pandas as pd
from typing import Union
import csv
import numpy as np
from typing import Optional, Union
from tgx.utils.graph_utils import edgelist_discritizer
# from tgx.datasets.data_loader import read_dataset


def read_edgelist(fname: Union[str, None] = None, 
             data: Union[object, None] = None,
             sep: str = ",", 
             header: bool = True,
             index: bool = False,
             discretize: bool = False,
             intervals: Union[str, int, None] = None,
             t_col: int = 2, 
             ts_sorted: bool = True,
             max_intervals: int = 200,
             weight: bool = False, 
             edge_feat: bool = False,
             feat_size: int = 0) -> dict:
    
    """
    Read temporal edgelist and store it in a dictionary.
    Parameters:
        fname: directory of a dataset in .csv format
        data: data object created from loading dgb/tgb datasets 
        sep: data seperators in the data file
        header: whether first line of data file is header
        index: whether the first column is row indices
        discretize: whether to discretize the data
        intervals: to discretize data based on "daily", "weekly", "monthly" or "yearly" or give the number of intervals
        t_col: column indext for timestamps (0 or 2)
        ts_sorted: if data are sorted based on timestamp
        max_intervals: maximum number of intervals to discretize data

    Returns:
        temp_edgelist: A dictionary of edges and their frequency at each time interval
    """
    
    start_col = 0
    # weight_col = np.inf
    # feat_col = np.inf

    
    if not ts_sorted:
        raise NotImplementedError("Only implemented for sorted data.")


    if data is not None:
        if isinstance(data, type):
            return _datasets_edgelist_loader(data.data, 
                                             discretize = discretize, 
                                             intervals = intervals,
                                             max_intervals=max_intervals)
        else:
            raise TypeError("Invalid data type, try data class")

    if index:
        start_col = 1
        t_col += 1

    if t_col < 2:
        u_col = t_col + 1
    else:
        u_col = start_col
    v_col = u_col + 1


    # if weight:
    #     weight_col = start_col + 3
    #     start_col += 1

    # if edge_feat:
    #     feat_col = int(start_col + 3) 
    
    # if edge_feat and feat_size == 0:
    #     print("Calculating number of features ...")
    #     line_len = [l for i, l in enumerate(csv.reader(open(fname), delimiter=sep)) if i == 2]
    #     feat_size = len(line_len[0]) - (start_col + 3)
    #     print("Number of features: ", feat_size)

    cols_to_read = [u_col, v_col, t_col]

   
    temp_edgelist = _load_edgelist(fname, cols_to_read, header=header)
    if discretize:
        unique_ts = list(temp_edgelist.keys())
        return edgelist_discritizer(temp_edgelist,
                                    unique_ts=unique_ts,
                                    time_interval=intervals,
                                    max_intervals=max_intervals)
    
    return temp_edgelist

def _load_edgelist(fname, columns, header):
    """
    read edges from the file and store them in a dictionary
    Parameters:
        fname: file address
        columns: order of the nodes and timestamp
        header: Whether the data file contains header
    """
    edgelist = open(fname, "r")
    edgelist.readline()
    lines = list(edgelist.readlines())
    edgelist.close()
    
    
    u_idx, v_idx, ts_idx = columns
    temp_edgelist = {}
    unique_edges = {}
    total_edges = 0
    if header:
        first_line = 1
    else:
        first_line = 0
    for i in range(first_line, len(lines)):
        line = lines[i]
        values = line.split(',')
        t = int(float(values[ts_idx]))
        u = values[u_idx]
        v = values[v_idx]

        if t not in temp_edgelist:
            temp_edgelist[t] = {}
            temp_edgelist[t][(u, v)] = 1
            
        else:
            if (u, v) not in temp_edgelist[t]:
                temp_edgelist[t][(u, v)] = 1
            else:
                temp_edgelist[t][(u, v)] += 1
        
        if (u,v) not in unique_edges:
            unique_edges[(u, v)] = 1

        total_edges += 1

    print("Number of loaded edges: " + str(total_edges))
    print("Number of unique edges:" + len(unique_edges.keys()))
    print("Available timestamps: ", len(temp_edgelist.keys()))
    return temp_edgelist

def _datasets_edgelist_loader(data, 
                              discretize=False, 
                              intervals : int = 200, 
                              max_intervals=200) -> dict:
    """
    load built-in datasets and tgb datasets
    """
    temp_edgelist = {}
    total_edges = 0
    unique_edges = {}
    for line in data:
        u = line[0]
        v = line[1]
        t = int(float(line[2]))
        
        if t not in temp_edgelist:
            temp_edgelist[t] = {}
            temp_edgelist[t][(u, v)] = 1
        else:
            if (u, v) not in temp_edgelist[t]:
                temp_edgelist[t][(u, v)] = 1
            else:
                temp_edgelist[t][(u, v)] += 1
        
        if (u,v) not in unique_edges:
            unique_edges[(u,v)] = 1
        total_edges += 1
    print("Number of loaded edges: " + str(total_edges))
    print("Number of unique edges:" + str(len(unique_edges.keys())))
    print("Available timestamps: ", len(temp_edgelist.keys()))

    if discretize:
        unique_ts = list(temp_edgelist.keys())
        return edgelist_discritizer(temp_edgelist,
                                    unique_ts=unique_ts,
                                    time_interval=intervals,
                                    max_intervals=max_intervals)
    
    return temp_edgelist


def _load_edgelist_with_discretizer(
        fname : str, 
        columns : list, 
        time_interval : Union[str , int] = 86400, 
        header : Optional[bool] = True):
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

    if isinstance(time_interval, str):
        if time_interval == "daily":
            interval_size = 86400
        elif time_interval == "weekly":
            interval_size = 86400 * 7
        elif time_interval == "monthly":
            interval_size = 86400 * 30
        elif time_interval == "yearly":
            interval_size = 86400* 365
    elif isinstance(time_interval, int):
        if time_interval > 100:
            raise ValueError("The maximum number of time intervals is {max_intervals}.")
        else:
            last_line = lines[-1]
            values = last_line.split(',')
            total_time = float(values[ts_idx])
            interval_size = int(total_time / (time_interval-1))
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




