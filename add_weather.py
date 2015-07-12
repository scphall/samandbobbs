import sfc
import pandas
import numpy as np


class AddWeather(object):
    def __init__(self, weather=None):
        self.weather = weather
        if self.weather is None:
            self.weather = 'weather/SFO.csv'
        return

    def add(self, filename):
        finger = 0
        data = sfc.get_data(filename)
        weather = pandas.read_csv(
            self.weather,
            infer_datetime_format=True,
            parse_dates=['DateTime']
        )
        # make both ascending in date
        weather = weather.sort('DateTime', ascending=True)
        weather = weather.reset_index(drop=True)
        data = data.reindex(index=data.index[::-1])
        data = data.reset_index(drop=True)
        new_cols = {k: [None] * len(data) for k in weather.columns}
        for i, date in enumerate(data.Dates):
            while abs(weather.DateTime[finger] - date) > abs(weather.DateTime[finger + 1] - date):
                finger += 1
            for k in weather.columns:
                new_cols[k][i] = weather[k][finger]
        new_data = data.join(pandas.DataFrame(new_cols))
        new_data.reindex(index=new_data.index[::-1])
        return new_data.reset_index(drop=True)


q = AddWeather()
a = q.add('data/trim_1e4.csv')


