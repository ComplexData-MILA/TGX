import pandas as pd
import csv
from tqdm import tqdm
import numpy as np
import time
from tgn.datasets.data_loader import read_dataset

def read_edgelist(fname = None, 
             data = None,
             sep = ",", 
             header = True,
             index = False,
             continuous = False,
             intervals = None,
             t_col = 2, 
             weight = False, 
             edge_feat = False,
             feat_size = 0,
             reindex_nodes = False,
             return_csv = False):
    

    start_col = 0
    weight_col = np.inf
    feat_col = np.inf

    if data is not None:
        if isinstance(data, str):
            fname, header, index, continuous, intervals = read_dataset(data)
        else:
            raise TypeError("Invalid data name type, try string")

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
        # print(feat_col)   
    
    if edge_feat and feat_size == 0:
        print("Calculating number of features ...")
        line_len = [l for i, l in enumerate(csv.reader(open(fname), delimiter=sep)) if i == 2]
        feat_size = len(line_len[0]) - (start_col + 3)
        print("Number of features: ", feat_size)

    # feat_l = np.zeros((num_lines, feat_size))
    cols_to_read = [u_col, v_col, t_col, weight_col, feat_col]

    if continuous:
        return load_continuous_edgelist(fname, cols_to_read, time_interval=intervals, header=header)
    else:
        return load_discrete_edgelist(fname, cols_to_read, header=header)


def load_continuous_edgelist(fname, columns, time_interval=86400, header=True):
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

    u_idx, v_idx, ts_idx, _, _ = columns

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
            interval_size = int(total_time / time_interval)
    else:
        raise TypeError("Invalid time interval")

    temporal_edgelist = {}
    total_n_edges = 0
    # with open(fname) as f:
    #     if header:
    #         s = next(f)  # skip the first line
    #     for idx, line in enumerate(f):
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

def load_discrete_edgelist(fname, columns, header):
    """
    treat each year as a timestamp
    """
    edgelist = open(fname, "r")
    edgelist.readline()
    lines = list(edgelist.readlines())
    edgelist.close()

    u_idx, v_idx, ts_idx, _, _ = columns
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
    # print("Available timestamps: ", temp_edgelist.keys())
    # print(temp_edgelist.values())
    return temp_edgelist


def csv_loader(fname, sep, header, columns, reindex_nodes, weight, edge_feat, feat_size=0):

    node_ids = {}
    num_lines = sum(1 for line in open(fname)) - 1
    u_list = np.zeros(num_lines)
    v_list = np.zeros(num_lines)
    ts_list = np.zeros(num_lines)
    w_list = np.zeros(num_lines)
    feat_l = np.zeros((num_lines, feat_size))

    u_col, v_col, t_col, weight_col, feat_col = columns
    
    with open(fname, "r") as csv_file:
        print("Reading file ...")
        csv_reader = csv.reader(csv_file, delimiter=sep)
        idx = 0
        for i, row in enumerate(csv_reader):
                if header and idx == 0:
                    idx += 1
                    continue
                elif not header and idx == 0:
                    idx = 1
                src = row[u_col]
                dst = row[v_col]
                ts = row[t_col]

                if reindex_nodes:
                    if src not in node_ids:
                        node_ids[src] = node_uid
                        node_uid += 1
                    if dst not in node_ids:
                        node_ids[dst] = node_uid
                        node_uid += 1
                    
                    u_list[idx-1] = int(node_ids[src])
                    v_list[idx-1] = int(node_ids[dst])
                else:
                    u_list[idx-1] = int(src)
                    v_list[idx-1] = int(dst)

                

                if weight and edge_feat:
                    w_list[idx-1] = row[weight_col]
                    feat_l[idx-1,:] = np.array(row[feat_col:])
                elif edge_feat:
                    feat_l[idx-1,:] = np.array(row[feat_col:])
                elif weight:
                    w_list[idx-1] = row[weight_col]
                
                ts_list[idx-1] = int(ts)
                idx += 1
        if weight:
            df = pd.DataFrame({"u": u_list,
                                "v": v_list,
                                "ts": ts_list,
                                "w": w_list})
        else:
            df = pd.DataFrame({"u": u_list,
                                "v": v_list,
                                "ts": ts_list})
        # print(df.head())
            
if __name__ == "__main__":
    # a = load_UN_temporarl_edgelist("/home/mila/r/razieh.shirzadkhani/tgx/data/UNtrade/UNtrade.csv")
    # print(a)

    read_edgelist(data=3,
                  header=True,return_csv=True)
    # read_edgelist("./data/full_clean_data_daily_agg.csv",
    #               t_col=0,
    #               weight=True)


    # read_edgelist("./data/ml_enron.csv",
    #               header=True,
    #               index=True)

    # read_edgelist("/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
    #               "python3.9/site-packages/tgb/datasets/tgbl_wiki/tgbl-wiki_edgelist_v2.csv", 
    #               header=True, 
    #               edge_feat=True,
    #               feat_size=173)

    # read_edgelist("/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
    #             "python3.9/site-packages/tgb/datasets/tgbl_review/tgbl-review_edgelist_v2.csv", 
    #             header=True, 
    #             t_col=0,
    #             weight=True)
    # dd = pd.read_csv("./data/ml_enron.csv", columns=["u", "i", "ts"])
