#!/bin/bash

set -eux

echo "check with flake8"
python -m flake8

echo "check with isort"
isort -c .

echo "check with pyright"
pyright -p `dirname "$0"` .