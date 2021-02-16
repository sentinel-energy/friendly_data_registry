"""SENTINEL archive registry

"""

from setuptools import setup, find_packages

setup(
    name="SENTINEL-archive-registry",
    version="0.1.dev0",
    url="https://github.com/sentinel-energy/sentinel-achive-registry",
    packages=find_packages(exclude=["tests"]),
    install_requires=["pyyaml"],
    package_data={"sark_registry": ["cols/*.json", "idxcols/*.json"]},
    include_package_data=True,
)
