from tgb.linkproppred.dataset import LinkPropPredDataset

name = "tgbl-review"

dataset = LinkPropPredDataset(name=name, root="datasets", preprocess=True)

data = dataset.full_data

type(data['sources']) #all source nodes of edge


