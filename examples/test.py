from tgn.readwrite.read_files import *
# from tgn.algorithms.TEA import TEA
from tgn.algorithms.visualization import TEA
from tgn.algorithms.TET import TET

# network = [
        #    'USLegis',
        #    'CanParl',
         #   'UNTrade',
         #   'UNVote',
        #    'Reddit',
        #    'Wikipedia',
        #    'Enron',
        #    'MOOC',
        #    'UCI',
        #    'SocialEvo',
        #    'Flights',
        #    'LastFM',
        #    'Contacts'
         #   ]

network = ["MOOC"]
for ntw in network:
    data = read_edgelist(data = ntw)
    plot_path = "./examples/plots/TET/"
    TEA(data, plot_path, network_name=ntw, font_size=20)
# main()

