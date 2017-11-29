import matplotlib.pyplot as plt
from itertools import cycle


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
        if event.button != 1 or event.key is not None:
            print('key+button: {!r}+{!r}'.format(event.key, event.button))
            return

        # get the event location in data-space
        self.xdata.append(event.xdata)
        self.ydata.append(event.ydata)

        # update the artist data
        self.ln.set_data(self.xdata, self.ydata)

        # ask the GUI to re-draw the next time it can
        self.ln.figure.canvas.draw_idle()

    def on_key(self, event):
        # This is _super_ useful for debugging!
        # print(event.key)

        # if the key is c (any case)
        if event.key.lower() == 'c':
            # change the color
            self.ln.set_color(next(self.color_cyle))

            # ask the GUI to re-draw the next time it can
            self.ln.figure.canvas.draw_idle()


fig, ax = plt.subplots()
ln, = ax.plot([], [], '-o')
line_maker = LineMaker(ln)
plt.show()

# EXERCISE (15 minutes)

# - modify to remove the closest point when key == 'shift'
# - change the line width for [1-9]
# - clear the line when event.key == 'escape'
