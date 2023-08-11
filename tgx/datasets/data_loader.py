
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
    'USLegis'   : {'header': True, 'index': False, 'cont_to_disc': False, 'intervals': None},
    'CanParl'   : {'header': True, 'index': False, 'cont_to_disc': False, 'intervals': None},
    'UNTrade'   : {'header': True, 'index': False, 'cont_to_disc': False, 'intervals': None},
    'UNVote'    : {'header': True, 'index': False, 'cont_to_disc': False, 'intervals': None},
    'Reddit'    : {'header': True, 'index': False, 'cont_to_disc': True, 'intervals': 'daily'},
    'Wikipedia' : {'header': True, 'index': False, 'cont_to_disc': True, 'intervals': 'daily'},
    'Enron'     : {'header': True, 'index': True, 'cont_to_disc': True, 'intervals': 'monthly'},
    'MOOC'      : {'header': True, 'index': False, 'cont_to_disc': True, 'intervals': 'daily'},
    'UCI'       : {'header': True, 'index': True, 'cont_to_disc': True, 'intervals': False},
    'SocialEvo' : {'header': True, 'index': True, 'cont_to_disc': True, 'intervals': 40},
    'Flights'   : {'header': True, 'index': False, 'cont_to_disc': False, 'intervals': None},
    'LastFM'    : {'header': True, 'index': False, 'cont_to_disc': True, 'intervals': 'monthly'},
    'Contacts'  : {'header': True, 'index': False, 'cont_to_disc': True, 'intervals': 'daily'}
}

def read_dataset(data):
    if data not in DataPath:
        raise KeyError('Data name invalid')
    
    print(f"Loading {data} network ...")
    path = DataPath[data]
    header = Data_specifications[data]['header']
    index = Data_specifications[data]['index']
    cont_to_disc = Data_specifications[data]['cont_to_disc']
    intervals = Data_specifications[data]['intervals']

    return (path, 
            header, 
            index, 
            cont_to_disc, 
            intervals)

class data():
    def __init__(self):
        self.Datapath = DataPath
        self.Data_specifications = Data_specifications
        
    def mooc(self):
        return(DataPath["MOOC"],
            [Data_specifications["MOOC"]["header"],
            Data_specifications["MOOC"]["index"],
            Data_specifications["MOOC"]["cont_to_disc"],
            Data_specifications["MOOC"]["intervals"]])

    def uci(self):
        return(DataPath["UCI"],
            [Data_specifications["UCI"]["header"],
            Data_specifications["UCI"]["index"],
            Data_specifications["UCI"]["cont_to_disc"],
            Data_specifications["UCI"]["intervals"]])
    
    def uslegis(self):
        return(DataPath["USLegis"],
            [Data_specifications["USLegis"]["header"],
            Data_specifications["USLegis"]["index"],
            Data_specifications["USLegis"]["cont_to_disc"],
            Data_specifications["USLegis"]["intervals"]])
    
    def canparl(self):
        return(DataPath["CanParl"],
            [Data_specifications["CanParl"]["header"],
            Data_specifications["CanParl"]["index"],
            Data_specifications["CanParl"]["cont_to_disc"],
            Data_specifications["CanParl"]["intervals"]])
    
    def untrade(self):
        return(DataPath["UNTrade"],
            [Data_specifications["UNTrade"]["header"],
            Data_specifications["UNTrade"]["index"],
            Data_specifications["UNTrade"]["cont_to_disc"],
            Data_specifications["UNTrade"]["intervals"]])
    
    def unvote(self):
        return(DataPath["UNVote"],
            [Data_specifications["UNVote"]["header"],
            Data_specifications["UNVote"]["index"],
            Data_specifications["UNVote"]["cont_to_disc"],
            Data_specifications["UNVote"]["intervals"]])
    
    def reddit(self):
        return(DataPath["Reddit"],
            [Data_specifications["Reddit"]["header"],
            Data_specifications["Reddit"]["index"],
            Data_specifications["Reddit"]["cont_to_disc"],
            Data_specifications["Reddit"]["intervals"]])
    
    def wikipedia(self):
        return(DataPath["Wikipedia"],
            [Data_specifications["Wikipedia"]["header"],
            Data_specifications["Wikipedia"]["index"],
            Data_specifications["Wikipedia"]["cont_to_disc"],
            Data_specifications["Wikipedia"]["intervals"]])
    
    def enron(self):
        return(DataPath["Enron"],
            [Data_specifications["Enron"]["header"],
            Data_specifications["Enron"]["index"],
            Data_specifications["Enron"]["cont_to_disc"],
            Data_specifications["Enron"]["intervals"]])
    
    def social_evo(self):
        return(DataPath["SocialEvo"],
            [Data_specifications["SocialEvo"]["header"],
            Data_specifications["SocialEvo"]["index"],
            Data_specifications["SocialEvo"]["cont_to_disc"],
            Data_specifications["SocialEvo"]["intervals"]])
    
    def flights(self):
        return(DataPath["Flights"],
            [Data_specifications["Flights"]["header"],
            Data_specifications["Flights"]["index"],
            Data_specifications["Flights"]["cont_to_disc"],
            Data_specifications["Flights"]["intervals"]])
    
    def lastfm(self):
        return(DataPath["LastFM"],
            [Data_specifications["LastFM"]["header"],
            Data_specifications["LastFM"]["index"],
            Data_specifications["LastFM"]["cont_to_disc"],
            Data_specifications["LastFM"]["intervals"]])
    
    def contacts(self):
        return(DataPath["Contacts"],
            [Data_specifications["Contacts"]["header"],
            Data_specifications["Contacts"]["index"],
            Data_specifications["Contacts"]["cont_to_disc"],
            Data_specifications["Contacts"]["intervals"]])

