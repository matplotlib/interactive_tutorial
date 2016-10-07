from urllib.request import urlopen
import gzip

import os
import os.path
import datetime

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import cartopy
import cartopy.crs
import cartopy.feature as cfeature

plt.ion()

def get_filtered_isd(data_dir, s_date=None, f_date=None,
                     allow_download=True):
    fname = 'isd-history.csv'
    target_file = os.path.join(data_dir, fname)

    if not os.path.exists(target_file) and allow_download:
        url_target = 'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-history.csv'
        with open(target_file, 'wb') as fout:
            print(url_target)
            fout.write(urlopen(url_target).read())

    isd_history = pd.read_csv(target_file)
    if s_date is not None:
        isd_history = isd_history[isd_history['BEGIN'] < s_date]
    if f_date is not None:
        isd_history = isd_history[isd_history['END'] > f_date]

    return isd_history


def extract_date_time(row):
    '''
    '''
    fmt_str = '%Y%m%d%H%M'
    dt = datetime.datetime.strptime(row[15:27], fmt_str)
    return dt, dt.year, dt.month, dt.day, dt.hour


def extract_temperature(row):
    t = int(row[87:92])
    if t == 9999:
        return (np.nan, )
    return (t / 10,)


def injest_file(fname):
    with gzip.open(fname, 'rt', encoding='ascii') as f:
        data = [extract_date_time(ln) + extract_temperature(ln)
                for ln in f]

    return pd.DataFrame(data,
                        columns=('datetime', 'year', 'month',
                                 'day', 'hour', 'T')).dropna()


def get_hourly_data(data_dir, template, years, allow_download=True,
                    urlbase='ftp://ftp.ncdc.noaa.gov/pub/data/noaa/{year}'):

    data_dir_template = os.path.join(data_dir, '{year}')
    target_template = os.path.join(data_dir_template, template)
    url_template = '/'.join((urlbase, template))
    data = []

    for year in years:
        os.makedirs(data_dir_template.format(year=year), exist_ok=True)

        target_file = target_template.format(year=year)

        if not os.path.exists(target_file) and allow_download:
            url_target = url_template.format(year=year)
            with open(target_file, 'wb') as fout:
                print(url_target)
                fout.write(urlopen(url_target).read())

        data.append(injest_file(target_file))
    data = pd.concat(data)
    data.set_index('datetime', inplace=True)
    return data


class StationPicker:
    def __init__(self, station_artist, data, data_path=None):
        if data_path is None:
            data_path = os.path.expanduser('~/data_cache')
        self.data_path = data_path
        self.event = None
        self.data = data
        self.station_artist = station_artist
        self.cid = station_artist.figure.canvas.mpl_connect('pick_event',
                                                            self._id_station)
        self.station_templates = {}
        self.station_rows = {}

    def _id_station(self, event):
        print('HIT')
        if event.artist is not self.station_artist:
            return True

        N = len(event.ind)
        if not N:
            return True
        for i in event.ind:
            row = self.data.iloc[i]
            label = row['STATION NAME']
            tmplate = '{USAF:05d}-{WBAN:05d}-{{year}}.gz'.format(**row)
            self.station_rows[label] = row
            self.station_templates[label] = tmplate
            print('{!r}: {!r}'.format(label, tmplate))

    def remove(self):
        self.station_artist.figure.canvas.mpl_disconnect(self.cid)
        self.cid = None

    def get_station_data(self, station_name, years):
        '''Get data from NOAA

        Parameters
        ----------
        station_name : str
            This has to be the name of a station you have clicked on
            (see sp.station_templates.keys())
        years : list
           List of years to get data for

        Returns
        -------
        DataFrame
            Only extracts the temperature, year, month, day, and hour
        '''
        return get_hourly_data(self.data_path,
                               self.station_templates[station_name],
                               years)


def plot_station_locations(fig, fih, pick_radius=10):
    fig.clf()
    fig.add_subplot(1, 1, 1, projection=cartopy.crs.PlateCarree())

    countries = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_0_countries',
            scale='50m',
            facecolor='none',
            edgecolor='gray')

    states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none',
            edgecolor='gray')

    land = cfeature.NaturalEarthFeature(
            category='physical',
            name='land',
            scale='50m',
            facecolor=cfeature.COLORS['land'])

    lakes = cfeature.NaturalEarthFeature(
        category='physical',
        name='lakes',
        scale='50m',
        facecolor=cfeature.COLORS['water'])

    ax = plt.axes(projection=cartopy.crs.PlateCarree())
    ax.set_xlim(-80.5, -71)
    ax.set_ylim(36, 45)

    ax.add_feature(land)
    ax.add_feature(lakes)
    ax.add_feature(states_provinces, edgecolor='gray')
    ax.add_feature(countries, edgecolor='gray')
    art, = ax.plot('LON', 'LAT', 'o', data=fih, ms=5, picker=10)

    sp = StationPicker(art, fih)

    return ax, art, sp


data_path = os.path.expanduser('~/data_cache')
fih = get_filtered_isd(data_path)
fig = plt.figure()
ax, art, sp = plot_station_locations(fig, fih)
