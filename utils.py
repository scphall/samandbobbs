import os
import zipfile
import pandas
################################################################################

'''
Some utils to make things easy.
'''


################################################################################

__author__ = [
    'Sam Hall',
    'Robyn Lucas',
]

################################################################################


def get_data(filename, drop_data=False):
    '''Get pandas.DataFrame from .csv or .csv.zip'''
    if not os.path.exists(filename):
        raise IOError('No filename: {}'.format(filename))
    if filename.endswith('.zip'):
        z = zipfile.ZipFile('../input/train.csv.zip')
        filename = z.open(filename.replace('.zip', ''))
    data = pandas.read_csv(filename, parse_dates=['Dates'],
                           infer_datetime_format=True)
    data.Time = data.Time = data.Dates.map(lambda x: x.time())
    if drop_data:
        data = data[(data.X<-121) & (data.Y<40)]
        data = data.dropna()
    return data


def write_data(df, filename):
    '''Don't have to think about index=False with this'''
    df.to_csv('data.csv', index=False)
    return


def time2minutes(time):
    '''datetime.time -> int'''
    return 60*time.hour + time.minute


def minutes2time(mins):
    '''int -> datetime.time'''
    return datetime.time(mins//60, mins%60)


################################################################################



