import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np
plt.ion()


class LineMaker:
    def __init__(self, ln):
        # stash the current data
        self.xdata = list(ln.get_xdata())
        self.ydata = list(ln.get_ydata())
        # stash the Line2D artist
        self.ln = ln
        self.color_cyle = cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                                 '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                                 '#bcbd22', '#17becf'])
        self.button_cid = ln.figure.canvas.mpl_connect('button_press_event',
                                                       self.on_button)
        self.key_cid = ln.figure.canvas.mpl_connect('key_press_event',
                                                    self.on_key)

    def on_button(self, event):
        # only consider events from the lines Axes
        if event.inaxes is not self.ln.axes:
            return

        # if not the left mouse button or a modifier key
        # is held down, bail
        if event.button != 1 or event.key not in (None, 'shift'):
            print('key+button: {!r}+{!r}'.format(event.key, event.button))
            return

        if event.key == 'shift':
            # compute the distance to each point *in data space*
            d = np.hypot(np.asarray(self.xdata) - event.xdata,
                         np.asarray(self.ydata) - event.ydata)
            # find the closest point
            ix = np.argmin(d)
            # remove that data point
            del self.xdata[ix]
            del self.ydata[ix]
        else:
            # get the event location in data-space
            # and add to internal data list
            self.xdata.append(event.xdata)
            self.ydata.append(event.ydata)
        # update the line
        self._update_line()

    def _update_line(self):
        # update the artist data
        self.ln.set_data(self.xdata, self.ydata)
        # ask the GUI to re-draw the next time it can
        self.ln.figure.canvas.draw_idle()

    def on_key(self, event):
        # This is _super_ useful for debugging!
        # print(event.key)

        # if the escape key is hit, clear the data
        if event.key == 'escape':
            # clear the internal data structures
            self.xdata.clear()
            self.ydata.clear()
            # update the internal line
            self._update_line()

        # if the key is c (any case)
        if event.key.lower() == 'c':
            # change the color
            self.ln.set_color(next(self.color_cyle))

            # ask the GUI to re-draw the next time it can
            self.ln.figure.canvas.draw_idle()

fig, ax = plt.subplots()
ln, = ax.plot([], [], '-o')
line_maker = LineMaker(ln)
