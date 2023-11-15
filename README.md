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

### Creating new branch ###

first create the branch on github
```
git fetch origin

git checkout -b test origin/test
```