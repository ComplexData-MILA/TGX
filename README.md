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

install Pytorch and PyG dependencies (#! currently not used)
```
pip install torch==2.0.0 --index-url https://download.pytorch.org/whl/cu117
pip install torch_geometric==2.3.0
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.0.0+cu117.html
```

3. install local dependencies under root directory `/TGX`
```
pip install -e py-tgx
```

