#coding=utf-8

from collections import OrderedDict
import plot as plt
import csv
import numpy as np

size = 10 ** 7

def read_raw():
    content = csv.reader(open('../data/dns_ttl.csv', 'r'))
    raw = [0 for x in range(size)]  # 原始数据，数组中每个值代表其下标对应TTL值的数目
    overflow = [[0, 0]]  # TTL大于10^7的值单独存储
    data = [[0, 0]]  # 二维数组，第一项为TTL值，第二项为其数目

    for item in content:
        if item[0] != 'ttl':
            item_int = int(item[0])

            if item_int <= size - 1:
                raw[item_int] += 1
            else:
                overflow_np = np.array(overflow)[:, 0]
                if item_int not in overflow_np:
                    overflow.append([item_int, 1])
                else:
                    tup = np.where(overflow_np == item_int)
                    overflow[tup[0][0]][1] += 1

    overflow = overflow[1:]
    overflow.sort(key=lambda x: x[0])
    print "data loaded."

    for index in range(len(raw)):
        if raw[index] != 0:
            data.append([index, raw[index]])
    for item in overflow:
        data.append(item)

    data = data[1:]

    print "data transformed."

    return data


def read_csv():
    reader = csv.reader(open('../data/ttl_distribution.csv', 'r'))
    data = []

    for item in reader:
        if item[0] != 'TTL':
            data.append([int(item[0]), int(item[1])])

    print "reading finished."

    return data


def write_csv(data):
    writer = csv.writer(open('../data/ttl_distribution.csv', 'wb'))
    header = ['TTL', 'Amount']

    writer.writerow(header)
    for item in data:
        writer.writerow(item)

    print "writing finished."


def compare(x, y):
    tempx = x.split("-")
    tempy = y.split("-")

    if int(tempx[0]) > int(tempy[0]):
        return 1
    elif int(tempx[0]) < int(tempy[0]):
        return -1
    else:
        return 0


def separate(raw):
    data = OrderedDict()

    for i in range(0, 12):
        index = str(i * 300) + '-' + str((i + 1) * 300 - 1)
        data[index] = 0

        for item in raw:
            if item[0] >= i * 300 and item[0] < (i + 1) * 300:
                data[index] += item[1]

    for i in range(0, 12):
        index = str(3600 + i * 600) + '-' + str(3600 + (i + 1) * 600 - 1)
        data[index] = 0

        for item in raw:
            if item[0] >= 3600 + i * 600 and item[0] < 3600 + (i + 1) * 600:
                data[index] += item[1]

    for i in range(0, 40):
        index = str(14400 + i * 1800) + '-' + str(14400 + (i + 1) * 1800 - 1)
        data[index] = 0

        for item in raw:
            if item[0] >= 14400 + i * 1800 and item[0] < 14400 + (i + 1) * 1800:
                data[index] += item[1]

    for i in range(0, 24):
        index = str(86400 + i * 3600) + '-' + str(86400 + (i + 1) * 3600 - 1)
        data[index] = 0

        for item in raw:
            if item[0] >= 86400 + i * 3600 and item[0] < 86400 + (i + 1) * 3600:
                data[index] += item[1]

    for i in range(0, 8):
        index = str(172800 + i * 21600) + '-' + str(172800 + (i + 1) * 21600 - 1)
        data[index] = 0

        for item in raw:
            if item[0] >= 172800 + i * 21600 and item[0] < 172800 + (i + 1) * 21600:
                data[index] += item[1]

    data['345600-604799'] = 0
    for item in raw:
        if item[0] >= 345600 and item[0] < 604799:
            data['345600-604799'] += item[1]

    data['604800-1799999'] = 0
    for item in raw:
        if item[0] >= 604800 and item[0] < 1799999:
            data['604800-1799999'] += item[1]

    data['1800000-3599999'] = 0
    for item in raw:
        if item[0] >= 1800000 and item[0] < 3599999:
            data['1800000-3599999'] += item[1]

    data['3600000-10000000'] = 0
    for item in raw:
        if item[0] >= 3600000 and item[0] < 10000000:
            data['3600000-10000000'] += item[1]

    data['10000000-'] = 0
    for item in raw:
        if item[0] >= 10000000:
            data['10000000-'] += item[1]

    return data


if __name__ == '__main__':
    read_raw('dns_ttl.csv')
    data = read_csv('ttl_distribution.csv')
    sp = separate(data)
    write_csv(data, 'ttl_distribution.csv')
    plt.plot(data)
    plt.plot_scatter(data)
    plt.plot_bar(sp)