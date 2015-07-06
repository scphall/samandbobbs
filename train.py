import pylab as pl
import re
import datetime
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import AdaBoostClassifier
import scipy
import zipfile
import os
import astral
from collections import OrderedDict


def time2mins(t):
    return 60*t.hour + t.minute


class Names2Int(object):
    def __init__(self):
        self.day2int = dict(zip(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday'
             'Friday', 'Saturday', 'Sunday'], range(7)
        ))
        cats = [
            'WARRANTS', 'OTHER OFFENSES', 'LARCENY/THEFT', 'VEHICLE THEFT',
            'VANDALISM', 'NON-CRIMINAL', 'ROBBERY', 'ASSAULT', 'WEAPON LAWS',
            'BURGLARY', 'SUSPICIOUS OCC', 'DRUNKENNESS',
            'FORGERY/COUNTERFEITING', 'DRUG/NARCOTIC', 'STOLEN PROPERTY',
            'SECONDARY CODES', 'TRESPASS', 'MISSING PERSON', 'FRAUD',
            'KIDNAPPING', 'RUNAWAY', 'DRIVING UNDER THE INFLUENCE',
            'SEX OFFENSES FORCIBLE', 'PROSTITUTION', 'DISORDERLY CONDUCT',
            'ARSON', 'FAMILY OFFENSES', 'LIQUOR LAWS', 'BRIBERY',
            'EMBEZZLEMENT', 'SUICIDE', 'LOITERING', 'SEX OFFENSES NON FORCIBLE',
            'EXTORTION', 'GAMBLING', 'BAD CHECKS', 'TREA', 'RECOVERED VEHICLE',
            'PORNOGRAPHY/OBSCENE MAT'
        ]
        resolutions = [
            'NONE', 'ARREST, BOOKED', 'ARREST, CITED', 'PSYCHOPATHIC CASE',
            'JUVENILE BOOKED', 'UNFOUNDED', 'EXCEPTIONAL CLEARANCE', 'LOCATED',
            'CLEARED-CONTACT JUVENILE FOR MORE INFO', 'NOT PROSECUTED',
            'JUVENILE DIVERTED', 'COMPLAINANT REFUSES TO PROSECUTE',
            'JUVENILE ADMONISHED', 'JUVENILE CITED',
            'DISTRICT ATTORNEY REFUSES TO PROSECUTE',
            'PROSECUTED BY OUTSIDE AGENCY', 'PROSECUTED FOR LESSER OFFENSE'
        ]
        districts = ['NORTHERN', 'PARK', 'INGLESIDE', 'BAYVIEW', 'RICHMOND', 'CENTRAL',
                     'TARAVAL', 'TENDERLOIN', 'MISSION', 'SOUTHERN']
        self.category2int = dict(zip(cats, range(len(cats))))
        self.pddistrict2int = dict(zip(districts, range(len(districts))))
        self.resolution2int = dict(zip(resolutions, range(len(resolutions))))

    def add_columns_enumerate(self, df):
        df['CategoryInt'] = df.Category.map(self.category2int)
        df['DayOfWeekInt'] = df.DayOfWeek.map(self.day2int)
        df['PdDistrictInt'] = df.PdDistrict.map(self.pddistrict2int)
        df['AddressCode'] = df.Address.map(lambda x: [
            y.strip() for y in re.sub(' ST| AV| BL| WY| Block of', '', x).split('/')
        ])
        return

    def add_columns_resolution(self, df):
        df['IsJuvenile'] = df.Resolution.str.contains('JUVENILE')
        df['IsBooked'] = df.Resolution.str.contains('BOOKED')
        df['IsCited'] = df.Resolution.str.contains('CITED')
        df['IsArrested'] = df.Resolution.str.contains('ARREST')
        df['IsProsecuted'] = (
            (df.Resolution=='NOT PROSECUTED') |
            (df.Resolution=='COMPLAINANT REFUSES TO PROSECUTE') |
            (df.Resolution=='DISTRICT ATTORNEY REFUSES TO PROSECUTE')
        ).astype(int) * -1 + (
            (df.Resolution=='PROSECUTED BY OUTSIDE AGENCY') |
            (df.Resolution=='PROSECUTED FOR LESSER OFFENSE')
        ).astype(int)
        return

    def add_columns_time(self, df):
        # A single location object should suffice, average long-lat and elevation is 16m (wiki)
        location = astral.Location(('SF', 'America', df.Y.mean(), df.X.mean(),
                                    'America/Los_Angeles', 16))
        #df['Date'] = df.Dates.map(
            #lambda d :
            #datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S'),
        #)
        # Time in minutes is better
        df['Time'] = df.Dates.map(lambda d : time2mins(d))
        df['Month'] = df.Dates.map(lambda d : d.month)
        df['Year'] = df.Dates.map(lambda d : d.year)
        sunset = df.Dates.map(lambda d : time2mins(location.sunset(d)))
        sunrise = df.Dates.map(lambda d : time2mins(location.sunrise(d)))
        dusk = df.Dates.map(lambda d : time2mins(location.dusk(d)))
        dawn = df.Dates.map(lambda d : time2mins(location.dawn(d)))
        # 0 : Day, 1 : Dusk, 2 : Dark, 3 : Dawn
        df['Darkness'] = \
                ((df.Time<dusk) & (df.Time>sunset)).astype(int) * 1 + \
                ((df.Time<dawn) | (df.Time>dusk)).astype(int) * 2 + \
                ((df.Time>dawn) & (df.Time<sunrise)).astype(int) * 3
        return

    def details(self, df):
        replacements = '()[].,\'\"/-$0123456789'
        replacements = dict(zip(replacements, ' '*len(replacements)))
        all_details = df.Descript.unique()
        all_details = ' '.join(all_details)
        all_words = ''.join([replacements.get(x, x) for x in all_details])
        all_words = pandas.Series([w for w in all_words.split(' ') if len(w)>3]).unique()
        return all_words


def get_train_data():
    pathname = 'data'
    data = pd.read_csv(os.path.join(pathname, 'train.csv'),
                       parse_dates=['Dates'],
                       infer_datetime_format=True)
    return data


def train(data):
    '''Does not work.
    At all.
    Yet.'''
    classifier = AdaBoostClassifier()
    print 'Train'
    classifier.fit(data[[
        'DayOfWeekInt'
    ]], data.Category)
    return classifier


data = get_train_data()
c = Names2Int()
c.add_columns_enumerate(data)
c.add_columns_resolution(data)
c.add_columns_time(data)
data.to_csv('data.csv', index=False)
#words = c.details(data)
#print data.head()


#train(data)



#if __name__ == "__main__":
    #train(data)


