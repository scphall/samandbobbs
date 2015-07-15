#!/usr/bin/python
###############################################################################
from collections import OrderedDict
import datetime
import numpy as np
import pandas
import pylab as pl
import sfc
import seaborn as sns
###############################################################################

###############################################################################
'''
Kaggle competition - San Fransisco Crime.

Make some plots.

'''
###############################################################################

__author__ = [
    'Sam Hall',
    'Robyn Lucas',
]

###############################################################################
# Plotting class

class Plot2D(object):
    def __init__(self):
        map_loc = "data/sf_map_copyright_openstreetmap_contributors.txt"
        self.mapdata = np.loadtxt(map_loc)
        self.aspect = float(self.mapdata.shape[0]) / self.mapdata.shape[1]
        self.lon_lat_box = (-122.5247, -122.3366, 37.699, 37.8299)
        self.clipsize = [[-122.5247, -122.3366], [37.699, 37.8299]]

    def _plot(self, df, name):
        fig = pl.figure(figsize=(10, 10*self.aspect))
        try:
            ax = sns.kdeplot(df.X, df.Y, clip=self.clipsize,
                             aspect=1/self.aspect,
                             shade=False, shade_lowest=False,
                             alpha=0.7, cmap='Blues')
        except ValueError:
            print 'Problem with {}.'.format(name),
            print 'Perhaps the number of entries is too small.'
            return
        ax.imshow(self.mapdata, cmap=pl.get_cmap('gray'),
                  extent=self.lon_lat_box, aspect=self.aspect)
        pl.savefig(
            'plots/map_{}.pdf'.format(name.replace('/', '_').replace(' ', '_'))
        )
        pl.close(fig)
        return


    def plot(self, df, name=None):
        if isinstance(df, pandas.DataFrame):
            self._plot(df, name, size)
        elif isinstance(df, dict):
            for k, v in df.iteritems():
                self._plot(v, k)
        else:
            raise TypeError('Cannot plot type {}'.format(type(df)))
        return

    def plot_scatter(self, cats, name):
        fig = pl.figure(figsize=(10, 10*self.aspect))
        cols = iter(pl.cm.rainbow(np.linspace(0,1,len(cats))))
        for col, (k, v) in enumerate(cats.iteritems()):
            pl.scatter(v.X, v.Y, alpha=0.3, label=k.capitalize(),
                       marker=',', c=cols.next())
        pl.imshow(self.mapdata, cmap=pl.get_cmap('gray'),
                  extent=self.lon_lat_box, aspect=self.aspect)
        pl.legend(scatterpoints=1, bbox_to_anchor=(1,0.6))
        pl.savefig(
            'plots/map_{}.png'.format(name.replace('/', '_').replace(' ', '_'))
        )
        pl.close(fig)
        return

###############################################################################
# Some functions


def get_time_df(cats, bins=24):
    time_range = [datetime.time(h, m) for h in range(24) for m in range(60)]
    category_names = cats.keys()
    times = pandas.DataFrame(index=time_range, columns=category_names)
    groups = {k:v.groupby('Time') for k, v in cats.iteritems()}
    for cat, group in groups.iteritems():
        for i, j in group:
            times.ix[i][cat] = len(j)
            times = times.fillna(0)
    all_bins = []
    bin_width = 24*60 / bins
    time_range = []
    for b in xrange(bins):
        bin_times = times[b*bin_width:(b+1)*bin_width]
        t1, t2 = bin_times.index[0], bin_times.index[-1]
        m = (t1.hour*60 + t1.minute + t2.hour*60 + t2.minute) / 2
        all_bins.append(bin_times.sum())
        time_range.append(datetime.time(m/60, m%60))
    df_out = pandas.concat(all_bins, axis=1).T
    df_out.index = time_range
    return df_out


def sort_categories_by_frequency(cats):
    order = sorted(cats, key=lambda x: len(cats[x]))
    out = OrderedDict()
    for i in order:
        out[i] = cats[i]
    return out


###############################################################################

if __name__ == "__main__":
    df = sfc.get_data('data/trim_1e5.csv', drop_data=True)
    cats = sfc.data2dict(df, 'Category')
    #pds = sfc.data2dict(df, 'PdDistrict')
    #plotter = Plot2D()
    #plotter.plot(cats)
    plotter.plot_scatter(pds, 'PDs')
    pds_theft = {k:v[v.Category=='VEHICLE THEFT'] for k, v in pds.iteritems()}
    plotter.plot_scatter(pds_theft, 'PDs_VehicleTheft')

###############################################################################
