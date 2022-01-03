"""Frictionless Energy Data Registry

"""

from pathlib import Path
from setuptools import setup, find_packages

requirements = Path("requirements.txt").read_text().strip().split("\n")

setup(
    name="friendly_data_registry",
    version="20220103",
    description="Schema registry for friendly_data",
    url="https://github.com/sentinel-energy/friendly_data_registry",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
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
