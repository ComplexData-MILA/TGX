import pandas as pd
import numpy as np
import requests
from clint.textui import progress
import os, io
import shutil
import sys
import zipfile
import urllib

__all__ = ["data"]
DataPath={
    'USLegis'   : "/data/USLegis/ml_USLegis.csv",
    'CanParl'   : "/data/CanParl/ml_CanParl.csv",
    'UNtrade'   : "/data/UNtrade/ml_UNtrade.csv",
    'UNvote'    : "/data/UNvote/ml_UNvote.csv",
    'reddit'    : "/data/reddit/ml_reddit.csv",
    'Wikipedia' : "/data/wikipedia/ml_wikipedia.csv",
    'enron'     : "/data/enron/ml_enron.csv",
    'mooc'      : "/data/mooc/ml_mooc.csv",
    'uci'       : "/data/uci/ml_uci.csv",
    'SocialEvo' : "/data/SocialEvo/ml_SocialEvo.csv",
    'Flights'   : "/data/Flights/ml_Flights.csv",
    'lastfm'    : "/data/lastfm/ml_lastfm.csv",
    'Contacts'  : "/data/Contacts/ml_Contacts.csv"
    }

Data_specifications = {
        'USLegis'       : {'discretize' : False,    'intervals': None},
        'CanParl'       : {'discretize' : False,    'intervals': None},
        'UNvote'        : {'discretize' : False,    'intervals': None},
        'reddit'        : {'discretize' : True,     'intervals': 'daily'},
        'enron'         : {'discretize' : True,     'intervals': 'monthly'},
        'mooc'          : {'discretize' : True,     'intervals': 'daily'},
        'uci'           : {'discretize' : True,     'intervals': 'weekly'},
        'SocialEvo'     : {'discretize' : True,     'intervals': 'weekly'},
        'Flights'       : {'discretize' : False,     'intervals': 121},
        'Contacts'      : {'discretize' : True,     'intervals': 'daily'},
        'lastfm'        : {'discretize' : True,     'intervals': 'monthly'}
        }

class builtin(object):
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
        try:
            data = pd.read_csv(f"{self.root}{self.path}", index_col=0)
        except:
            self.download_file(self)
            data = pd.read_csv(f"{self.root}{self.path}", index_col=0)

        self.data =  data.iloc[:, 0:3].to_numpy()
        return self
    
    def download_file(self):

        print("Data missing, download recommended!")
        inp = input('Will you download the dataset(s) now? (y/N)\n').lower()
        url = f"https://zenodo.org/record/7213796/files/{self.name}.zip"
        path_download = f"./data"
        print(path_download)
        print(url)
        if inp == 'y':
            print(f"Download started, this might take a while . . .")
            zip_path, _ = urllib.request.urlretrieve(url)
            with zipfile.ZipFile(zip_path, "r") as f:
                f.extractall(path_download)
            print("Download completed")

        else:
            print("Download cancelled")


    @classmethod
    def mooc(self, root):
        data = "mooc"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def uci(self, root):
        data = "uci"
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
        data = "UNtrade"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def unvote(self, root):
        data = "UNvote"
        self.root = root
        self.read_specifications(self, data)
        self.load_dgb_data(self)
        return self
    
    @classmethod
    def reddit(self, root):
        data = "reddit"
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
        data = "enron"
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
        data = "lastfm"
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