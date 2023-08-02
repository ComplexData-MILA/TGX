import pandas as pd
import csv
from tqdm import tqdm
import numpy as np
import time

class Dataloader():

    def __init__(self, datapath, sep, columns = None, names = None, header = None):
        self.datapath = datapath
        self.sep = sep
        self.columns = columns
        self.names = names
        self.header = header

def read_edgelist(fname, 
             sep = ",", 
             header = False,
             index = False,
             t_col = 2, 
             weight = False, 
             edge_feat = False,
             feat_size = 0,
             reindex_nodes = False):
    
    num_lines = sum(1 for line in open(fname)) - 1
    u_list = np.zeros(num_lines)
    v_list = np.zeros(num_lines)
    ts_list = np.zeros(num_lines)
    w_list = np.zeros(num_lines)
    node_ids = {}
    node_uid = 0
    start_col = 0
    weight_col = 0

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
        print(feat_col)   
    
    if edge_feat and feat_size == 0:
        print("Calculating number of features ...")
        line_len = [l for i, l in enumerate(csv.reader(open(fname), delimiter=sep)) if i == 2]
        feat_size = len(line_len[0]) - (start_col + 3)
        print("Number of features: ", feat_size)

    feat_l = np.zeros((num_lines, feat_size))
    

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
        print(df.head())    
        return df, feat_l



    # print("csv took %s seconds" % (time.time() - start_time))
    # start_time = time.time()
    # df = pd.read_csv(fname)
    # print("pd took %s seconds" % (time.time() - start_time))

# read_edgelist("./data/contact.csv",
#               header=True,
#               weight=True)

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

read_edgelist("/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
              "python3.9/site-packages/tgb/datasets/tgbl_review/tgbl-review_edgelist_v2.csv", 
              header=True, 
              t_col=0,
              weight=True)
# dd = pd.read_csv("./data/ml_enron.csv", columns=["u", "i", "ts"])
