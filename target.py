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

def stock_history(symbol, i=None, f=None, fmt='%Y-%m-%d', ival=None):
    url = 'https://ichart.finance.yahoo.com/table.csv'
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

    date2num = strpdate2num('%Y-%m-%d')
    data = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[], 'volume':[], 'adj-close':[]}
    def add_data(k,v):
        data[k].append(v)

    for row in s[1:]:
        t = row.split(',')
        add_data('date',date2num(t[0]))
        add_data('open',float(t[1]))
        add_data('high',float(t[2]))
        add_data('low',float(t[3]))
        add_data('close',float(t[4]))
        add_data('volume',float(t[5]))
        add_data('adj-close',float(t[6]))

    date = np.array(data['date'])
    close = np.array(data['close'])

    if not ival:
        ival = close[-1]

    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1),(0,0))

    ax1.plot_date(date,close,'-')
    ax1.fill_between(date, close, ival, where=close>ival, facecolor='g', alpha=0.5)
    ax1.fill_between(date, close, ival, where=close<ival, facecolor='r', alpha=0.5)
    ax1.plot([],[], label='gain',color='g',linewidth=5, alpha=0.5)
    ax1.plot([],[], label='loss',color='r',linewidth=5, alpha=0.5)

    ax1.set_title(symbol.upper())
    ax1.set_axis_bgcolor('k')
    ax1.grid(True, color='w', linestyle='-')
    ax1.legend()

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.xaxis.label.set_color('c')
    ax1.yaxis.label.set_color('r')

    plt.xlabel('date')
    plt.ylabel('price')
    plt.subplots_adjust(bottom=0.20)
    plt.show()

if __name__ == '__main__':
    #print yahoo_stock_quote('GOOG')
    stock_history('ebay', '2015-01-01', ival=25)
