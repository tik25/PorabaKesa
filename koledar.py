import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def generate_data(datelist, df, N):
    datumiPorabe = {}
    for i in range(N):
        if df["Cena"][i] > 0:
            trenutni = df["Datum"][i]
            dan, mesc, leto = trenutni.split(".")
            if int(dan) < 10:
                dan = "0{}".format(dan)
            if int(mesc) < 10:
                mesc = "0{}".format(mesc)
            datum = "{}-{}-{}".format(leto, mesc, dan)
            if datum in datumiPorabe.keys():
                datumiPorabe[datum] += df["Cena"][i]
            else:
                datumiPorabe[datum] = df["Cena"][i]

    data = []
    for datum in datelist:
        datum = str(datum)[:10]
        if datum not in datumiPorabe.keys():
            data.append(0)
        else:
            data.append(float(datumiPorabe[datum]))
    return data


def calendar_array(dates, data):
    i, j = zip(*[d.isocalendar()[1:] for d in dates])
    i = np.array(i) - min(i)
    j = np.array(j) - 1
    ni = max(i) + 1

    calendar = np.nan * np.zeros((ni, 7))
    calendar[i, j] = data
    return i, j, calendar


def calendar_heatmap(ax, dates, data):
    # fix colorbar
    interval = np.linspace(0.45, 1)
    colors = plt.cm.seismic(interval)
    cmap = LinearSegmentedColormap.from_list('name', colors)
    #

    i, j, calendar = calendar_array(dates, data)
    im = ax.imshow(calendar, interpolation='none', cmap=cmap)
    label_days(ax, dates, i, j, calendar)
    label_months(ax, dates, i, j, calendar)
    ax.figure.colorbar(im)


def label_days(ax, dates, i, j, calendar):
    ni, nj = calendar.shape
    day_of_month = np.nan * np.zeros((ni, 7))
    day_of_month[i, j] = [d.day for d in dates]

    for (i, j), day in np.ndenumerate(day_of_month):
        if np.isfinite(day):
            ax.text(j, i, int(day), ha='center', va='center')

    ax.set(xticks=np.arange(7),
           xticklabels=['M', 'T', 'W', 'R', 'F', 'S', 'S'])
    ax.xaxis.tick_top()


def label_months(ax, dates, i, j, calendar):
    month_labels = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                             'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    months = np.array([d.month for d in dates])
    uniq_months = sorted(set(months))
    yticks = [i[months == m].mean() for m in uniq_months]
    labels = [month_labels[m - 1] for m in uniq_months]
    ax.set(yticks=yticks)
    ax.set_yticklabels(labels, rotation=90)
