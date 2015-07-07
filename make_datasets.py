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
        data = input
    else:
        raise IOError('Cannot deal with a {}'.format(type(input)))
    # Shrink to random records
    if size is not None and size < len(data):
        random.seed(sfc._SEED)
        data = data.ix[sorted(random.sample(xrange(len(data)), size))]
        data.reset_index()
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
    return copy.deepcopy(df[df.Category.isin(cats)])

###############################################################################



if __name__ == "__main__":
    train = sfc.get_data('data/train.csv')
    trimmed = trim_categories(train)
    # Formatting
    formatter = sfc.DataFormat()
    formatter.add_columns_enumerate(trimmed)
    formatter.add_columns_resolution(trimmed) # Almost certainly not used
    formatter.add_columns_time(trimmed)
    # Make the actual datasets
    make_dataset(trimmed, 'data/trim_1e4.csv', size=10000,
                 comment='Random set of training data. ' \
                 'Selected Categories, 1e4 records')

###############################################################################
