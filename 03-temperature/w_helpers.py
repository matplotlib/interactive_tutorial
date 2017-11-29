import datetime
import pandas as pd
import os
from pathlib import Path


def aggregate_by_month(df, col='T'):
    """Given a data frame of hourly data, compute statistics by month

    Parameters
    ----------
    df : DataFrame
       Must have columns {'year', 'month'}

    col : str, optional
       The column to aggregate.  Defaults to 'T'

    Returns
    -------
    DataFrame
       Indexed on the 15th of the month,
       Has columns of `describe` + 'year' and 'month'
    """
    gb = df.groupby(('year', 'month'))[col].describe()
    new_index = [datetime.date(*m, *(15, )) for m in gb.index]
    gb.reset_index(inplace=True)
    gb.index = new_index
    return gb


def aggregate_by_day(df, col='T'):
    """Given a data frame of hourly data, compute statistics by day

    Parameters
    ----------
    df : DataFrame
       Must have columns {'year', 'month', 'day'}

    col : str, optional
       The column to aggregate.  Defaults to 'T'

    Returns
    -------
    DataFrame
       Indexed by day.
       Has columns of `describe` + 'year', 'month', and 'day'
    """

    gb = df.groupby(('year', 'month', 'day'))[col].describe()
    new_index = [datetime.date(*m) for m in gb.index]
    gb.reset_index(inplace=True)
    gb.index = new_index
    return gb


def extract_month_of_daily(daily, year, month):
    """Given daily values, extract a given month

    Parameters
    ----------
    daily : DataFrame
        must of columns {'year', 'month'}

    year, month : int
        The year and month of interest

    Returns
    -------

    DataFrame
         Indexed on days from start of month.  Same columns as input
    """
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


def load_data(dataset):
    """Load data from a given dataset

    Parameters
    ----------
    dataset : str
       Searches from dataset.h5 in this file's directory

    Returns
    -------
    DataFrame
       Hourly temperature data
    """
    p = Path(os.path.dirname(os.path.realpath(__file__))) / 'data'
    fname = p / f'{dataset}.h5'

    try:
        return pd.read_hdf(str(fname))
    except FileNotFoundError:
        sources = {f.stem for f in p.iterdir() if
                   f.is_file() and f.name.endswith('h5')}
        raise RuntimeError(f"Could not not find {dataset!r}.  Existing "
                           f"datasets are {sources}")
