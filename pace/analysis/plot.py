"""
Look at this graph
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn

seaborn.set()


def congestion(telemetry: pd.DataFrame):
    """
    Plot congestion over time
    :param telemetry: Processed Simple DataFrame
    :return: matplotlib.figure
    """
    figure = plt.figure(figsize=(20, 10))
    ax = figure.add_subplot(111)
    ax.set_title("Area Congestion")
    ax.set_xlabel("Time")
    ax.set_ylabel("Congestion")
    im = ax.plot(telemetry['Congestion'])
    return figure


def polyfit_congestion(telemetry: pd.DataFrame, poly_degree=8):
    """
    Plot polynomial fit congestion over time
    :param poly_degree: Degree of polynomial fit
    :param telemetry: Processed Simple DataFrame
    :return: matplotlib.figure
    """
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.set_title("Area Congestion")
    ax.set_xlabel("Time")
    ax.set_ylabel("Congestion")

    conv_times = mdates.date2num(telemetry.index.to_list())

    y_values = telemetry['Congestion']
    x_values = np.linspace(0, 1, len(telemetry.loc[:, "Congestion"]))

    coeffs = np.polyfit(x_values, y_values, poly_degree)
    poly_eqn = np.poly1d(coeffs)
    y_hat = poly_eqn(x_values)

    im = ax.plot(telemetry.index, y_hat)
    return figure


def eval_model(times, congestion, model):
    """
    Plot the model vs the data
    :param times:
    :param congestion:
    :param model:
    :return:
    """
    import matplotlib.pyplot as plt
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.set_title("Model Prediction vs Data")
    ax.set_xlabel("24-Hour Time")
    ax.set_ylabel("Congestion")

    ticks = range(0, 1441, 120)
    ax.set_xticks(ticks)

    dic = {0: '00',
           60 * 1: '01',
           60 * 2: '02',
           60 * 3: '03',
           60 * 4: '04',
           60 * 5: '05',
           60 * 6: '06',
           60 * 7: '07',
           60 * 8: '08',
           60 * 9: '09',
           60 * 10: '10',
           60 * 11: '11',
           60 * 12: '12',
           60 * 13: '13',
           60 * 14: '14',
           60 * 15: '15',
           60 * 16: '16',
           60 * 17: '17',
           60 * 18: '18',
           60 * 19: '19',
           60 * 20: '20',
           60 * 21: '21',
           60 * 22: '22',
           60 * 23: '23',
           60 * 24: '00',
           }
    labels = [ticks[i] if t not in dic.keys() else dic[t] for i, t in enumerate(ticks)]

    ax.set_xticklabels(labels)

    x = times[:, 0]
    y = congestion.to_numpy()

    ax.scatter(x, y, label="Actual")

    predictions = model.predict(np.arange(0, 1440).reshape(-1, 1))

    ax.scatter(np.arange(1440), predictions, label="Prediction")

    ax.legend()
    return figure


def devices_per_probes(telemetry: pd.DataFrame):
    """
    plot number of devices per number of probes
    :param telemetry: Processed Simple DataFrame
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("Devices Per Request")
    ax.set_xlabel("Number of Devices")
    ax.set_ylabel("Number of Requests")
    mi = ax.plot(telemetry['Devices'] / telemetry['Total Probes'])
    return figure


def devices_per_interval(telemetry: pd.DataFrame):
    """
    plot number of devices per each interval
    :param telemetry: Processed Simple Dataframe
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("Devices per Interval")
    ax.set_xlabel("Time")
    ax.set_ylabel("Number of Devices")
    mi = ax.plot(telemetry['Number Devices'] / telemetry['Interval'])
    return figure


def probes_per_time_vs_devices_per_interval(telemetry: pd.DataFrame):
    """
    plot number of probes per time versus number of devices per time interval
    :param telemetry: Processed Simple DataFrame
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("Requests per Time over Devices per Interval")
    ax.set_xlabel("Devices per Interval")
    ax.set_ylabel("Requests per Time")
    probes_per_time = telemetry['Total Probes'] / telemetry['Interval']
    requests_per_interval = telemetry['Number SSID Requests']/telemetry['Interval']
    mi = ax.plot(probes_per_time/requests_per_interval)
    return figure


def SSID_freq(telemetry: pd.DataFrame):
    """
    plot frequency of the request of each SSID
    :param telemetry: Processed Simple DataFrame
    :return: mathplotlib.figure
    """
    figure = plt.figure(figsize=(20, 4))
    ax = figure.add_subplot(111)
    ax.set_title("SSID Frequency")
    ax.set_xlabel("SSID")
    ax.set_ylabel("number of requests")
    mi = ax.plot(telemetry['SSID Requests']/telemetry['Number SSID Requests'])
    return figure


def SSID_plot(telemetry: pd.DataFrame):
    """
    Creates a bar graph of total the SSID's
    :param telemetry:
    :return: matplotlib.figure
    """
    import collections
    dic0 = telemetry['SSID Requests']
    dicts = dic0.values
    c = {}
    for d in dicts:
        for i in d.keys():
            if i in c.keys():
                c[i] += d[i]
            else:
                c[i] = d[i]
    import operator
    c = sorted(c.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = collections.OrderedDict(c)

    figure = plt.figure(figsize=(16, 9))
    ax = figure.add_subplot(111)
    tick_labels1 = list(sorted_dict.keys())[:20:2][::-1]
    tick_labels2 = list(sorted_dict.keys())[1:20:2]
    tick_labels = tick_labels1 + tick_labels2
    bar_values1 = list(sorted_dict.values())[:20:2][::-1]
    bar_values2 = list(sorted_dict.values())[1:20:2]
    bar_values = bar_values1 + bar_values2

    count = 0
    for i in tick_labels:
        if len(i) > 15:
            tick_labels[count] = i[:15] + '...'
        count += 1

    plt.xticks(rotation='vertical')
    ax.bar(range(20), bar_values, align='center', tick_label=tick_labels)

    ax.set_title("SSID Request Frequency")
    ax.set_xlabel("SSID")
    ax.set_ylabel("Number of Requests")
    return figure
