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
    def __init__(self, maxlen=12):
        self.event_deque = deque([], maxlen=maxlen)

    def __call__(self, event):
        print('called {} at ({}, {})'.format(event.name,
                                             event.xdata,
                                             event.ydata))
        self.event_deque.append(event)

    def collect_string(self):
        return ''.join([ev.key for ev in self.event_deque
                        if ev.name == 'key_press_event'])

fc = FormatterCollector()
cid = fig.canvas.mpl_connect('key_press_event', fc)
cid2 = fig.canvas.mpl_connect('key_release_event', fc)
cid2 = fig.canvas.mpl_connect('button_press_event', fc)
