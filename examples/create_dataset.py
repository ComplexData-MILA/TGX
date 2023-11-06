import pandas as pd

data = pd.read_csv("/home/mila/r/razieh.shirzadkhani/TGX-2/data/ml_mooc.csv", index_col=0)
split = data[411740:411749]
data = data.drop(index=[411740,411741,411742,411743,411744,411745,411746,411747,411748])
df2 = pd.concat([data.iloc[:2], split, data.iloc[2:]]).reset_index(drop=True)
df2.to_csv("/home/mila/r/razieh.shirzadkhani/TGX-2/data/ml_mooc_unsorted.csv")