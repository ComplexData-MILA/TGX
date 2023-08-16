import networkx as nx

class Graph():
    def __init__(self, 
                 edgelist = None, 
                 discrete_edgelist = None,
                 continuous_edgelist = None,
                 discretized = True):
        
        self.edgelist = edgelist
        self.discrite_edgelist = discrete_edgelist
        self.continuous_edgelist = continuous_edgelist
        if discretized:
            self.discrite_graph = self._generate_graph()
        
        
    def _generate_graph(self):
        '''
        This function returns a list of snaoshots
        '''
        if self.edgelist is None:
            return []
        G_times = []
        G = nx.Graph()
        cur_t = 0
        yy = 0
        for ts, edge_data in self.edgelist.items():
            for (u,v), n in edge_data.items():
                if (ts != cur_t):
                    G_times.append(G)   
                    G = nx.Graph()  
                    cur_t = ts 
                G.add_edge(u, v) 
        G_times.append(G)
        return G_times