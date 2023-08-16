
common_path = '/network/scratch/r/razieh.shirzadkhani/data'
DataPath={
    'USLegis'   : f"{common_path}/USLegis/USLegis.csv",
    'CanParl'   : f"{common_path}/CanParl/CanParl.csv",
    'UNTrade'   : f"{common_path}/UNtrade/UNtrade.csv",
    'UNVote'    : f"{common_path}/UNvote/UNvote.csv",
    'Reddit'    : f"{common_path}/reddit/reddit.csv",
    'Wikipedia' : f"{common_path}/wikipedia/wikipedia.csv",
    'Enron'     : f"{common_path}/enron/ml_enron.csv",
    'MOOC'      : f"{common_path}/mooc/mooc.csv",
    'UCI'       : f"{common_path}/uci/ml_uci.csv",
    'SocialEvo' : f"{common_path}/SocialEvo/ml_SocialEvo.csv",
    'Flights'   : f"{common_path}/Flights/Flights.csv",
    'LastFM'    : f"{common_path}/lastfm/lastfm.csv",
    'Contacts'  : f"{common_path}/Contacts/Contacts.csv"}

Data_specifications = {
        'USLegis'   : {'header': True, 'index': False, 'discretize': False, 'intervals': None},
        'CanParl'   : {'header': True, 'index': False, 'discretize': False, 'intervals': None},
        'UNTrade'   : {'header': True, 'index': False, 'discretize': False, 'intervals': None},
        'UNVote'    : {'header': True, 'index': False, 'discretize': False, 'intervals': None},
        'Reddit'    : {'header': True, 'index': False, 'discretize': True, 'intervals': 'daily'},
        'Wikipedia' : {'header': True, 'index': False, 'discretize': True, 'intervals': 'daily'},
        'Enron'     : {'header': True, 'index': True, 'discretize': True, 'intervals': 'monthly'},
        'MOOC'      : {'header': True, 'index': False, 'discretize': True, 'intervals': 'daily'},
        'UCI'       : {'header': True, 'index': True, 'discretize': True, 'intervals': 38},
        'SocialEvo' : {'header': True, 'index': True, 'discretize': True, 'intervals': 40},
        'Flights'   : {'header': True, 'index': False, 'discretize': False, 'intervals': 'daily'},
        'LastFM'    : {'header': True, 'index': False, 'discretize': True, 'intervals': 'monthly'},
        'Contacts'  : {'header': True, 'index': False, 'discretize': True, 'intervals': 'daily'}
        }

class data():
    def __init__(self):
        pass
        
    @classmethod    
    def mooc(self):
        data = "MOOC"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def uci(self):
        data = "UCI"
        self.read_specifications(self, data)
        return self
       
    @classmethod
    def uslegis(self):
        data = "USLegis"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def canparl(self):
        data = "CanParl"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def untrade(self):
        data = "UNTrade"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def unvote(self):
        data = "UNVote"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def reddit(self):
        data = "Reddit"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def wikipedia(self):
        data = "Wikipedia"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def enron(self):
        data = "Enron"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def social_evo(self):
        data = "SocialEvo"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def flights(self):
        data = "Flights"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def lastfm(self):
        data = "LastFM"
        self.read_specifications(self, data)
        return self
    
    @classmethod
    def contacts(self):
        data = "Contacts"
        self.read_specifications(self, data)
        return self

    def read_specifications(self, data):
        self.name = data
        self.path = DataPath[data]
        self.header = Data_specifications[data]['header']
        self.index = Data_specifications[data]['index']
        self.discretize = Data_specifications[data]['discretize']
        self.intervals = Data_specifications[data]['intervals']
        return self


if __name__ == "__main__":
    import tgx
    # mooc_data=tgx.data.mooc()
    # _=tgx.data.canparl()
    tt=tgx.data.contacts()
    print(tt.path)
    # _=tgx.data.enron()
    # _=tgx.data.flights()
    # _=tgx.data.lastfm()
    # _=tgx.data.reddit()
    # _=tgx.data.social_evo()
    # _=tgx.data.uci()
    # _=tgx.data.untrade()
    # _=tgx.data.unvote()
    # _=tgx.data.uslegis()