###############################################################################
from fuzzywuzzy import process
from utils import *
import os
import pickle
import sfc
###############################################################################
__all__ = ['AddressCode']
###############################################################################


class AddressCode(object):
    def __init__(self):
        self.filename = 'pkls/addresscode.pkl'
        self.code = None
        self.choices = None
        self.get()
        return

    def get(self):
        if not os.path.exists(self.filename):
            adds = sfc.get_data('data/train.csv').Address.unique()
            self.code = dict(zip(adds, range(len(adds))))
            with open(self.filename, 'w') as f:
                pickle.dump(self.code, f)
        else:
            with open(self.filename, 'r') as f:
                self.code = pickle.load(f)
        return

    def __call__(self, key):
        if self.code.has_key(key):
            return self.code[key]
        if self.choices is None:
            self.choices = self.code.keys()
        guess = process.extractOne(key, self.choices)
        print key, guess[0]
        self.code[guess[0]] = self.code[key]
        return self.code[guess[0]]


###############################################################################
