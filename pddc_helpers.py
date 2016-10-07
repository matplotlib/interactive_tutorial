from urllib.request import urlopen
import datetime
import numpy as np
import pandas as pd
import gzip
import os

def aggregate_by_month(df, col='T'):
    gb = df.groupby(('year', 'month'))['T'].describe().unstack()
    new_index = [datetime.date(*m, *(15, )) for m in gb.index]
    gb.reset_index(inplace=True)
    gb.index = new_index
    return gb


def aggregate_by_day(df, col='T'):
    gb = df.groupby(('year', 'month', 'day'))['T'].describe().unstack()
    new_index = [datetime.date(*m) for m in gb.index]
    gb.reset_index(inplace=True)
    gb.index = new_index
    return gb


def extract_month_of_daily(daily, year, month):
    ix = (daily['month'] == month) & (daily['year'] == year)
    df = daily[ix]
    idx = [(m - df.index[0]).days for m in df.index]
    df.reset_index(inplace=True)
    df.index = idx
    return df


def extract_day_of_hourly(hourly_df, year, month, day):
    """Given a data frame with hourly data, extract data for year-month-day

    Parameters
    ----------
    hourly_df : DataFrame
      Must have columns 'year', 'month', 'day' with the expected semantics and
      a time index

    year, month, day : int
        The day to extract the data for
    """

    ix = ((hourly_df['month'] == month) &
          (hourly_df['year'] == year) &
          (hourly_df['day'] == day))
    df = hourly_df[ix]
    midnight = datetime.datetime(year, month, day, 0, 0)
    df.index = [(m - midnight).seconds / 3600 for m in df.index]
    return df


def load_bwi_data():
    fname = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'bwi.h5')
    return pd.read_hdf(fname)


def label_date(ax, label, date, df):
    '''Helper function to annotate a date

    ``date`` is assumed to be in the index of ``df``

    Parameters
    ----------
    ax : Axes
       The axes to draw to

    label : str
        The text of the label

    date : object in index of df
        The x coordinate

    df : DataFrame
        The data source

    '''
    y = df.loc[date]['mean']
    return ax.annotate(label, (date, y),
                       ha='right',
                       xytext=(-10, -30),
                       textcoords='offset points',
                       arrowprops={'arrowstyle': '->'})
