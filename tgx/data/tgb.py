import numpy as np

Data_specifications = {
        'tgbl-wiki'     : {'discretize' : True,     'time_scale': 'daily'},
        'tgbl-review'   : {'discretize' : True,     'time_scale': 'yearly'},
        'tgbl-coin'     : {'discretize' : True,     'time_scale': 'weekly'},
        'tgbl-comment'  : {'discretize' : True,     'time_scale': 'monthly'},
        'tgbl-flight'   : {'discretize' : True,     'time_scale': 'monthly'},
        'tgbn-trade'    : {'discretize' : False,    'time_scale': None},
        'tgbn-genre'    : {'discretize' : True,     'time_scale': 'monthly'},
        'tgbn-reddit'   : {'discretize' : True,     'time_scale': 'monthly'}
        }

class tgb_data(object):
    def __init__(self, dname: str, 
            edge_feat: bool = False,
            w: bool = False,
            edge_label: bool = False,
            edge_idxs: bool = False):
        """
        Data class for loading default (in-package) temporal datasets

        In order to use "tgb" datasets install tgb package
        for more detals visit here: https://tgb.complexdatalab.com/

        In order to use dgb datasets download and extract dataset file
        from here: https://zenodo.org/record/7213796#.Y1cO6y8r30o
        and locate them in ./data/ directory.
        """
        self.tgb(dname, 
                edge_feat = edge_feat,
                w = w,
                edge_label = edge_label,
                edge_idxs = edge_idxs)
        
        return

    @classmethod
    def tgb(self, dname: str, 
            edge_feat: bool = False,
            w: bool = False,
            edge_label: bool = False,
            edge_idxs: bool = False):
        """
        Load datasets from "tgb" package. To load these datasets you need to install tgb package.
        Parameters:
            dname: str, name of the dataset from the list:
                        ["tgbl-wiki", "tgbl-review", 
                        "tgbl-coin", "tgbl-comment", 
                        "tgbl-flight","tgbn-trade", 
                        "tgbn-genre", "tgbn-reddit"]
            edge_feat: list of edge features
            w: edge weights
            edge_label: edge labels
            edge_idxs: edge indexes

        """
        try:
            from tgb.linkproppred.dataset import LinkPropPredDataset
            from tgb.nodeproppred.dataset import NodePropPredDataset
        except:
            print("First install TGB package using 'pip install py-tgb'")
        
        link_pred = ["tgbl-wiki", "tgbl-review", "tgbl-coin", "tgbl-comment", "tgbl-flight"]
        node_pred = ["tgbn-trade", "tgbn-genre", "tgbn-reddit"]
        if dname in link_pred:
            data = LinkPropPredDataset(name=dname, root="datasets", preprocess=True)
        elif dname in node_pred:
            data = NodePropPredDataset(name=dname, root="datasets", preprocess=True)
        else:
            raise ValueError("Invalid tgb dataset name")
        
        data = data.full_data
        data = np.array([data['sources'], data["destinations"], data["timestamps"]])
        self.data = np.transpose(data)

        if edge_feat:
            self.edge_feat = data['edge_feat']
        if w:
            self.w = data['w']
        if edge_label:
            self.edge_label = data['edge_label']
        if edge_idxs:
            self.edge_idxs = data['edge_idxs']
        
        self.discretize = Data_specifications[dname]['discretize']
        self.time_scale = Data_specifications[dname]['time_scale']
        self.name = dname

        return self


    def read_specifications(self, 
                            data: type):
        """
        Load dataset specifications for dgb datasets
        Parameters:
            data: str, name of the dataset
        """
        self.name = data
        self.discretize = Data_specifications[data]['discretize']
        self.time_scale = Data_specifications[data]['time_scale']
        return self