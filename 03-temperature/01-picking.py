import matplotlib.pyplot as plt
from w_helpers import load_data, aggregate_by_day, extract_day_of_hourly, label_date

import uuid

datasource = 'mdw'

temperature = load_data(datasource)
temperature = temperature[temperature['year'] >= 2017]
temperature_daily = aggregate_by_day(temperature)


class RowPrinter:
    def __init__(self, ln, df, picker=10):
        ln.set_picker(picker)
        # we can use this to ID our line!
        self.uid = str(uuid.uuid4())
        ln.set_gid(self.uid)
        self.ln = ln
        self.df = df
        self.cid = None
        self.connect()

    def connect(self):
        self.remove()
        self.cid = ln.figure.canvas.mpl_connect('pick_event',
                                                self)

    def __call__(self, event):
        # ignore picks on not-our-artist
        if event.artist is not self.ln:
            return
        # for each hit index, print out the row
        for i in event.ind:
            print(self.df.iloc[i])

    def remove(self):
        if self.cid is not None:
            self.ln.figure.canvas.mpl_disconnect(self.cid)
            self.cid = None


fig, ax = plt.subplots()
ln, = ax.plot('mean', '-o', data=temperature_daily)
ax.set_xlabel('Date [UTC]')
ax.set_ylabel('Air Temperature [℃]')
ax.set_title(f'{datasource} temperature')

rp = RowPrinter(ln, temperature_daily)

one_day = extract_day_of_hourly(temperature, 2017, 10, 27)
plt.show()

# EXERCISE
# - make the print out nicer looking

# - open a new window with plot of day temperature
#   - fig, ax = plt.subplots()
#   - one_day = extract_day_of_hourly(temperature, 2015, 10, 18)
# - make picking add a label using the function `label_date` (which is
#   already imported from the `w_helpers` module)

# - use `get_gid` to filter artists instead of `is not`
