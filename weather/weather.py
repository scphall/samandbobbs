import os
import datetime
import pandas
from os.path import join


class WeatherDataAmalgamate(object):
    def __init__(self):
        return

    def _make_year_sfo(self, year):
        year = str(year)
        cols = [
            'DateUTC',
            'Time',
            'TemperatureC',
            'Humidity',
            'Wind SpeedKm/h',
            'Precipitationmm',
            'Events',
            'Conditions',
        ]
        path = 'SFO'
        data_year = pandas.DataFrame()
        months = [str(x) for x in range(1, 13)]
        for month in months:
            for day in xrange(1, 32):
                try:
                    datetime.date(int(year), int(month), day)
                except ValueError:
                    continue
                filename = join(path, year, month, '{}.csv'.format(day))
                if not os.path.exists(filename):
                    continue
                print filename
                data = pandas.read_csv(filename)
                data['Time'] = data.TimePST if 'TimePST' in data.columns \
                    else data.TimePDT
                data = data[cols].set_index('DateUTC')
                data_year = data_year.append(data)
        data_year.to_csv(join('SFO', '{}.csv'.format(year)))
        return

    def make_years_sfo(self):
        years = range(2003, 2016)
        for year in years:
            self._make_year_sfo(year)
        return

    def amalgamate_sfo(self)
    data = pandas.DataFrame()
    for year in years:
        data = data.append(
            pandas.read_csv('SFO/{}.csv'.format(year)).set_index('DateUTC')
        )
        def wind_speed_convert(ws):
            if ws == 'Calm':
                return '0'
            return ws
        data = data[data.TemperatureC>-100]
        data['WindSpeed'] = data['Wind SpeedKm/h'].map(wind_speed_convert)
        data['WindSpeed'] = data['WindSpeed'].astype(float)
        del data['Wind SpeedKm/h']
        conditions_mapping = {
            'Partly Cloudy',
            'Scattered Clouds',
            'Mostly Cloudy',
            'Overcast',
            'Clear',
            'Patches of Fog',
            'Fog',
            'Haze',
            'Light Rain',
            'Rain',
            'Drizzle',
            'Heavy Rain',
            'Thunderstorm',
            'Heavy Thunderstorms and Rain',
            'Smoke',
            'Unknown',
            'Mist',
            'Thunderstorms and Rain',
            'Light Drizzle',
            'Light Thunderstorms and Rain',
            'Thunderstorms with Small Hail',
            'Light Ice Pellets',
            'Squalls',
            'Thunderstorms and Ice Pellets',
            'Ice Pellets',
            'Shallow Fog',
            'Heavy Thunderstorms with Small Hail'
        }
        data.to_csv('SFO.csv')
        return


if __name__ == "__main__":
    w = WeatherDataAmalgamate()
    w.make_years_sfo()
    w.amalgamate_sfo()

