from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="py-tgx",
    version="0.3.1",
    description="Temporal Graph Visualization with TGX",
    url="https://github.com/ComplexData-MILA/TGX",
    keywords="Temporal Graph Visualization",
    license="MIT",
    packages=find_packages(),
)