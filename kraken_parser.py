import pandas as pd
import krakenex

import datetime
import calendar
import time


def date_nix(str_date):
    return calendar.timegm(str_date.timetuple())


def date_str(nix_time):
    return datetime.datetime.fromtimestamp(nix_time).strftime('%m, %d, %Y')


def date(start, end, ofs):
    req_data = {'type': 'all',
                'trades': 'true',
                'start': str(date_nix(start)),
                'end': str(date_nix(end)),
                'ofs': str(ofs)
                }
    return req_data

k = krakenex.API()
k.load_key('kraken.key')

data = []
count = 0
for i in range(1,11):
    start_date = datetime.datetime(2016, i+1, 1)
    end_date = datetime.datetime(2016, i+2, 29)
    th = k.query_private('TradesHistory', date(start_date, end_date, 1))
    time.sleep(.25)
    print(th)
    th_error = th['error']
    try:
        if int(th['result']['count'])>0:
            count += th['result']['count']
            data.append(pd.DataFrame.from_dict(th['result']['trades']).transpose())
    except Exception as e:
        print(e)

trades = pd.DataFrame
trades = pd.concat(data, axis = 0)
trades = trades.sort_values(columns='time', ascending=True)
trades.to_csv('data.csv')
