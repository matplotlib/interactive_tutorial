import matplotlib.pyplot as plt
from w_helpers import load_bwi_data, aggregate_by_month
plt.ion()

bwi = load_bwi_data()
bwi_monthly = aggregate_by_month(bwi)

fig, ax = plt.subplots()

def plot_aggregated_errorbar(ax, gb, label, picker=None, *,
                             bands=None,
                             center_line='mean',
                             **kwargs):
    if bands is None:
        bands = ['min', 'max']
    kwargs.setdefault('capsize', 3)
    kwargs.setdefault('markersize', 5)
    kwargs.setdefault('marker', 'o')
    eb = ax.errorbar(gb.index, center_line,
                     yerr='std',
                     data=gb,
                     label=label,
                     picker=picker,
                     **kwargs)
    fill = ax.fill_between(gb.index, *bands, alpha=.5,
                           data=gb, color=eb[0].get_color())
    ax.legend()
    ax.figure.canvas.draw_idle()
    return eb, fill

arts = plot_aggregated_errorbar(ax, bwi_monthly, 'bwi',
                                bands=['25%', '75%'],
                                center_line='50%')
