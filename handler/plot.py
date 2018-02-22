#coding=utf-8

import matplotlib.pyplot as plt
import numpy as np

def plot(data):
    datax = range(len(data))
    datax[0] = 0.2

    plt.gcf().set_size_inches(20, 14)
    plt.title("TTL Distribution Analysis")
    plt.xlabel("TTL /s")
    plt.ylabel("Amount")
    plt.xscale('log')
    plt.yscale('log')

    plt.plot(datax, np.array(data)[:, 1])

    print("plot ended.")

    plt.show()


def plot_scatter(data):
    datax =  list(np.array(data)[:, 0])
    datax[0] = 0.2

    plt.figure(figsize=(40, 15), dpi=70)
    plt.title("TTL Distribution Analysis")
    plt.xlabel("TTL /s")
    plt.ylabel("Amount")
    plt.xscale('log')
    plt.yscale('log')

    plt.scatter(datax, np.array(data)[:, 1], s=5)

    print("plot ended.")

    plt.show()


def plot_bar(data):
    plt.figure(figsize=(40, 14), dpi=70)
    plt.title("TTL Distribution Analysis")
    plt.xlabel("TTL /s")
    plt.ylabel("Amount")
    plt.yscale('log')

    ax = plt.gca()
    ax.set_xticks(np.arange(0, 101, 1))
    xtick = []

    for index in range(len(data.keys())):
        if index % 3 == 0:
            xtick.append(list(data.keys())[index].split("-")[0])
        else:
            xtick.append('')

    ax.set_xticklabels(xtick)

    plt.plot(data.values())

    plt.show()


def plot_pie(data):
    plt.figure(figsize=(6, 6))
    plt.title("DGA domain percentage")

    labels = ["Non-DGA", "DGA"]
    explode = [0, 0.1]
    plt.axes(aspect=1)
    plt.pie(x=data, labels=labels, explode=explode, autopct = '%3.1f%%', labeldistance=1.1, startangle = 90, pctdistance = 0.6)

    plt.legend()
    plt.show()