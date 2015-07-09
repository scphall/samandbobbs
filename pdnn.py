from matplotlib.colors import ListedColormap
from sklearn.externals import joblib # Apparently better for this than pickle
from sklearn import datasets
from sklearn import neighbors
import copy
import sfc
import numpy as np
import pandas
import pickle
import pylab as pl


class Juristictions(object):
    def __init__(self):
        self.n_neighbors = 20
        self.step = 0.001
        self.weights = 'distance'
        self.weights = 'uniform'
        self.clf = None
        self.filename = 'pkls/knn_pds.pkl'
        return

    def train(self, data):
        X = data[['X', 'Y']]
        y = data.PdDistrictInt
        self.clf = neighbors.KNeighborsClassifier(
            self.n_neighbors, weights=self.weights
        )
        self.clf.fit(X, y)
        x_min, x_max = X.X.min() - 0.01, X.X.max() + 0.01
        y_min, y_max = X.Y.min() - 0.01, X.Y.max() + 0.01
        xx, yy = np.meshgrid(
            np.arange(x_min, x_max, self.step),
            np.arange(y_min, y_max, self.step)
        )
        Z = self.clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        fig = pl.figure()
        pl.xlim(xx.min(), xx.max())
        pl.ylim(yy.min(), yy.max())
        pl.pcolormesh(xx, yy, Z, cmap='jet', alpha=0.1)
        pl.savefig('plots/knn_PDregions.png')
        pl.scatter(X.X, X.Y, c=y, cmap='jet', alpha=0.2)
        pl.savefig('plots/knn_PD.png')
        pl.close(fig)
        return

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        joblib.dump(self.clf, filename)
        return

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        self.clf = joblib.load(filename)
        return

    def outside_juristiction(self, data):
        data = copy.deepcopy(data)
        xynames = ['X', 'Y']
        data['Prediction'] = pandas.Series(self.clf.predict(data[xynames]))
        data = data[data.PdDistrictInt != data.Prediction]
        data = data.reset_index(drop=True)
        data['Prob'] = pandas.Series(
            [max(x) for x in self.clf.predict_proba(data[xynames])]
        )
        data = data[data.Prob > 0.95].reset_index(drop=True)
        fig = pl.figure()
        x_min, x_max = data.X.min() - 0.01, data.X.max() + 0.01
        y_min, y_max = data.Y.min() - 0.01, data.Y.max() + 0.01
        xx, yy = np.meshgrid(
            np.arange(x_min, x_max, self.step),
            np.arange(y_min, y_max, self.step)
        )
        Z = self.clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        pl.xlim(xx.min(), xx.max())
        pl.ylim(yy.min(), yy.max())
        pl.pcolormesh(xx, yy, Z, cmap='jet', alpha=1.0)
        pl.scatter(data.X, data.Y, c=data.PdDistrictInt, cmap='jet', alpha=1.0)
        pl.savefig('plots/knn_PD_2.png')
        pl.close(fig)
        return data

    def plot(self, filename):
        indices = ['Category']
        data = sfc.get_data(filename)[indices]
        data.Category = data.Category.map(lambda x: x.capitalize())
        groups = data.groupby('Category')
        fig = pl.figure()
        groups.size().plot(kind='bar')
        fig.subplots_adjust(bottom=0.35)
        pl.savefig('plots/categories_outside_pd.pdf)
        pl.show()
        return


###############################################################################


def main(load=True):
    indices = ['X', 'Y', 'PdDistrictInt']
    train = sfc.get_data('data/trim_1e4.csv', drop_data=True)[indices]
    all = sfc.get_data('data/all.csv', drop_data=True)
    knn = Juristictions()
    if load:
        knn.load()
    else:
        knn.train(train)
        knn.save()
    data = knn.outside_juristiction(all)
    sfc.write_data(data, 'data/outside_pd.csv', comment='Outside juristiction')
    return


###############################################################################


if __name__ == "__main__":
    main(False)
    knn = Juristictions()
    knn.plot('data/outside_pd.csv')

###############################################################################
