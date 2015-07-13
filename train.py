import sfc
import pandas
from sklearn import cross_validation
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import BaggingClassifier
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
        'Moon',
        'Hour',
        'DayOfWeekInt',
        'Day',
        'Month',
        'Year',
        'PdDistrictInt',
        'TemperatureC',
        'Precipitationmm',
        'InPdDistrict',
        'Conditions',
        'AddressCode',
    ]
    weather_mapping = {
        'Light Drizzle': 1,
        'Drizzle': 2,
        'Light Rain': 3,
        'Rain': 4,
        'Heavy Rain': 5,
        'Thunderstorm': 6,
    }
    data.Precipitationmm = data.Precipitationmm.fillna(-1)
    data.Conditions = data.Conditions.map(weather_mapping).fillna(0)

    train, test = split(data)
    X_train = train[train_vars]
    y_train = train.CategoryInt
    X_test = test[train_vars]
    y_test = test.CategoryInt

    bdt_real_2 = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=8),
        n_estimators=10,
        learning_rate=1
    )

    #bdt_real = DecisionTreeClassifier(max_depth=None, min_samples_split=1,
                                      #random_state=6065)

    bdt_real = BaggingClassifier(base_estimator=bdt_real_2,
                                random_state=6065,
                                n_estimators=100)

    #bdt_real = RandomForestClassifier(random_state=6065,
                                      #n_estimators=200)

    #bdt_real = ExtraTreesClassifier(random_state=6065,
                                    #min_samples_split=5,
                                    #n_estimators=200)

    bdt_real.fit(X_train, y_train)
    y_predict = pandas.Series(bdt_real.predict(X_test))
    print len(y_predict[y_predict == y_test])
    print len(y_predict)
    return bdt_real

bdt = train_classifiers(sfc.get_data('data/all.csv'))
test = sfc.get_data('data/test.csv')
