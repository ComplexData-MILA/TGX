from tgn.readwrite.read_files import *
from tgn.algorithms.TEA import TEA

network = [
        #    'USLegis',
        #    'CanParl',
        #    'UNTrade',
        #    'UNVote',
        #    'Reddit',
        #    'Wikipedia',
        #    'Enron',
        #    'MOOC',
           'UCI',
           'SocialEvo',
           'Flights',
           'LastFM',
           'Contacts'
           ]

# network = ["MOOC"]
for ntw in network:
    data = read_edgelist(data = ntw)
    plot_path = "./examples/plots/"
    TEA(data, plot_path, network_name=ntw)


