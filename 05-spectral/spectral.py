import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.widgets import SpanSelector
from matplotlib.colors import LogNorm
import numpy as np
import h5py


def plot_all_chan_spectrum(spectrum, bins, *, ax=None, **kwargs):

    def integrate_to_angles(spectrum, bins, lo, hi):
        lo_ind, hi_ind = bins.searchsorted([lo, hi])
        return spectrum[lo_ind:hi_ind].sum(axis=0)

    if ax is None:
        fig, ax = plt.subplots(figsize=(13.5, 9.5))
    else:
        fig = ax.figure

    div = make_axes_locatable(ax)
    ax_r = div.append_axes('right', 2, pad=0.1, sharey=ax)
    ax_t = div.append_axes('top', 2, pad=0.1, sharex=ax)

    ax_r.yaxis.tick_right()
    ax_r.yaxis.set_label_position("right")
    ax_t.xaxis.tick_top()
    ax_t.xaxis.set_label_position("top")

    im = ax.imshow(spectrum, origin='lower', aspect='auto',
                   extent=(-.5, 383.5,
                           bins[0], bins[-1]),
                   norm=LogNorm())

    e_line, = ax_r.plot(spectrum.sum(axis=1), bins[:-1] + np.diff(bins))
    p_line, = ax_t.plot(spectrum.sum(axis=0))
    label = ax_t.annotate('[0, 70] kEv', (0, 1), (10, -10),
                          xycoords='axes fraction',
                          textcoords='offset pixels',
                          va='top', ha='left')

    def update(lo, hi):
        p_data = integrate_to_angles(spectrum, bins, lo, hi)
        p_line.set_ydata(p_data)
        ax_t.relim()
        ax_t.autoscale(axis='y')

        label.set_text(f'[{lo:.1f}, {hi:.1f}] keV')
        fig.canvas.draw_idle()

    span = SpanSelector(ax_r, update, 'vertical', useblit=True,
                        rectprops={'alpha': .5, 'facecolor': 'red'},
                        span_stays=True)

    ax.set_xlabel('channel [#]')
    ax.set_ylabel('E [keV]')

    ax_t.set_xlabel('channel [#]')
    ax_t.set_ylabel('total counts')

    ax_r.set_ylabel('E [keV]')
    ax_r.set_xlabel('total counts')
    ax.set_xlim(-.5, 383.5)
    ax.set_ylim(bins[0], bins[-1])
    ax_r.set_xlim(xmin=0)

    return spectrum, bins, {'center': {'ax': ax, 'im': im},
                            'top': {'ax': ax_t, 'p_line': p_line},
                            'right': {'ax': ax_r, 'e_line': e_line,
                                      'span': span}}


with h5py.File('germ.h5', 'r') as fin:
    spectrum = fin['spectrum'][:]
    bins = fin['bins'][:]

ret = plot_all_chan_spectrum(spectrum, bins)
plt.show()


# Exercise (15 minutes)
# - add span selector to top axes to change curve in right axes
