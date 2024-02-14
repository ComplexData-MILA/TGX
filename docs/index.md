<!-- # TGX -->
![TGX logo](2023_TGX_logo.png)

# Temporal Graph Analysis with TGX (WSDM 2024 Demo Track)
<h4>
	<a href="https://arxiv.org/abs/2402.03651"><img src="https://img.shields.io/badge/arXiv-pdf-yellowgreen"></a>
	<a href="https://complexdata-mila.github.io/TGX/"><img src="https://img.shields.io/badge/docs-orange"></a>
</h4> 

TGX supports all datasets from [TGB](https://tgb.complexdatalab.com/) and [Poursafaei et al. 2022](https://openreview.net/forum?id=1GVpwr2Tfdg) as well as any custom dataset in `.csv` format. 
TGX provides numerous temporal graph visualization plots and statistics out of the box


### Data Loading ###
For detailed tutorial on how to load the datasets into `tgx.Graph`, see [`docs/tutorials/data_loader.ipynb`](https://github.com/ComplexData-MILA/TGX/blob/master/docs/tutorials/data_loader.ipynb)

1. Load TGB datasets
```
import tgx
dataset = tgx.tgb_data("tgbl-wiki")
ctdg = tgx.Graph(dataset)
```

2. Load built-in datasets
```
dataset = tgx.builtin.uci()
ctdg = tgx.Graph(dataset)
```

3. Load custom datasets from `.csv` 
```
from tgx.io.read import read_csv
toy_fname = "docs/tutorials/toy_data.csv"
edgelist = read_csv(toy_fname, header=True,index=False, t_col=0,)
tgx.Graph(edgelist=edgelist)
```

### Visualization and Statistics ###
For detailed tutorial on how to generate visualizations and compute statistics for temporal graphs, see [`docs/tutorials/data_viz_stats.ipynb`](https://github.com/ComplexData-MILA/TGX/blob/master/docs/tutorials/data_viz_stats.ipynb)

1. Discretize the network (required for viz)

```
dataset = tgx.builtin.uci()
ctdg = tgx.Graph(dataset)
time_scale = "weekly"
dtdg, ts_list = ctdg.discretize(time_scale=time_scale, store_unix=True)
```

2. Plot the number of nodes over time

```
tgx.degree_over_time(dtdg, network_name="uci")
```

3. Compute novelty index
```
tgx.get_novelty(dtdg)
```


### Install dependency
Our implementation works with python >= 3.9 and can be installed as follows

1. set up virtual environment (conda should work as well)
```
python -m venv ~/tgx_env/
source ~/tgx_env/bin/activate
```

2. install external packages
```
pip install -r requirements.txt
```

3. install local dependencies under root directory `/TGX`
<!-- ```
pip install -e py-tgx
``` -->
```
pip install -e .
```



3. [alternatively] install from test-pypi

```
pip install -i https://test.pypi.org/simple/ py-tgx
```
You can specify the version with `==`, note that the pypi version might not always be the most updated version


4. [optional] install mkdocs dependencies to serve the documentation locally
```
pip install mkdocs-glightbox
```

### Creating new branch ###

first create the branch on github
```
git fetch origin

git checkout -b test origin/test
```
