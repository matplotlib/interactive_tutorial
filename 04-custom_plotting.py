import matplotlib.pyplot as plt
from pddc_helpers import load_bwi_data, aggregate_by_month
plt.ion()


def plot_aggregated_errorbar(ax, gb, label, picker=None, **kwargs):
    kwargs.setdefault('capsize', 3)
    kwargs.setdefault('markersize', 5)
    kwargs.setdefault('marker', 'o')
    eb = ax.errorbar(gb.index, 'mean',
                     yerr='std',
                     data=gb,
                     label=label,
                     picker=picker,
                     **kwargs)
    fill = ax.fill_between(gb.index, 'min', 'max', alpha=.5,
                           data=gb, color=eb[0].get_color())
    ax.legend()
    ax.figure.canvas.draw_idle()
    return eb, fill

bwi = load_bwi_data()
bwi_monthly = aggregate_by_month(bwi)

fig, ax = plt.subplots()
ax.set_xlabel('Date [UTC]')
ax.set_ylabel('Air Temperature [℃]')
ax.set_title('BWI')

arts = plot_aggregated_errorbar(ax, bwi_monthly, 'bwi')
