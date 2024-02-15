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
        'appdirs==1.4.4',
        'networkx==3.1',
        'numpy==1.24.2',
        'pandas==1.5.3',
        'py-tgb==0.9.2',
        'requests==2.28.2',
        'scikit_learn==1.3.0',
        'scipy==1.10.1',
        'seaborn==0.13.2',
        'sklearn==0.0',
        'torch==2.0.1',
        'torch-geometric-temporal==0.54.0',
        'torch_geometric==2.3.1',
        'torch_scatter==2.1.1',
        'torch_sparse==0.6.17',
        'tqdm==4.65.0',
        'wandb==0.16.3',
    ],
)