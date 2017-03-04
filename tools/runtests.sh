#!/bin/bash

# This script must be run from the project root /path/to/pyapptemplate

export PYTHONPATH=$PYTHONPATH:${PWD}:abcde
python -m unittest discover
