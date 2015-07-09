'''
Kaggle competition - San Fransisco Crime.
In an attempt to do this a bit more properly...

This will make our dataset.
data/train.csv -> data.csv

'''
###############################################################################

__author__ = [
    'Sam Hall',
    'Robyn Lucas',
]

###############################################################################
from utils import *
from dataformatter import DataFormat
###############################################################################
_SEED = 31966
_VERBOSE = 0


def msg(level, message):
    global _VERBOSE
    if level >= _VERBOSE:
        print message
    return
