#!/bin/bash
pip3 uninstall OpenNeglect
python3 setup.py develop
pip3 install -e . --force-reinstall
