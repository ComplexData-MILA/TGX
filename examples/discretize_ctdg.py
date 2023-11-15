import tgx

"""
1. load a dataset
2. load into a graph
3. discretize the graph
4. save the graph back to a csv
"""

dataset = tgx.builtin.uci()
# dataset = tgx.tgb_data("tgbl-wiki")
ctdg = tgx.Graph(dataset)
ctdg.save2csv("ctdg")
dtdg = ctdg.discretize(time_scale="daily")
dtdg.save2csv("dtdg")
dtdg = ctdg.discretize(time_scale=200)
dtdg.save2csv("dtdg_200")


