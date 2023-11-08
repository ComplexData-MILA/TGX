# import networkx as nx
from typing import Optional
from tgx.utils.graph_utils import edgelist_discritizer, frequency_count
from tgx.io.read import read_csv

class Graph(object):
    def __init__(self, 
                 dataset: Optional[object] = None, 
                 fname: Optional[str] = None,
                 edgelist: Optional[dict] = None,
                 discretized: Optional[bool] = False):
        """
        Create a Graph object with specific characteristics
        Args:
            edgelist: a dictionary of temporal edges in the form of {t: {(u, v), freq}}
            discretized: whether the given edgelist was discretized or not
        """

        if dataset is not None and isinstance(dataset, type):
            self.data = read_csv(dataset)
        elif fname is not None and isinstance(fname, str):
            self.data = read_csv(fname)
        elif edgelist is not None and isinstance(edgelist, dict):
            self.data = edgelist
        else:
            raise TypeError("Please enter valid input.")
        
        self.subsampled_graph = None
        self.freq_data = None
        
        
    def discretize(self, intervals):
        # self.discretized = True
        disc_G = edgelist_discritizer(self.data,
                                                  time_interval = intervals)
        self.continueos_G = self.data
        self.data = disc_G
        return self.data    

    def count_freq(self):
        self.freq_data = frequency_count(self.data)
        return self

    def number_of_edges(self) -> int:
        r"""
        Calculate total number of nodes present in an edgelist
        """
        edgelist = self.data
        a = 0
        for _, edges in edgelist.items():
            a += len(edges)
        
        return #len(edges_list.keys())

    def number_of_nodes(self) -> int:
        r"""
        Calculate total number of nodes present in an edgelist
        """
        
        edgelist = self.data
        node_list = {}
        for _, edge_data in edgelist.items():
            for (u,v), _ in edge_data.items():
                if u not in node_list:
                    node_list[u] = 1
                if v not in node_list:
                    node_list[v] = 1
        return len(node_list.keys())

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
    
    