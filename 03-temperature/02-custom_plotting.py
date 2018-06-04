import matplotlib.pyplot as plt
from w_helpers import load_data, aggregate_by_month
plt.ion()

temperature = load_data('mdw')
temperature_monthly = aggregate_by_month(temperature)

fig, ax = plt.subplots()


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


arts = plot_aggregated_errorbar(ax, temperature_monthly, 'temperature')

# EXERCISE (10 minutes)

# - make the shaded area configurable
# - make center line configurable
