import tgx


mooc = tgx.data.uci()
data = tgx.read_edgelist(data = mooc)
plot_path = "./examples/plots/"
# tgx.TEA(data, plot_path, network_name=mooc.name)
# plot_path1 = "./examples/plots/TET/"
# TET(data, plot_path1, network_name=ntw)


plot_path = "./examples/plots/"
G = tgx.Graph(data)
tgx.edges_per_timestamp(G.discrite_graph, plot_path, network_name=mooc.name)
tgx.average_degree(G.discrite_graph, plot_path, network_name=mooc.name)
tgx.nodes_per_timestamp(G.discrite_graph, plot_path, network_name=mooc.name)



# data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
#                 "python3.9/site-packages/tgb/datasets/tgbl_wiki/tgbl-wiki_edgelist_v2.csv", 
#                 header=True)
# plot_path2 = "./examples/plots/TEA/"
# tgx.TEA(data, plot_path2, network_name="tgbl_wiki", intervals=30)
# plot_path1 = "./examples/plots/TET/"
# tgx.TET(data, plot_path1, network_name="tgbl_wiki", intervals=30)

# data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
#                 "python3.9/site-packages/tgb/datasets/tgbl_coin/tgbl-coin_edgelist.csv", 
#                 header=True,
#                 t_col=0)
# plot_path2 = "./examples/plots/TEA/"
# tgx.TEA(data, plot_path2, network_name="tgbl_coin", intervals=30)
# plot_path1 = "./examples/plots/TET/"
# tgx.TET(data, plot_path1, network_name="tgbl_coin", intervals=30)

# data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
#                 "python3.9/site-packages/tgb/datasets/tgbl_comment/tgbl-comment_edgelist.csv", 
#                 header=True)
# plot_path2 = "./examples/plots/TEA/"
# tgx.TEA(data, plot_path2, network_name="tgbl_comment", intervals=30)
# plot_path1 = "./examples/plots/TET/"
# tgx.TET(data, plot_path1, network_name="tgbl_comment", intervals=30)

# data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
#                 "python3.9/site-packages/tgb/datasets/tgbl_flight/tgbl-flight_edgelist.csv", 
#                 header=True)
# plot_path2 = "./examples/plots/TEA/"
# tgx.TEA(data, plot_path2, network_name="tgbl_flight", intervals=30)
# plot_path1 = "./examples/plots/TET/"
# tgx.TET(data, plot_path1, network_name="tgbl_flight", intervals=30)

# data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
#                 "python3.9/site-packages/tgb/datasets/tgbn_genre/tgbn-genre_edgelist.csv", 
#                 header=True)
# plot_path2 = "./examples/plots/TEA/"
# tgx.TEA(data, plot_path2, network_name="tgbn_genre", intervals=30)
# plot_path1 = "./examples/plots/TET/"
# tgx.TET(data, plot_path1, network_name="tgbn_genre", intervals=30)

# data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
#                 "python3.9/site-packages/tgb/datasets/tgbn_trade/tgbn-trade_edgelist.csv", 
#                 header=True,
#                 t_col=0)
# plot_path2 = "./examples/plots/TEA/"
# tgx.TEA(data, plot_path2, network_name="tgbn_trade", intervals=30)
# plot_path1 = "./examples/plots/TET/"
# tgx.TET(data, plot_path1, network_name="tgbn_trade", intervals=30)

# data = tgx.read_edgelist(fname="/home/mila/r/razieh.shirzadkhani/.conda/envs/tg/lib/"
#                 "python3.9/site-packages/tgb/datasets/tgbn-arxiv/tgbn-trade_edgelist.csv", 
#                 header=True)
# plot_path2 = "./examples/plots/TEA/"
# tgx.TEA(data, plot_path2, network_name="tgbn_arxiv", intervals=30)
# plot_path1 = "./examples/plots/TET/"
# tgx.TET(data, plot_path1, network_name="tgbn_arxiv", intervals=30)