def mooc():
    return(DataPath["MOOC"],
        [Data_specifications["MOOC"]["header"],
        Data_specifications["MOOC"]["index"],
        Data_specifications["MOOC"]["cont_to_disc"],
        Data_specifications["MOOC"]["intervals"]])

def uci():
    return(DataPath["UCI"],
        [Data_specifications["UCI"]["header"],
        Data_specifications["UCI"]["index"],
        Data_specifications["UCI"]["cont_to_disc"],
        Data_specifications["UCI"]["intervals"]])

def uslegis():
    return(DataPath["USLegis"],
        [Data_specifications["USLegis"]["header"],
        Data_specifications["USLegis"]["index"],
        Data_specifications["USLegis"]["cont_to_disc"],
        Data_specifications["USLegis"]["intervals"]])

def canparl(self):
    return(DataPath["CanParl"],
        [Data_specifications["CanParl"]["header"],
        Data_specifications["CanParl"]["index"],
        Data_specifications["CanParl"]["cont_to_disc"],
        Data_specifications["CanParl"]["intervals"]])

def untrade(self):
    return(DataPath["UNTrade"],
        [Data_specifications["UNTrade"]["header"],
        Data_specifications["UNTrade"]["index"],
        Data_specifications["UNTrade"]["cont_to_disc"],
        Data_specifications["UNTrade"]["intervals"]])

def unvote(self):
    return(DataPath["UNVote"],
        [Data_specifications["UNVote"]["header"],
        Data_specifications["UNVote"]["index"],
        Data_specifications["UNVote"]["cont_to_disc"],
        Data_specifications["UNVote"]["intervals"]])

def reddit(self):
    return(DataPath["Reddit"],
        [Data_specifications["Reddit"]["header"],
        Data_specifications["Reddit"]["index"],
        Data_specifications["Reddit"]["cont_to_disc"],
        Data_specifications["Reddit"]["intervals"]])

def wikipedia(self):
    return(DataPath["Wikipedia"],
        [Data_specifications["Wikipedia"]["header"],
        Data_specifications["Wikipedia"]["index"],
        Data_specifications["Wikipedia"]["cont_to_disc"],
        Data_specifications["Wikipedia"]["intervals"]])

def enron(self):
    return(DataPath["Enron"],
        [Data_specifications["Enron"]["header"],
        Data_specifications["Enron"]["index"],
        Data_specifications["Enron"]["cont_to_disc"],
        Data_specifications["Enron"]["intervals"]])

def social_evo(self):
    return(DataPath["SocialEvo"],
        [Data_specifications["SocialEvo"]["header"],
        Data_specifications["SocialEvo"]["index"],
        Data_specifications["SocialEvo"]["cont_to_disc"],
        Data_specifications["SocialEvo"]["intervals"]])

def flights(self):
    return(DataPath["Flights"],
        [Data_specifications["Flights"]["header"],
        Data_specifications["Flights"]["index"],
        Data_specifications["Flights"]["cont_to_disc"],
        Data_specifications["Flights"]["intervals"]])

def lastfm(self):
    return(DataPath["LastFM"],
        [Data_specifications["LastFM"]["header"],
        Data_specifications["LastFM"]["index"],
        Data_specifications["LastFM"]["cont_to_disc"],
        Data_specifications["LastFM"]["intervals"]])

def contacts(self):
    return(DataPath["Contacts"],
        [Data_specifications["Contacts"]["header"],
        Data_specifications["Contacts"]["index"],
        Data_specifications["Contacts"]["cont_to_disc"],
        Data_specifications["Contacts"]["intervals"]])
if __name__ == "__main__":
    # print(read_dataset("MOOC"))
    import tgx
    _,_=tgx.mooc()
    _,_=tgx.data.canparl()
    _,_=tgx.data.contacts()
    _,_=tgx.data.enron()
    _,_=tgx.data.flights()
    _,_=tgx.data.lastfm()
    _,_=tgx.data.reddit()
    _,_=tgx.data.social_evo()
    _,_=tgx.data.uci()
    _,_=tgx.data.untrade()
    _,_=tgx.data.unvote()
    _,_=tgx.data.uslegis()

