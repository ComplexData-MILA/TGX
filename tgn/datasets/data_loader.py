
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
    'USLegis'   : {'header': True, 'index': False, 'continuous': False, 'intervals': None},
    'CanParl'   : {'header': True, 'index': False, 'continuous': False, 'intervals': None},
    'UNTrade'   : {'header': True, 'index': False, 'continuous': False, 'intervals': None},
    'UNVote'    : {'header': True, 'index': False, 'continuous': False, 'intervals': None},
    'Reddit'    : {'header': True, 'index': False, 'continuous': True, 'intervals': 'daily'},
    'Wikipedia' : {'header': True, 'index': False, 'continuous': True, 'intervals': 'daily'},
    'Enron'     : {'header': True, 'index': True, 'continuous': True, 'intervals': 'monthly'},
    'MOOC'      : {'header': True, 'index': False, 'continuous': True, 'intervals': 28},
    'UCI'       : {'header': True, 'index': True, 'continuous': True, 'intervals': 39},
    'SocialEvo' : {'header': True, 'index': True, 'continuous': True, 'intervals': 40},
    'Flights'   : {'header': True, 'index': False, 'continuous': False, 'intervals': None},
    'LastFM'    : {'header': True, 'index': False, 'continuous': True, 'intervals': 'monthly'},
    'Contacts'  : {'header': True, 'index': False, 'continuous': True, 'intervals': 'daily'}
}

def read_dataset(data):
    if data not in DataPath:
        raise KeyError('Data name invalid')
    
    print(f"Loading {data} network ...")
    path = DataPath[data]
    header = Data_specifications[data]['header']
    index = Data_specifications[data]['index']
    continuous = Data_specifications[data]['continuous']
    intervals = Data_specifications[data]['intervals']

    return (path, 
            header, 
            index, 
            continuous, 
            intervals)


if __name__ == "__main__":
    print(read_dataset("MOOC"))
