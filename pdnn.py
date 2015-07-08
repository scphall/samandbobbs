from matplotlib.colors import ListedColormap
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
        self.weights = 'uniform' # 'distance'
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
        if self.clf is None:
            raise ValueError('No KNN object loaded for saving')
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as f:
            pickle.dump(self.clf, f)
        return

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, 'r') as f:
            self.clf = pickle.load(f)
        return

    def outside_knn_juristictions(self, data):
        xynames = ['X', 'Y']
        newX = copy.deepcopy(data)
        newX['Prob'] = pandas.Series(
            [max(x) for x in self.clf.predict_proba(newX[xynames])]
        )
        newX['Prediction'] = pandas.Series(self.clf.predict(newX[xynames]))
        newX['Actual'] = data['PdDistrictInt']
        newX = newX[newX.Actual != newX.Prediction]
        newX = newX[newX.Prob > 0.9]
        x_min, x_max = data.X.min() - 0.01, data.X.max() + 0.01
        y_min, y_max = data.Y.min() - 0.01, data.Y.max() + 0.01
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
        pl.scatter(newX.X, newX.Y, c=newX.Actual, cmap='jet', alpha=0.5)
        pl.savefig('plots/knn_PD_2.png')
        pl.close(fig)
        return newX.reset_index()


if __name__ == "__main__":
    data = sfc.get_data('data/trim_1e6.csv', drop_data=True)
    knn = Juristictions()
    #knn.train(data)
    #knn.save()
    knn.load()
    outside_data = knn.outside_knn_juristictions(data)
    sfc.write_data(outside_data, 'data/outside_pd.csv',
                   comment='from trim_1e6')
