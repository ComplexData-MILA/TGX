import pandas as pd
import numpy as np
from tgb.linkproppred.dataset import LinkPropPredDataset
from tgb.nodeproppred.dataset import NodePropPredDataset

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
        'SocialEvo' : {'header': True, 'index': 0, 'discretize': True, 'intervals': 40},
        'Flights'   : {'header': True, 'index': 0, 'discretize': False,'intervals': 'daily'},
        'LastFM'    : {'header': True, 'index': 0, 'discretize': True, 'intervals': 'monthly'},
        'Contacts'  : {'header': True, 'index': 0, 'discretize': True, 'intervals': 'daily'}
        }

class data():
    def __init__(self):
        pass

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

    @classmethod
    def tgb(self, dname, root):
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
        return self


    def read_specifications(self, data):
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