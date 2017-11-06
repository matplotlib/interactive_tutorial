# This may be required if you are on a Mac and default to using OSX as
# your backend
# import matplotlib
# matplotlib.use('qt5agg')

import matplotlib.pyplot as plt
import numpy as np


last_ev = None


def event_printer(event):
    """Helper function for exploring events.

    Prints all public attributes +
    """
    # capture the last event
    global last_ev
    last_ev = event
    if hasattr(event, 'inaxes') and event.inaxes is not None:
        print(f'{event.name} ({event.xdata:.3f}, {event.ydata:.3f})')
    else:
        print(f'{event.name}')


th = np.linspace(0, 2*np.pi, 64)
fig, ax = plt.subplots()
ax.plot(th, np.sin(th), 'o-', picker=5)

cids = {k: fig.canvas.mpl_connect(k, event_printer)
        for k in ('button_press_event', 'button_release_event',
                  'scroll_event',
                  'key_press_event', 'key_release_event',
                  'pick_event')}


plt.show()
