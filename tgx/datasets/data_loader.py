import pandas as pd
import numpy as np


__all__ = ["data"]
DataPath={
    'USLegis'   : "/data/USLegis/ml_USLegis.csv",
    'CanParl'   : "/data/CanParl/ml_CanParl.csv",
    'UNTrade'   : "/data/UNtrade/ml_UNtrade.csv",
    'UNVote'    : "/data/UNvote/ml_UNvote.csv",
    'Reddit'    : "/data/reddit/ml_reddit.csv",
    'Wikipedia' : "/data/wikipedia/ml_wikipedia.csv",
    'Enron'     : "/data/enron/ml_enron.csv",
    'MOOC'      : "/data/mooc/ml_mooc.csv",
    'UCI'       : "/data/uci/ml_uci.csv",
    'SocialEvo' : "/data/SocialEvo/ml_SocialEvo.csv",
    'Flights'   : "/data/Flights/ml_Flights.csv",
    'LastFM'    : "/data/lastfm/ml_lastfm.csv",
    'Contacts'  : "/data/Contacts/ml_Contacts.csv"
    }

Data_specifications = {
        'USLegis'       : {'discretize' : False,    'intervals': None},
        'CanParl'       : {'discretize' : False,    'intervals': None},
        'UNVote'        : {'discretize' : False,    'intervals': None},
        'Reddit'        : {'discretize' : True,     'intervals': 'daily'},
        'Enron'         : {'discretize' : True,     'intervals': 'monthly'},
        'MOOC'          : {'discretize' : True,     'intervals': 'daily'},
        'UCI'           : {'discretize' : True,     'intervals': 'weekly'},
        'SocialEvo'     : {'discretize' : True,     'intervals': 'weekly'},
        'Flights'       : {'discretize' : False,    'intervals': None},
        'Contacts'      : {'discretize' : True,     'intervals': 'daily'},
        'LastFM'        : {'discretize' : True,     'intervals': 'monthly'},
        'tgbl-wiki'     : {'discretize' : True,     'intervals': 'daily'},
        'tgbl-review'   : {'discretize' : True,     'intervals': 'yearly'},
        'tgbl-coin'     : {'discretize' : True,     'intervals': 'weekly'},
        'tgbl-comment'  : {'discretize' : True,     'intervals': 'monthly'},
        'tgbl-flight'   : {'discretize' : True,     'intervals': 'monthly'},
        'tgbn-trade'    : {'discretize' : False,    'intervals': None},
        'tgbn-genre'    : {'discretize' : True,     'intervals': 'monthly'},
        'tgbn-reddit'   : {'discretize' : True,     'intervals': 'monthly'}
        }

class data(object):
    def __init__(self):
        """
        Data class for loading default (in-package) temporal datasets

        In order to use "tgb" datasets install tgb package
        for more detals visit here: https://tgb.complexdatalab.com/

        In order to use dgb datasets download and extract dataset file
        from here: https://zenodo.org/record/7213796#.Y1cO6y8r30o
        and locate them in ./data/ directory.
        """
        pass

    @classmethod
    def tgb(self, dname: str):
        """
        Load datasets from "tgb" package. To load these datasets you need to install tgb package.
        Parameters:
            dname: str, name of the dataset from the list:
                        ["tgbl-wiki", "tgbl-review", 
                        "tgbl-coin", "tgbl-comment", 
                        "tgbl-flight","tgbn-trade", 
                        "tgbn-genre", "tgbn-reddit"]
    
        """
        from tgb.linkproppred.dataset import LinkPropPredDataset
        from tgb.nodeproppred.dataset import NodePropPredDataset
        
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
        self.discretize = Data_specifications[dname]['discretize']
        self.intervals = Data_specifications[dname]['intervals']
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
        self.path = DataPath[data]
        # self.header = Data_specifications[data]['header']
        # self.index = Data_specifications[data]['index']
        self.discretize = Data_specifications[data]['discretize']
        self.intervals = Data_specifications[data]['intervals']
        return self
    
    def load_dgb_data(self):
        data = pd.read_csv(f"{self.root}{self.path}", index_col=0)
        self.data =  data.iloc[:, 0:3].to_numpy()
        return self
    

    @classmethod
    def mooc(self, root):
        data = "MOOC"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def uci(self, root):
        data = "UCI"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self

    @classmethod   
    def uslegis(self, root):
        data = "USLegis"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def canparl(self, root):
        data = "CanParl"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def untrade(self, root):
        data = "UNTrade"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def unvote(self, root):
        data = "UNVote"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def reddit(self, root):
        data = "Reddit"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def wikipedia(self, root):
        data = "Wikipedia"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def enron(self, root):
        data = "Enron"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def social_evo(self, root):
        data = "SocialEvo"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def flights(self, root):
        data = "Flights"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def lastfm(self, root):
        data = "LastFM"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def contacts(self, root):
        data = "Contacts"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self

if __name__ == "__main__":
    import tgx
    # mooc_data=tgx.data.mooc()
    # _=tgx.data.canparl()
    # tt=tgx.data.contacts()
    # _=tgx.data.enron()
    # _=tgx.data.flights()
    # _=tgx.data.lastfm()
    # _=tgx.data.reddit()
    # _=tgx.data.social_evo()
    # _=tgx.data.uci()
    # _=tgx.data.untrade()
    # _=tgx.data.unvote()
    # tgx.data.uslegis(root='/network/scratch/r/razieh.shirzadkhani')
    tgx.data.enron(root='/network/scratch/r/razieh.shirzadkhani')