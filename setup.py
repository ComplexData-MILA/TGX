from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="py-tgx",
    version="0.3.0",
    description="Temporal Graph Visualization with TGX",
    url="https://github.com/ComplexData-MILA/TGX",
    keywords="Temporal Graph Visualization",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'appdirs',
        'networkx',
        'numpy',
        'pandas',
        'py-tgb',
        'requests',
        'scikit_learn',
        'scipy',
        'seaborn',
        'sklearn',
        'torch',
        'torch-geometric-temporal',
        'torch_geometric',
        'torch_scatter',
        'torch_sparse',
        'tqdm',
        'wandb',
    ],
)