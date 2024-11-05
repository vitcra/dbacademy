import setuptools
from setuptools import find_packages

setuptools.setup(
    version="v3.0.86",
    name="dbacademy",
    author="Databricks, Inc",
    maintainer="Databricks Academy",
    url="https://github.com/databricks-academy/dbacademy",
    install_requires=[],
    package_dir={"": "src"},
    packages=find_packages(where="src")
)
