import matplotlib.pyplot as plt
from w_helpers import load_ornl_data, aggregate_by_day, extract_day_of_hourly

import uuid


ornl = load_ornl_data()
ornl = ornl[ornl['year'] >= 2016]
ornl_daily = aggregate_by_day(ornl)


class RowPrinter:
    def __init__(self, ln, df, picker=10):
        ln.set_picker(picker)
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
ln, = ax.plot('mean', '-o', data=ornl_daily)
ax.set_xlabel('Date [UTC]')
ax.set_ylabel('Air Temperature [℃]')
ax.set_title('ORNL')
rp = RowPrinter(ln, ornl_daily)

one_day = extract_day_of_hourly(ornl, 2015, 10, 18)
plt.show()

# EXERCISE
# - make the print out nicer looking

# - open a new window with plot of day temperature
#   - fig, ax = plt.subplots()
#   - one_day = extract_day_of_hourly(bwi, 2015, 10, 18)


# - make picking add a label with `label_data`
# - use `get_gid` to filter instead of `is not`
