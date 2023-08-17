from tgb.linkproppred.dataset import LinkPropPredDataset


from tgb.nodeproppred.dataset import NodePropPredDataset




name = "tgbn-genre"

dataset = NodePropPredDataset(name=name, root="datasets")


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