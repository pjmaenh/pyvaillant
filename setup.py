# python setup.py --dry-run --verbose install

from distutils.core import setup

import setuptools

setup(
    name='pyvaillant',
    version="0.0.3",  
    author="Pieter-Jan Maenhaut, based on netatmo-vaillant by Samuel Dumont and netatmo by Hugo Dupras",
    author_email="noreply@pjm.be",
    py_modules=["pyvaillant"],
    packages=["smart_home"],
    package_dir={"smart_home": "smart_home"},
    scripts=[],
    data_files=[],
    url="https://github.com/pjmaenh/pyvaillant",
    license="MIT",
    description="Simple API to access Netatmo weather station data from any Python 3 script. "
    "Designed for (but not limited to) Home-Assitant",
    long_description=open("README.md").read(),
)
