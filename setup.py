from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="py-tgx",
    version="0.1.1",
    description="Temporal graph",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/fpour/tgx",
    author="Razieh Shirzadkhani",
    author_email="razieh.shirzadkhani@gmail.com",
    keywords="demo project",
    license="MIT",
    packages=["tgx"],
    install_requires=[],
    include_package_data=True,
)