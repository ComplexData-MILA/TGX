# from tgx.readwrite.read_files import *
import tgx


# network = [
#            'USLegis',
#            'CanParl',
#            'UNTrade',
#            'UNVote',
#            'Reddit',
#            'Wikipedia',
#            'Enron',
#            'MOOC',
#            'UCI',
#            'SocialEvo',
#            'Flights',
#            'LastFM',
#            'Contacts'
#            ]

# network = ["UCI"]
# for ntw in network:
#     data = read_edgelist(data = ntw)
#     # print(data)
#     plot_path = "./examples/plots/TEA/"
#     TEA(data, plot_path, network_name=ntw, intervals=38)
    # plot_path1 = "./examples/plots/TET/"
    # TET(data, plot_path1, network_name=ntw)

data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
                "python3.9/site-packages/tgb/datasets/tgbl_review/tgbl-review_edgelist_v2.csv", 
                header=True, 
                t_col=0)
plot_path2 = "./examples/plots/TEA/"
tgx.TEA(data, plot_path2, network_name="tgbl-review", intervals=30)
plot_path1 = "./examples/plots/TET/"
tgx.TET(data, plot_path1, network_name="tgbl-review")
