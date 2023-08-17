import pandas as pd
import csv
import numpy as np
from typing import Optional, Union
from tgx.utils.edgelist import edgelist_discritizer
# from tgx.datasets.data_loader import read_dataset

def read_edgelist(fname : str = None, 
             data : type = None,
             sep = ",", 
             header = True,
             index = False,
             discretize = False,
             intervals = None,
             t_col = 2, 
             weight = False, 
             edge_feat = False,
             feat_size = 0,
             ts_sorted = True,
             reindex_nodes = False,
             return_csv = False):
    
    start_col = 0
    weight_col = np.inf
    feat_col = np.inf

    
    if not ts_sorted:
        raise NotImplementedError("Only implemented for sorted data.")


    if data is not None:
        if isinstance(data, type):
            return _datasets_edgelist_loader(data.data, 
                                             discretize = discretize, 
                                             intervals = intervals)
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


    if weight:
        weight_col = start_col + 3
        start_col += 1

    if edge_feat:
        feat_col = int(start_col + 3) 
    
    if edge_feat and feat_size == 0:
        print("Calculating number of features ...")
        line_len = [l for i, l in enumerate(csv.reader(open(fname), delimiter=sep)) if i == 2]
        feat_size = len(line_len[0]) - (start_col + 3)
        print("Number of features: ", feat_size)

    cols_to_read = [u_col, v_col, t_col]

    if discretize:
        return _load_edgelist_with_discretizer(fname, cols_to_read, time_interval=intervals, header=header)
    else:
        return _load_edgelist(fname, cols_to_read, header=header)


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
            raise ValueError("The maximum number of time intervals can be set to 100.")
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


def _load_edgelist(fname, columns, header):
    """
    treat each year as a timestamp
    """
    edgelist = open(fname, "r")
    edgelist.readline()
    lines = list(edgelist.readlines())
    edgelist.close()
    
    
    u_idx, v_idx, ts_idx = columns
    temp_edgelist = {}
    total_edges = 0
    if header:
        first_line = 1
    else:
        first_line = 0
    for i in range(first_line, len(lines)):
        line = lines[i]
        
        values = line.split(',')
        # print(values)
        
        t = int(float(values[ts_idx]))
        u = values[u_idx]
        v = values[v_idx]

        
        if t not in temp_edgelist:
            temp_edgelist[t] = {}
            temp_edgelist[t][(u, v)] = 1
            # print(temp_edgelist)
            # break
        else:
            if (u, v) not in temp_edgelist[t]:
                temp_edgelist[t][(u, v)] = 1
            else:
                temp_edgelist[t][(u, v)] += 1
        total_edges += 1
    print("Number of loaded edges: " + str(total_edges))
    print("Available timestamps: ", len(temp_edgelist.keys()))
    # print(temp_edgelist.values())
    return temp_edgelist

def _datasets_edgelist_loader(data, discretize=False, intervals : int = 100):
    temp_edgelist = {}
    total_edges = 0
    
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
        total_edges += 1
    print("Number of loaded edges: " + str(total_edges))
    print("Available timestamps: ", len(temp_edgelist.keys()))

    if discretize:
        unique_ts = list(temp_edgelist.keys())
        return edgelist_discritizer(temp_edgelist,
                                    unique_ts=unique_ts,
                                    time_interval=intervals)
    
    return temp_edgelist