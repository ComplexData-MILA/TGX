import networkx as nx
from typing import Optional


class Graph(object):
    def __init__(self, 
                 edgelist: Optional[dict] = None, 
                 discretized: Optional[bool] = False):
        """
        Create a Graph object with specific characteristics
        Args:
            edgelist: a dictionary of temporal edges in the form of {t: {(u, v), freq}}
            discretized: whether the given edgelist was discretized or not
        """
        
        self.edgelist = edgelist
        self.subsampled_graph = None
        self.graph = self._generate_graph()
        self.discretized = discretized
        
        # if discretized:
        #     self.discrite_graph = self._generate_graph()
        #     self.discrite_edgelist = edgelist
        # else:
        #     self.continuous_edgelist = edgelist
        
        
    def number_of_nodes(self, edgelist: Optional[dict] = None) -> int:
        r"""
        Calculate total number of nodes present in an edgelist
        Parameters:
            edgelist: dictionary in the form of {t: {(u, v), freq}}
        """
        if self.edgelist is None:
            return []
        elif edgelist is None:
            edgelist = self.edgelist
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

    def _generate_graph(self, 
                        edgelist: Optional[dict] = None
                        ) -> list:
        r'''
        Generate a list of graph snapshots. Each snapshot is a 
        Networkx graph object.
        Parameters:
            edgelist: a dictionary containing in the form of {t: {(u, v), freq}}
        Returns:
            G_times: a list of networkx graphs
        '''
        if self.edgelist is None:
            return []
        elif edgelist is None:
            edgelist = self.edgelist
        G_times = []
        G = nx.Graph()
        cur_t = 0
        for ts, edge_data in edgelist.items():
            for (u,v), n in edge_data.items():
                if (ts != cur_t):
                    G_times.append(G)   
                    G = nx.Graph()  
                    cur_t = ts 
                G.add_edge(u, v, freq=n) 
        G_times.append(G)
        return G_times
    
    