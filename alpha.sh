#! /bin/sh

export PYTHONPATH_SAVE=$PYTHONPATH
export PYTHONPATH=.
python apps/alpha/main.py
export PYTHONPATH=$PYTHONPATH_SAVE
