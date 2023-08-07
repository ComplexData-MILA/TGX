from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="tgn",
    version="0.0.1",
    description="Temporal graph",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rshirzadkhani/tgn",
    author="Razieh Shirzadkhani",
    author_email="razieh.shirzadkhani@gmail.com",
    keywords="demo project",
    license="MIT",
    packages=["tgn"],
    install_requires=[],
    include_package_data=True,
)