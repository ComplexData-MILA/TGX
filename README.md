<!-- # TGX -->
![TGX logo](docs/2023_TGX_logo.png)

# Temporal Graph Analysis with TGX
<h4>
	<a href="https://arxiv.org/abs/2402.03651"><img src="https://img.shields.io/badge/arXiv-pdf-yellowgreen"></a>
	<a href="https://pypi.org/project/py-tgx/"><img src="https://img.shields.io/pypi/v/py-tgx.svg?color=brightgreen"></a>
	<a href="https://complexdata-mila.github.io/TGX/"><img src="https://img.shields.io/badge/docs-orange"></a>
</h4> 

This repository contains the code for the paper "Temporal Graph Analysis with TGX" (WSDM 2024, Demo Track).

TGX overview:
- TGX supports all datasets from [TGB](https://tgb.complexdatalab.com/) and [Poursafaei et al. 2022](https://openreview.net/forum?id=1GVpwr2Tfdg) as well as any custom dataset in `.csv` format. 
- TGX provides numerous temporal graph visualization plots and statistics out of the box.


## Dependecies
TGX implementation works with `python >= 3.9` and can be installed as follows.

1. Set up virtual environment (conda should work as well).
	```
	python -m venv tgx_env/
	source tgx_env/bin/activate
	```

2. Upgrade pip (Optional)
	```
	pip install --upgrade pip
	```

3. Install external packages
	```
	pip install -r requirements.txt
	```

4. Install local dependencies under root directory `/TGX`.
	```
	pip install -e .
	```

5. [Aternative] Install TGX from [`PyPi`](https://pypi.org/project/py-tgx/):

	```
	pip install py-tgx
	```

6. [optional] Install `mkdocs` dependencies to serve the documentation locally.
	```
	pip install mkdocs mkdocs-material mkdocstrings-python mkdocs-glightbox mkdocs-jupyter ipython_genutils
	```


For tutorials on how to use TGX to generate visualizations and compute statistics for temporal graphs, see [`docs/tutorials/data_viz_stats.ipynb`](https://github.com/ComplexData-MILA/TGX/blob/master/docs/tutorials/data_viz_stats.ipynb)


### Citation
If TGX is useful for your work, please consider citing it:
```bibtex
@article{shirzadkhani2024temporal,
  title={Temporal Graph Analysis with TGX},
  author={Shirzadkhani, Razieh and Huang, Shenyang and Kooshafar, Elahe and Rabbany, Reihaneh and Poursafaei, Farimah},
  journal={arXiv preprint arXiv:2402.03651},
  year={2024}
}
```
