import pandas as pd
import numpy as np
from tgb.linkproppred.dataset import LinkPropPredDataset
from tgb.nodeproppred.dataset import NodePropPredDataset

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
        'USLegis'   : {'header': True, 'index': 0, 'discretize': False,'intervals': None},
        'CanParl'   : {'header': True, 'index': 0, 'discretize': False,'intervals': None},
        'UNTrade'   : {'header': True, 'index': 0, 'discretize': False,'intervals': None},
        'UNVote'    : {'header': True, 'index': 0, 'discretize': False,'intervals': None},
        'Reddit'    : {'header': True, 'index': 0, 'discretize': True, 'intervals': 'daily'},
        'Wikipedia' : {'header': True, 'index': 0, 'discretize': True, 'intervals': 'daily'},
        'Enron'     : {'header': True, 'index': 0, 'discretize': True, 'intervals': 'monthly'},
        'MOOC'      : {'header': True, 'index': 0, 'discretize': True, 'intervals': 'daily'},
        'UCI'       : {'header': True, 'index': 0, 'discretize': True, 'intervals': 39},
        'SocialEvo' : {'header': True, 'index': 0, 'discretize': True, 'intervals': 49},
        'Flights'   : {'header': True, 'index': 0, 'discretize': False,'intervals': 'daily'},
        'LastFM'    : {'header': True, 'index': 0, 'discretize': True, 'intervals': 50},
        'Contacts'  : {'header': True, 'index': 0, 'discretize': True, 'intervals': 'daily'}
        }

class data():
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
    def tgb(self, dname):
        """
        Load datasets from "tgb" package. To load these datasets you need to install tgb package.
        Parameters:
            dname: str, name of the dataset from the list:
                        ["tgbl-wiki", "tgbl-review", 
                        "tgbl-coin", "tgbl-comment", 
                        "tgbl-flight","tgbn-trade", 
                        "tgbn-genre", "tgbn-reddit"]
        
        Returns:
            self.name: str, name of the dataset
            self.data: array, a numpy array with shape (Edges, Time)
        """
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
        self.name = dname
        return self


    def read_specifications(self, data):
        """
        Load dataset specifications for dgb datasets
        Parameters:
            data: str, name of the dataset
        Returns:
            self.name: str, name of the dataset
            self.path: dataset path in your local machine 
            self.
        """
        self.name = data
        self.path = DataPath[data]
        self.header = Data_specifications[data]['header']
        self.index = Data_specifications[data]['index']
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