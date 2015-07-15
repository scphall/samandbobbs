###############################################################################
from fuzzywuzzy import process
from utils import *
import os
import pandas
import pickle
import sfc
###############################################################################
__all__ = ['AddressCode']
###############################################################################


class AddressCode(object):
    '''Class for turning all addresses into a unique code
    A dictionary of codes is kept in a pickled file
    '''
    def __init__(self):
        # As is, this is not very flexible, but it should not need to be
        self.filename = 'pkls/addresscode.pkl'
        self.code = None
        self.choices = None
        # Automatic
        self.get()
        return

    def add_code(self, add):
        '''Attempt to make all addresses uniform, to remove duplicates A/B B/A
        '''
        add = '/'.join(sorted(add.replace(' ', '').split('/')))
        add = add.replace('Blockof', 'Bo')
        return add

    def get(self):
        '''Pretty much the initialization and setup'''
        # If filename exists, then load, else make it
        if not os.path.exists(self.filename):
            adds = sfc.get_data('data/train.csv').Address.unique()
            adds = pandas.Series([self.add_code(x) for x in adds]).unique()
            self.code = dict(zip(adds, range(len(adds))))
            with open(self.filename, 'w') as f:
                pickle.dump(self.code, f)
        else:
            with open(self.filename, 'r') as f:
                self.code = pickle.load(f)
        return

    def __call__(self, key):
        '''Requires a __call__ in order to use pandas.Series.map'''
        key = self.add_code(key)
        if self.code.has_key(key):
            return self.code[key]
        if self.choices is None:
            self.choices = self.code.keys()
        guess = process.extractOne(key, self.choices)
        print key, guess[0]
        self.code[key] = self.code[guess[0]]
        return self.code[guess[0]]


###############################################################################
