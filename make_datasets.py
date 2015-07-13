#!/usr/local/bin/python
###############################################################################
import copy
import sfc
import os
import random
import pandas
###############################################################################


def make_dataset(input, output, comment='', size=None):
    sfc.msg('making {}'.format(output))
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
    sfc.msg('Make trimmed datasets')
    train = sfc.get_data('data/train.csv')
    trimmed = trim_categories(train)
    # Formatting
    formatter = sfc.DataFormat()
    trimmed = formatter.add_columns_enumerate(trimmed)
    trimmed = formatter.add_columns_time(trimmed)
    trimmed = formatter.add_weather(trimmed)
    # Make the actual datasets
    make_dataset(trimmed, 'data/trim_1e4.csv', size=10000,
                 comment='Random set of training data. ' \
                 'Selected Categories, 1e4 records')
    make_dataset(trimmed, 'data/trim_1e5.csv', size=100000,
                 comment='Random set of training data. ' \
                 'Selected Categories, 1e5 records')
    make_dataset(trimmed, 'data/trim.csv',
                 comment='Random set of training data. ' \
                 'Selected Categories, all records')
    return


def make_full():
    sfc.msg('Make full dataset')
    train = sfc.get_data('data/train.csv')
    # Formatting
    formatter = sfc.DataFormat()
    train = formatter.add_columns_enumerate(train)
    train = formatter.add_columns_time(train)
    train = formatter.add_weather(train)
    make_dataset(train, 'data/all.csv',
                 comment='All training data')
    return


def make_test():
    sfc.msg('Make test dataset')
    test = sfc.get_data('data/test.csv')
    # Formatting
    formatter = sfc.DataFormat()
    test = formatter.add_columns_enumerate(test)
    test = formatter.add_columns_time(test)
    test = formatter.add_weather(test)
    make_dataset(test, 'data/test_format.csv',
                 comment='Formatted test data')
    test = test.sort('Id', ascending=True).reset_index(drop=True)
    return test


if __name__ == "__main__":
    sfc.msg(1)
    #make_trimmed()
    #make_full()
    make_test()
###############################################################################
