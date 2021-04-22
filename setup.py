"""Frictionless Energy Data Registry

"""

from setuptools import setup, find_packages

setup(
    name="friendly_data_registry",
    version="20210422",
    description="Schema registry for friendly_data",
    url="https://github.com/sentinel-energy/friendly_data_registry",
    packages=find_packages(exclude=["tests"]),
    install_requires=["pyyaml"],
    package_data={
        "friendly_data_registry": [
            "cols/*.json",
            "cols/*.yaml",
            "idxcols/*.json",
            "idxcols/*.yaml",
        ]
    },
    include_package_data=True,
)
