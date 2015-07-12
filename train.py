import sfc
import pandas
from sklearn import cross_validation
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
import pylab as pl


def split(data):
    train, test = cross_validation.train_test_split(data, random_state=6065)
    #train, test = cross_validation.train_test_split(data)
    return train, test

def address_code(data):
    pass

def train_classifiers(data):
    train_vars = [
        'X', 'Y',
        'Darkness',
        #'Moon',
        'Minutes',
        #'Hour',
        'DayOfWeekInt',
        #'Day',
        'Month',
        'Year',
        'PdDistrictInt',
        #'AddCode',
        #'InPdDistrict',
    ]
    adds = data.Address
    conv = {}
    count = 0
    for add in adds.unique():
        conv[add] = count
        count += 1
    #data['AddCode'] = data.Address.map(lambda x: conv[x])
    #data['Moon'] = data.Moon.map(lambda x: x // 7)
    #data['Hour'] = data.Minutes.map(lambda x: x // 60)
    train, test = split(data)
    X_train = train[train_vars]
    y_train = train.CategoryInt
    X_test = test[train_vars]
    y_test = test.CategoryInt

    bdt_real = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=8),
        n_estimators=800,
        random_state=6065,
        learning_rate=1)

    bdt_real.fit(X_train, y_train)

    y_predict = pandas.Series(bdt_real.predict(X_test))

    print len(y_predict[y_predict == y_test])
    print len(y_predict)
    #pl.show()
    return


train_classifiers(sfc.get_data('data/trim_1e4.csv'))






