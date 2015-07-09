#!/usr/local/bin/python
###############################################################################
import copy
import sfc
import os
import random
import pandas
###############################################################################


def make_dataset(input, output, comment='', verbose=False, size=None):
    data = None
    # Get the input data
    if isinstance(input, str):
        if not os.path.exists(input):
            input2 = os.path.join('data', input)
            if not os.path.exists(input2):
                raise IOError('Neither {} nor {} exist'.format(input, input2))
            input = input2
        data = sfc.get_data(input)
    elif isinstance(input, pandas.DataFrame):
        data = copy.deepcopy(input)
    else:
        raise IOError('Cannot deal with a {}'.format(type(input)))
    # Shrink to random records
    if size is not None and size < len(data):
        random.seed(sfc._SEED)
        data = data.ix[sorted(random.sample(xrange(len(data)), size))]
        data.reset_index(drop=True)
    sfc.write_data(data, output, comment=comment)
    return


def trim_categories(df):
    cats = [
        'ASSAULT', 'BRIBERY', 'BURGLARY', 'DRIVING UNDER THE INFLUENCE',
        'DRUG/NARCOTIC', 'DRUNKENNESS', 'FORGERY/COUNTERFEITING', 'FRAUD',
        'KIDNAPPING', 'LARCENY/THEFT', 'PROSTITUTION', 'RECOVERED VEHICLE',
        'ROBBERY', 'SEX OFFENSES FORCIBLE', 'STOLEN PROPERTY', 'SUICIDE',
        'VANDALISM', 'VEHICLE THEFT',
    ]
    return copy.deepcopy(df[df.Category.isin(cats)]).reset_index(drop=True)

###############################################################################


def make_trimmed():
    train = sfc.get_data('data/train.csv')
    trimmed = trim_categories(train)
    # Formatting
    formatter = sfc.DataFormat()
    formatter.add_columns_enumerate(trimmed)
    #formatter.add_columns_resolution(trimmed) # Almost certainly not used
    formatter.add_columns_time(trimmed)
    # Make the actual datasets
    make_dataset(trimmed, 'data/trim_1e4.csv', size=10000,
                 comment='Random set of training data. ' \
                 'Selected Categories, 1e4 records')
    make_dataset(trimmed, 'data/trim_1e5.csv', size=100000,
                 comment='Random set of training data. ' \
                 'Selected Categories, 1e5 records')
    make_dataset(trimmed, 'data/trim_1e6.csv', size=1000000,
                 comment='Random set of training data. ' \
                 'Selected Categories, 1e6 records')
    make_dataset(trimmed, 'data/trim.csv',
                 comment='Random set of training data. ' \
                 'Selected Categories, all records')
    return


def make_full():
    train = sfc.get_data('data/train.csv')
    # Formatting
    formatter = sfc.DataFormat()
    formatter.add_columns_enumerate(train)
    formatter.add_columns_time(train)
    make_dataset(train, 'data/all.csv',
                 comment='All training data')
    return


if __name__ == "__main__":
    make_trimmed()
    #make_full()
###############################################################################
