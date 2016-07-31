#!local/bin/python

"""
@author  :  Rajan Khullar
@created :  07/29/16
@updated :  07/31/16
"""

import csv
import urllib2
import inspect
import requests
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.dates import strpdate2num, DateFormatter

def yahoo_stock_quote(symbol):
    url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1c1hgv' % symbol
    f = urllib2.urlopen(url)
    s = f.read().strip().split(',')
    f.close()
    d = {}
    d['symbol']  = s[0].replace('"','')
    d['last']    = float(s[1])
    d['date']    = s[2].replace('"','')
    d['change']  = float(s[3])
    d['high']    = float(s[4])
    d['low']     = float(s[5])
    d['vol']     = int(s[6])
    return d

def stock_history(symbol, i=None, f=None, fmt='%Y-%m-%d'):
    url = 'http://ichart.finance.yahoo.com/table.csv'
    date2num = strpdate2num(fmt)
    num2 = {'Y':DateFormatter('%Y'),'m':DateFormatter('%m'),'d':DateFormatter('%d')}

    payload = {}
    payload['s'] = symbol

    if i:
        x = date2num(i)
        payload['a'] = num2['m'](x)
        payload['b'] = num2['d'](x)
        payload['c'] = num2['Y'](x)

        if not f:
            t = dt.datetime.today()
            payload['d'] = str(t.month)
            payload['e'] = str(t.day)
            payload['f'] = str(t.year)
        else:
            x = date2num(f)
            payload['d'] = num2['m'](x)
            payload['e'] = num2['d'](x)
            payload['f'] = num2['Y'](x)

    r = requests.get(url, params=payload)
    f = urllib2.urlopen(r.url)
    s = f.read().strip().split('\n')
    f.close()

    for row in s:
        print row

if __name__ == '__main__':
    #print yahoo_stock_quote('GOOG')
    stock_history('AAPL', '2000-01-01')
