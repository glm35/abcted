#!/bin/bash

# This script must be run from the project root /path/to/pyapptemplate

export PYTHONPATH=$PYTHONPATH:${PWD}:abcted
python -m unittest discover
