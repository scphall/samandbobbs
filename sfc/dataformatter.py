#!/usr/bin/python
###############################################################################
from utils import *
import astral
import datetime
import pandas
import re
###############################################################################

'''
Kaggle competition - San Fransisco Crime.
In an attempt to do this a bit more properly...

This will make our dataset.
data/train.csv -> data.csv

'''


###############################################################################

__author__ = [
    'Sam Hall',
    'Robyn Lucas',
]

###############################################################################
# Class


@singleton
class DataFormat(object):
    '''Class to take initial dataset and format it as required.
    Should make it a singleton or something.
    '''
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.day2int = dict(zip(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
             'Friday', 'Saturday', 'Sunday'], range(7)
        ))
        cats = [
            'ARSON', 'ASSAULT', 'BAD CHECKS', 'BRIBERY', 'BURGLARY',
            'DISORDERLY CONDUCT', 'DRIVING UNDER THE INFLUENCE',
            'DRUG/NARCOTIC', 'DRUNKENNESS', 'EMBEZZLEMENT', 'EXTORTION',
            'FAMILY OFFENSES', 'FORGERY/COUNTERFEITING', 'FRAUD', 'GAMBLING',
            'KIDNAPPING', 'LARCENY/THEFT', 'LIQUOR LAWS', 'LOITERING',
            'MISSING PERSON', 'NON-CRIMINAL', 'OTHER OFFENSES',
            'PORNOGRAPHY/OBSCENE MAT', 'PROSTITUTION', 'RECOVERED VEHICLE',
            'ROBBERY', 'RUNAWAY', 'SECONDARY CODES', 'SEX OFFENSES FORCIBLE',
            'SEX OFFENSES NON FORCIBLE', 'STOLEN PROPERTY', 'SUICIDE',
            'SUSPICIOUS OCC', 'TREA', 'TRESPASS', 'VANDALISM', 'VEHICLE THEFT',
            'WARRANTS', 'WEAPON LAWS',
        ]
        resolutions = [
            'NONE', 'ARREST, BOOKED', 'ARREST, CITED',
            'CLEARED-CONTACT JUVENILE FOR MORE INFO',
            'COMPLAINANT REFUSES TO PROSECUTE',
            'DISTRICT ATTORNEY REFUSES TO PROSECUTE', 'EXCEPTIONAL CLEARANCE',
            'JUVENILE ADMONISHED', 'JUVENILE BOOKED', 'JUVENILE CITED',
            'JUVENILE DIVERTED', 'LOCATED', 'NOT PROSECUTED',
            'PROSECUTED BY OUTSIDE AGENCY', 'PROSECUTED FOR LESSER OFFENSE',
            'PSYCHOPATHIC CASE', 'UNFOUNDED',
        ]
        districts = ['BAYVIEW', 'CENTRAL', 'INGLESIDE', 'MISSION', 'NORTHERN',
                     'PARK', 'RICHMOND', 'SOUTHERN', 'TARAVAL', 'TENDERLOIN']
        self.category2int = dict(zip(cats, range(len(cats))))
        self.pddistrict2int = dict(zip(districts, range(len(districts))))
        self.resolution2int = dict(zip(resolutions, range(len(resolutions))))
        return

    def add_columns_enumerate(self, df):
        '''Adding enumerations to DataFile'''
        if self.verbose:
            print __doc__
        df['CategoryInt'] = df.Category.map(self.category2int)
        df['DayOfWeekInt'] = df.DayOfWeek.map(self.day2int)
        df['PdDistrictInt'] = df.PdDistrict.map(self.pddistrict2int)
        #re_string = ' ST| AV| BL| WY'
        #df['AddressCode'] = df.Address.map(
            #lambda x: [
                #y.strip() for y in
                #re.sub(re_string, '', x).replace('Block of ', 'BO').split('/')
            #]
        #)
        return

    def add_columns_resolution(self, df):
        '''Adding enumerations of resolutions to pandas.DataFile'''
        if self.verbose:
            print __doc__
        df['IsJuvenile'] = df.Resolution.str.contains('JUVENILE')
        df['IsBooked'] = df.Resolution.str.contains('BOOKED')
        df['IsCited'] = df.Resolution.str.contains('CITED')
        df['IsArrested'] = df.Resolution.str.contains('ARREST')
        df['IsProsecuted'] = (
            (df.Resolution == 'NOT PROSECUTED') |
            (df.Resolution == 'COMPLAINANT REFUSES TO PROSECUTE') |
            (df.Resolution == 'DISTRICT ATTORNEY REFUSES TO PROSECUTE')
        ).astype(int) * -1 + (
            (df.Resolution == 'PROSECUTED BY OUTSIDE AGENCY') |
            (df.Resolution == 'PROSECUTED FOR LESSER OFFENSE')
        ).astype(int)
        return

    def add_columns_time(self, df):
        '''Add columns about the time.
        Astral class uses average long=lat and elevation is 16m (wiki).'''
        if self.verbose:
            print 'Adding enumerations of resolutions to DataFile'
        location = astral.Location(('SF', 'America', df.Y.mean(), df.X.mean(),
                                    'America/Los_Angeles', 16))
        # Time in minutes is better for playing with
        df['Minutes'] = df.Dates.map(lambda d: time2minutes(d))
        df['Month'] = df.Dates.map(lambda d: d.month)
        df['Year'] = df.Dates.map(lambda d: d.year)
        sunset = df.Dates.map(lambda d: time2minutes(location.sunset(d)))
        sunrise = df.Dates.map(lambda d: time2minutes(location.sunrise(d)))
        dusk = df.Dates.map(lambda d: time2minutes(location.dusk(d)))
        dawn = df.Dates.map(lambda d: time2minutes(location.dawn(d)))
        df['Moon'] = df.Dates.map(lambda d: location.moon_phase(d))
        # 0 : Day, 1 : Dusk, 2 : Dark, 3 : Dawn
        df['Darkness'] = \
            ((df.Minutes < dusk) & (df.Minutes > sunset)).astype(int) + \
            ((df.Minutes < dawn) | (df.Minutes > dusk)).astype(int) * 2 + \
            ((df.Minutes > dawn) & (df.Minutes < sunrise)).astype(int) * 3
        df['Sunset'] = sunset
        df['Sunrise'] = sunrise
        df['Dusk'] = dusk
        df['Dawn'] = dawn
        return

    def details(self, df):
        '''Unused'''
        replacements = '()[].,\'\"/-$0123456789'
        replacements = dict(zip(replacements, ' '*len(replacements)))
        all_details = df.Descript.unique()
        all_details = ' '.join(all_details)
        all_words = ''.join([replacements.get(x, x) for x in all_details])
        all_words = pandas.Series(
            [w for w in all_words.split(' ') if len(w) > 3]
        ).unique()
        return all_words

###############################################################################


if __name__ == "__main__":
    data = get_data('data/train_1e4.csv')
    formatter = DataFormat()
    formatter.add_columns_enumerate(data)
    formatter.add_columns_resolution(data)
    formatter.add_columns_time(data)
    write_data(data, 'data.csv')

###############################################################################
