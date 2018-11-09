#! /bin/sh

export PYTHONPATH_SAVE=$PYTHONPATH
export PYTHONPATH=.
python sirtet/main.py
export PYTHONPATH=$PYTHONPATH_SAVE
