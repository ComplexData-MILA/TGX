# import networkx as nx
import copy
import csv
import numpy as np
from typing import Optional, Union
from tgx.utils.graph_utils import discretize_edges, frequency_count, subsampling
from tgx.io.read import read_csv

#TODO should contain a new property tracking the number of timestamps#TODO should contain a new property tracking the number of timestamps
class Graph(object):
    def __init__(self, 
                 dataset: Optional[object] = None, 
                 fname: Optional[str] = None,
                 edgelist: Optional[dict] = None):
        """
        Create a Graph object with specific characteristics
        Args:
            dataset: a dataset object
            edgelist: a dictionary of temporal edges in the form of {t: {(u, v), freq}}
        """

        if dataset is not None:
            if isinstance(dataset, type) or isinstance(dataset,object):
                #! not sure why read csv here
                self.data = read_csv(dataset)
        elif fname is not None and isinstance(fname, str):
            self.data = read_csv(fname)
        elif edgelist is not None and isinstance(edgelist, dict):
            self.data = edgelist
        else:
            raise TypeError("Please enter valid input.")
        
        self.subsampled_graph = None
        self.freq_data = None
        self.id_map = None #a map from original node id to new node id based on their order of appearance

    #TODO support edge features, edge weights, node features and more, currently supports, timestamp, source, destination
    def export_full_data(self):
        """
        convert self.data inot a dictionary of numpy arrays similar to TGB LinkPropPredDataset
        """
        num_edge = self.number_of_edges()
        sources = np.zeros(num_edge, dtype=np.int64)
        destinations = np.zeros(num_edge, dtype=np.int64)
        timestamps = np.zeros(num_edge, dtype=np.int64)
        idx = 0
        edgelist = self.data

        for ts, edge_data in edgelist.items():
            for u,v in edge_data.keys():
                sources[idx] = u
                destinations[idx] = v
                timestamps[idx] = ts
                idx += 1
        full_data = {
            "sources": sources,
            "destinations": destinations,
            "timestamps": timestamps,
        }
        return full_data

    def shift_time_to_zero(self) -> None:
        r"""
        shift all edges in the dataset to start with timestamp 0
        """
        min_t = list(self.data.keys())[0]
        new_data = {}
        for ts in self.data.keys():
            new_data[ts - min_t] = self.data[ts]
        self.data = new_data
        
    def discretize(self, 
                   time_scale: Union[str, int],
                   store_unix: bool = False,
                   freq_weight: bool = False) -> object:
        """
        discretize the graph object based on the given time interval
        Args:
            time_scale: time interval to discretize the graph
            store_unix: whether to store converted unix time in a list
            freq_weight: whether to weight the edges by frequency in the new graph object
        """
        new_G = copy.deepcopy(self)    
        # discretie differently based on # of intervals of time granularity
        output = discretize_edges(self.data,
                                    time_scale = time_scale,
                                    store_unix = store_unix,
                                    freq_weight = freq_weight)
        disc_G = output[0]
        new_G.data = disc_G
        if (store_unix):
            return new_G, output[1]
        else:
            return (new_G, )

    def count_freq(self):
        self.freq_data = frequency_count(self.data)
        return self

    def subsampling(self, 
                    node_list: Optional[list] = [], 
                    random_selection: Optional[bool] = True, 
                    N: Optional[int] = None) -> object:
        new_G = copy.deepcopy(self) 
        new_G.data = subsampling(new_G, node_list = node_list, random_selection=random_selection, N=N)
        return new_G

    def number_of_edges(self) -> int:
        r"""
        Calculate total number of nodes present in an edgelist
        """
        edgelist = self.data
        e_num = 0
        for _, edges in edgelist.items():
            e_num += len(edges)
        
        return e_num

    def unique_edges(self) -> int:
        r"""
        Calculate the number of unique edges
        Parameters:
        graph_edgelist: Dictionary containing graph data
        """
        unique_edges = {}
        for _, e_list in self.data.items():
            for e in e_list:
                if e not in unique_edges:
                    unique_edges[e] = 1
        return len(unique_edges)
    

    def total_nodes(self) -> int:
        r"""
        Calculate total number of unique nodes present in an edgelist
        """
        edgelist = self.data
        node_list = {}
        for _, edge_data in edgelist.items():
            for u,v in edge_data.keys():
                if u not in node_list:
                    node_list[u] = 1
                if v not in node_list:
                    node_list[v] = 1
        return len(node_list)
    

    def max_nid(self) -> int:
        r"""
        find the largest node ID in the dataset
        """
        edgelist = self.data
        max_id = 0
        for _, edge_data in edgelist.items():
            for u,v in edge_data.keys():
                if u > max_id:
                    max_id = u
                if v > max_id:
                    max_id = v
        return max_id + 1 #offset by 1
    
    def map_nid(self) -> dict:
        r"""
        remap all node ids in the dataset to start from 0 and based on node order of appearance. Also updates self.data
        Output: 
            id_map: a dictionary mapping original node id to new node id
        """
        edgelist = self.data
        id_map = {}
        nid = 0
        new_edgelist = {}
        for ts, edge_data in edgelist.items():
            new_edgelist[ts] = {}
            for u,v in edge_data.keys():
                if u not in id_map:
                    id_map[u] = nid
                    nid += 1
                if v not in id_map:
                    id_map[v] = nid
                    nid += 1
                new_edgelist[ts][(id_map[u],id_map[v])] = edge_data[(u,v)]
        self.data = new_edgelist
        return id_map


    def node_per_ts(self):
        active_nodes = {}
        for ts in range(len(self.data)):
            edgelist_t = self.data[ts]
            active_nodes.append(self.edgelist_node_count(edgelist_t))
        return active_nodes

    def edgelist_node_count(self, edge_data: list):
        node_list = {}
        for edge in edge_data:
            (u, v) = edge
            if u not in node_list:
                node_list[u] = 1
            if v not in node_list:
                node_list[v] = 1
        return len(node_list.keys())
    
    def edgelist_node_list(self, edge_data: list):
        node_list = {}
        for edge in edge_data:
            (u, v) = edge
            if u not in node_list:
                node_list[u] = 1
            if v not in node_list:
                node_list[v] = 1
        return list(node_list.keys())

    def nodes_list(self) -> list:
        r"""
        Return a list of nodes present in an edgelist
        """
        node_list = {}
        for _, edge_data in self.edgelist.items():
            for (u,v), _ in edge_data.items():
                if u not in node_list:
                    node_list[u] = 1
                if v not in node_list:
                    node_list[v] = 1
        
        self.node_list = list(node_list.keys())
        return list(node_list.keys())
    
    def check_time_gap(self) -> bool:
        r"""
        Check whether the edgelist timestamps have gaps or not (increments bigger than 1)
        Returns:
            time_gap: a boolean indicating whether there is a time gap or not
        """
        time_gap = False
        ts = list(self.data.keys())
        for i in range(1, len(ts)):
            if ts[i] - ts[i-1] > 1:
                time_gap = True
                return time_gap
        return time_gap
    
    def save2csv(self,
                 fname:str = "output") -> None:
        r"""
        Save the graph object in an edgelist format to a csv file
        Args:
            fname: name of the csv file to save the graph, no csv suffix needed
        """
        outname = fname + ".csv"
        #iterate through all edges
        with open(outname, 'w') as csvfile:
            print ("saving to ", outname)
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['timestamp'] + ['source'] + ['destination'])
            for t, edges_list in self.data.items():
                for edge in edges_list:
                    (u, v) = edge
                    csvwriter.writerow([t] + [u] + [v])        
                    
    # def _generate_graph(self, 
    #                     edgelist: Optional[dict] = None
    #                     ) -> list:
    #     r'''
    #     Generate a list of graph snapshots. Each snapshot is a 
    #     Networkx graph object.
    #     Parameters:
    #         edgelist: a dictionary containing in the form of {t: {(u, v), freq}}
    #     Returns:
    #         G_times: a list of networkx graphs
    #     '''
    #     if self.edgelist is None:
    #         return []
    #     elif edgelist is None:
    #         edgelist = self.edgelist
    #     G_times = []
    #     G = nx.Graph()
    #     cur_t = 0
    #     for ts, edge_data in edgelist.items():
    #         for (u,v), n in edge_data.items():
    #             if (ts != cur_t):
    #                 G_times.append(G)   
    #                 G = nx.Graph()  
    #                 cur_t = ts 
    #             G.add_edge(u, v, freq=n) 
    #     G_times.append(G)
    #     return G_times
    
    