import os
import zipfile
import pandas
###############################################################################

'''
Some utils to make things easy.
'''


###############################################################################

__author__ = [
    'Sam Hall',
    'Robyn Lucas',
]

__all__ = [
    'get_data', 'write_data', 'time2minutes', 'minutes2time', 'singleton',
    'data2dict',
]

###############################################################################


def get_data(filename, drop_data=False):
    '''Get pandas.DataFrame from .csv or .csv.zip'''
    if not os.path.exists(filename):
        raise IOError('No filename: {}'.format(filename))
    if filename.endswith('.zip'):
        z = zipfile.ZipFile(filename)
        filename = z.open(filename.replace('.zip', ''))
    data = pandas.read_csv(
        filename,
        parse_dates=['Dates'], infer_datetime_format=True,
        comment='#',
    )
    data.Time = data.Dates.map(lambda x: x.time())
    if drop_data:
        data = data[(data.X < -121) & (data.Y < 40)]
        data = data.dropna()
        data = data.reset_index()
    return data


def write_data(df, filename, comment=''):
    '''Don't have to think about index=False with this'''
    with open(filename, 'w') as f:
        if len(comment):
            f.write('# {}\n'.format(comment))
        df.to_csv(f, index=False)
    return


def time2minutes(time):
    '''datetime.time -> int'''
    return 60 * time.hour + time.minute


def minutes2time(mins):
    '''int -> datetime.time'''
    return datetime.time(mins // 60, mins % 60)


def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


def data2dict(df, cat_name, prefix=''):
    '''Takes a pandas.DataFrame and returns a dictionary of DataFrames
    where each key is a unique category name'''
    category_names = df[cat_name].unique()
    cats = {
        prefix + k: df[df[cat_name]==k].reset_index(drop=True)
        for k in category_names
    }
    return cats


###############################################################################
