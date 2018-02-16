#!/bin/bash

# TODO : Check parameter here.

SCRIPT=$1
DATASET=$2

git pull
python workspace/$SCRIPT $DATASET
git add -A
git commit -m "[RUN] $SCRIPT $DATASET"
git push
