import sfc
import pylab as pl


def plot1():
    fig = pl.figure()
    data = sfc.get_data('data/all.csv')
    data.Category = data.Category.map(lambda x: x.capitalize())
    data_day = data[data.Darkness == 0]
    data_dark = data[data.Darkness == 2]
    data_day = data_day.groupby('Category').size()
    data_dark = data_dark.groupby('Category').size()
    data_day = data_day.map(lambda x: float(x) / data_day.sum())
    data_dark = data_dark.map(lambda x: float(x) / data_dark.sum())
    data_day.plot(kind='bar', label='Light', color='b', alpha = 0.5)
    data_dark.plot(kind='bar', label='Dark', color='g', alpha = 0.5)
    fig.subplots_adjust(bottom=0.40)
    pl.legend()
    return

def plot2():
    pass


plot1()
pl.show()
