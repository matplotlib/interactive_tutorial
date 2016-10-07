import matplotlib.pyplot as plt
import numpy as np
plt.ion()

ev = None


def event_printer(event):
    """Helper function for exploring events.

    Prints all public attributes +
    """
    global ev
    ev = event
    for k, v in sorted(vars(event).items()):
        print('{k}: {v!r}'.format(k=k, v=v))
    print('-'*25)

th = np.linspace(0, 2*np.pi, 64)
fig, ax = plt.subplots()
ax.plot(th, np.sin(th), 'o-', picker=5)

cid = fig.canvas.mpl_connect('button_press_event', event_printer)
# fig.canvas.mpl_disconnect(cid)


# EXERCISE
# - Try all 'active' events
#   ['button_press_event', 'button_release_event', 'scroll_event',
#    'key_press_event', 'key_release_event', 'pick_event']
# - tweak the print line
# - remove a callback
# - add more than one callback to the canvas
