###############################################################################
import os
import datetime
import pandas
from os.path import join
###############################################################################
'''
Take data from wget data and make a nice csv of all data
SFO is SF airport
SFM is SF midtown, which is rubbish
'''
###############################################################################


class WeatherDataAmalgamate(object):
    def __init__(self):
        self.cols_sfo = [
            'DateUTC',
            'Time',
            'TemperatureC',
            'Humidity',
            'Wind SpeedKm/h',
            'Precipitationmm',
            'Events',
            'Conditions',
        ]
        self.cols_sfm = [
            'DateUTC',
            'Time',
            'TemperatureC',
            'DewpointC',
            'PressurehPa',
            'WindSpeedKMH',
            'Humidity',
            'HourlyPrecipMM',
        ]
        return

    def _make_year_sfo(self, year):
        year = str(year)
        path = 'SFO'
        data_year = pandas.DataFrame()
        months = [str(x) for x in range(1, 13)]
        for month in months:
            for day in xrange(1, 32):
                # Ensure that the date is actually a real date
                try:
                    datetime.date(int(year), int(month), day)
                except ValueError:
                    continue
                filename = join(path, year, month, '{}.csv'.format(day))
                if not os.path.exists(filename):
                    continue
                print filename
                data = pandas.read_csv(filename, infer_datetime_format=True,
                                       parse_dates=['DateUTC', 'Time'])
                data.DateUTC = data.DateUTC.map(lambda x: x.date())
                data.Time = data.Time.map(lambda x: x.time())
                data_year = data_year.append(data, ignore_index=True)
        data_year = data_year.reset_index(drop=True)
        data_year.to_csv(join('SFO', '{}.csv'.format(year)), index=False)
        return

    def _make_year_sfm(self, year):
        year = str(year)
        path = 'SFM'
        data_year = pandas.DataFrame()
        months = [str(x) for x in range(1, 13)]
        for month in months:
            for day in xrange(1, 32):
                # Ensure that the date is actually a real date
                try:
                    datetime.date(int(year), int(month), day)
                except ValueError:
                    continue
                filename = join(path, year, month, '{}.csv'.format(day))
                if not os.path.exists(filename):
                    continue
                print filename
                data = pandas.read_csv(filename, infer_datetime_format=True,
                                       parse_dates=['DateUTC', 'Time'])
                data.DateUTC = data.DateUTC.map(lambda x: x.date())
                data.Time = data.Time.map(lambda x: x.time())
                data_year = data_year.append(data, ignore_index=True)
        data_year = data_year.reset_index(drop=True)
        data_year.to_csv(join('SFM', '{}.csv'.format(year)), index=False)
        return

    def make_years_sfo(self):
        years = range(2003, 2016)
        for year in years:
            self._make_year_sfo(year)
        return

    def make_years_sfm(self):
        years = range(2006, 2016)
        for year in years:
            self._make_year_sfm(year)
        return

    def amalgamate_sfo(self):
        data = pandas.DataFrame()
        years = range(2003, 2016)
        for year in years:
            new = pandas.read_csv('SFO/{}.csv'.format(year))[self.cols_sfo]
            new['DateTime'] = new.DateUTC + ' ' + new.Time
            new.set_index('DateTime')
            data = data.append(new)
        def wind_speed_convert(ws):
            if ws == 'Calm':
                return '0'
            return ws
        data = data[data.TemperatureC>-100]
        data['WindSpeed'] = data['Wind SpeedKm/h'].map(wind_speed_convert)
        data['WindSpeed'] = data['WindSpeed'].astype(float)
        del data['Wind SpeedKm/h']
        del data['DateUTC']
        del data['Time']
        #data = data.reindex(index=data.index[::-1])
        data = data.drop_duplicates(subset='DateTime', take_last=False)
        data = data.reset_index(drop=True)
        data.to_csv('SFO.csv', index=False)
        return

    def amalgamate_sfm(self):
        data = pandas.DataFrame()
        years = range(2006, 2016)
        for year in years:
            new = pandas.read_csv('SFM/{}.csv'.format(year))[self.cols_sfm]
            new['DateTime'] = new.DateUTC + ' ' + new.Time
            new.set_index('DateTime')
            data = data.append(new)
        data = data[data.TemperatureC>-100]
        data['WindSpeed'] = data['WindSpeedKMH']
        del data['WindSpeedKMH']
        del data['DateUTC']
        del data['Time']
        data = data.drop_duplicates(subset='DateTime', take_last=False)
        data = data.reset_index(drop=True)
        data.to_csv('SFM.csv', index=False)
        return

    def amalgamate(self):
        read_opts = {
            'infer_datetime_format': True,
            'parse_dates': ['DateTime'],
        }
        data = pandas.DataFrame()
        data_sfo = pandas.read_csv('SFO.csv', **read_opts)
        data_sfm = pandas.read_csv('SFM.csv', **read_opts)
        cusp = datetime.datetime(2006, 1, 1, 0, 0, 0)
        data_sfo = data_sfo[data_sfo.DateTime < cusp]
        data_sfm = data_sfm[data_sfm.DateTime > cusp]
        data = data.append(data_sfo)
        data = data.append(data_sfm)
        data.to_csv('weee.csv')
        return


###############################################################################
if __name__ == "__main__":
    w = WeatherDataAmalgamate()
    w.make_years_sfo()
    w.amalgamate_sfo()
    #w.make_years_sfm()
    #w.amalgamate_sfm()
    #w.amalgamate()

