<!-- # TGB -->
![TGB logo](imgs/2023_TGX_logo.png)

# Temporal Graph Analysis with TGX (WSDM 2024 Demo Track)
<h4>
	<a href="https://arxiv.org/abs/2402.03651"><img src="https://img.shields.io/badge/arXiv-pdf-yellowgreen"></a>
	<a href="https://complexdata-mila.github.io/TGX/"><img src="https://img.shields.io/badge/docs-orange"></a>
</h4> 

<!-- <a href="https://pypi.org/project/py-tgb/"><img src="https://img.shields.io/pypi/v/py-tgb.svg?color=brightgreen"></a>
<a href="https://tgb.complexdatalab.com/"><img src="https://img.shields.io/badge/website-blue"></a> -->


### Example Usage ###
TGX provides many built in datasets as well as supporting TGB datasets. In addition, TGX provides dataset discretization and visualization.
To get started, see our [starting example](https://github.com/ComplexData-MILA/TGX/blob/master/starting_example.py)
```
python starting_example.py -d tgbl-wiki -t daily
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
