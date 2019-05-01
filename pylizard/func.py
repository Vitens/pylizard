import datetime

import numpy
import pandas
import pyproj
import requests


def pnt2buis(x, y, dist, report=False, url_lizard='https://vitens.lizard.net/api/v3/', proxydict={}):
    p_rd = pyproj.Proj(init='epsg:28992')
    p_wgs = pyproj.Proj(proj='latlong', datum='WGS84')

    lon, lat = pyproj.transform(p_rd, p_wgs, x, y)
    lizard_url_stn = url_lizard+'groundwaterstations/'

    meta = []
    idx = []
    nxt_url = '{}?dist={}&point={},{}'.format(lizard_url_stn, dist, lon, lat)
    while nxt_url != None:
        if report:
            print('GET', nxt_url)
        data = requests.get(nxt_url, proxies=proxydict).json()
        results = data['results']
        nxt_url = data['next']

        for p in results:
            buis = p['code']
            coor = p['geometry']['coordinates']
            lon, lat = coor[:2]
            surface_level = p['surface_level']
            x, y = pyproj.transform(p_wgs, p_rd, lon, lat)
            for f in p['filters']:
                i = f['code']
                filt = int(i[-3:])
                bkf = f['filter_top_level']
                okf = f['filter_bottom_level']
                uuid_hand = ''
                uuid_diver = ''
                if f['timeseries'] != []:
                    for t in f['timeseries']:
                        if t['parameter'] == 'Handpeiling':
                            uuid_hand = t['uuid']
                        elif t['parameter'] == 'Stijghoogte':
                            uuid_diver = t['uuid']
                meta.append([buis, filt, x, y, lat, lon,
                             surface_level, bkf, okf, uuid_hand, uuid_diver])
                idx.append(i)
    df = pandas.DataFrame(meta,
                          columns=['buis', 'filt', 'x', 'y', 'lat', 'lon',
                                   'surface_level', 'bkf', 'okf', 'uuid_hand', 'uuid_diver'],
                          index=idx)
    df['bkf'] = df['surface_level']-df['bkf']
    df['okf'] = df['surface_level']-df['okf']
    return df


def get_timeseries(uuid, tmin=None, tmax=None, report=False, url_lizard='https://vitens.lizard.net/api/v3/', proxydict={}):
    lizard_url_ts = url_lizard+'timeseries/'
    url = lizard_url_ts + uuid
    if report:
        print('GET', url)

    ts = requests.get(url, proxies=proxydict).json()

    ts_tmin = datetime.datetime.fromtimestamp(
        numpy.sign(ts['start'])*ts['start']/1000-2*3600)
    ts_tmax = datetime.datetime.fromtimestamp(
        numpy.sign(ts['end'])*ts['end']/1000+2*3600)

    if (tmin is None) or (tmax is None):
        ts = ts_tmin.isoformat('T') + 'Z'
        te = ts_tmax.isoformat('T') + 'Z'
    else:
        ts = ts.isoformat('T') + 'Z'
        te = te.isoformat('T') + 'Z'

    url = '{}{}/data/?start={}&end={}'.format(lizard_url_ts, uuid, ts, te)
    if report:
        print('GET', url)
    data = requests.get(url, proxies=proxydict).json()
    df = pandas.DataFrame(data)

    df['datetime'] = pandas.to_datetime(1e6*df.timestamp)
    df.set_index('datetime', inplace=True)
    df['head'] = df[['max', 'min']].mean(axis=1)
    df = df.loc[:, 'head']

    return df
