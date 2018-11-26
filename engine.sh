#! /bin/sh

export PYTHONPATH_SAVE=$PYTHONPATH
export PYTHONPATH=.
python apps/engine/main.py
export PYTHONPATH=$PYTHONPATH_SAVE
