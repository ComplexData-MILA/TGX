import networkx as nx

class Graph():
    def __init__(self, 
                 edgelist = None, 
                 discretized = True):
        """
        hello I am the only documentation here...
        actually not
        """
        
        self.edgelist = edgelist
        self.subsampled_graph = None
        if discretized:
            self.discrite_graph = self._generate_graph()
            self.discrite_edgelist = edgelist
        else:
            self.continuous_edgelist = edgelist
        
        
    def number_of_nodes(self):
        node_list = {}
        for _, edge_data in self.edgelist.items():
            for (u,v), _ in edge_data.items():
                if u not in node_list:
                    node_list[u] = 1
                if v not in node_list:
                    node_list[v] = 1
        return len(node_list.keys())

    def nodes(self):
        node_list = {}
        for _, edge_data in self.edgelist.items():
            for (u,v), _ in edge_data.items():
                if u not in node_list:
                    node_list[u] = 1
                if v not in node_list:
                    node_list[v] = 1
        
        self.node_list = list(node_list.keys())
        return list(node_list.keys())

    def _generate_graph(self, edgelist=None):
        '''
        This function returns a list of snaoshots
        '''
        if self.edgelist is None:
            return []
        elif edgelist is None:
            edgelist = self.edgelist
        G_times = []
        G = nx.Graph()
        cur_t = 0
        yy = 0
        for ts, edge_data in edgelist.items():
            for (u,v), n in edge_data.items():
                if (ts != cur_t):
                    G_times.append(G)   
                    G = nx.Graph()  
                    cur_t = ts 
                G.add_edge(u, v) 
        G_times.append(G)
        return G_times
    
    