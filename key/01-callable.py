from collections import deque
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
plt.ion()

# disable the built in key bindings
for k in ['keymap.all_axes',
          'keymap.back',
          'keymap.forward',
          'keymap.fullscreen',
          'keymap.grid',
          'keymap.home',
          'keymap.pan',
          'keymap.save',
          'keymap.xscale',
          'keymap.yscale',
          'keymap.zoom']:
    mpl.rcParams[k] = []


fig, ax = plt.subplots()

th = np.linspace(0, 2*np.pi, 64)
ln, = ax.plot(th, np.sin(th), 'o-', picker=5)


class FormatterCollector:
    def __init__(self, maxlen=15):
        self.event_deque = deque([], maxlen=maxlen)

    def __call__(self, event):
        print(f'called {event.name} at ')
        print(f' screen: ({event.x}, {event.y})')
        if event.inaxes:
            print(f'   data: ({event.xdata:.3g}, {event.ydata:.3g})')
        self.event_deque.append(event)

    def collect_string(self):
        return ''.join([ev.key for ev in self.event_deque
                        if ev.name == 'key_press_event'])


fc = FormatterCollector()
cids = {k: fig.canvas.mpl_connect(k, fc)
        for k in ('key_press_event', 'button_press_event')}
