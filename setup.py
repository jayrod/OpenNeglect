# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from os.path import exists
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('OpenNeglect/OpenNeglect.py').read(),
    re.M
    ).group(1)

if exists("README.md"):
    with open("README.md", "rb") as f:
        long_descr = f.read().decode("utf-8")
else:
    long_descr = "Small wrapper for rpcclient",

setup(
    name = "cmdline-OpenNeglect",
    packages = ["OpenNeglect"],
    entry_points = {
        "console_scripts": ['OpenNeglect = OpenNeglect.OpenNeglect:main']
        },
    version = version,
    install_requires = ['markdown-table>=2019.4.13'],
    description = "Small wrapper for rpcclient",
    long_description = long_descr,
    author = "",
    author_email = "",
    )
