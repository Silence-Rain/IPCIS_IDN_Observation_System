#coding=utf-8

import csv
import numpy as np


def read_csv(handler):
    data = []
    if handler == 'domain':
        reader = csv.reader(open('../data/dns_domain_dga_ttl.csv', 'r'))
        for item in reader:
            data.append([item[0], int(item[1]), int(item[2])])
    elif handler == 'whois':
        reader = csv.reader(open('../data/domain_whois_utf8.csv', 'r'))
        for item in reader:
            data.append([item[0], item[1]])
    elif handler == 'ttl':
        reader = csv.reader(open('../data/ttl_distribution.csv', 'r'))
        for item in reader:
            data.append([int(item[0]), int(item[1])])

    print "reading " + handler + " finished."
    return data


def write_csv(data, url):
    writer = csv.writer(open(url, 'wb'))

    for item in data:
        writer.writerow(item)

    print "writing finished."


def peakAnalyse(peakIndex):
    peakNum = [0 for x in range(len(peakIndex))]
    data = read_csv('ttl')

    for i in range(0, len(peakIndex)):
        for item in data:
            if item[0] > peakIndex[i] - 10 and item[0] < peakIndex[i] + 10:
                peakNum[i] += item[1]

    ret = []
    for i in range(0, len(peakIndex)):
        ret.append([peakIndex[i], peakNum[i]])

    write_csv(ret, '../data/peak_analysis.csv')


def findPeak():
    raw = read_csv('ttl')
    ret = []

    for item in raw:
        if item[1] >= 10000 and item[0] % 10 == 0:
            ret.append(item[0])

    return ret


def find_2Big2Small():
    whois = read_csv('whois')
    domain = read_csv('domain')
    domainTooSmall = []
    domainTooBig = []
    resTooSmall = []
    resTooBig = []

    for item in domain:
        # if item[2] > 172800:
        #     domainTooBig.append(item)
        if item[2] <= 1800 and item[2] != 0:
            domainTooSmall.append(item)
    print "data filtered."

    # for item in domainTooBig:
    #     for i in whois:
    #         if i[0] == item[0]:
    #             resTooBig.append(i)
    # write_csv(resTooBig, 'data\\res_tooBig.csv')
    #
    domainInWhois = list(np.array(whois)[:, 0])
    for item in domainTooSmall:
        if item[0] in domainInWhois:
            resTooSmall.append(whois[domainInWhois.index(item[0])])
    print "search completed."
    write_csv(resTooSmall, '../data/res_tooSmall.csv')


def categorizeByDay():
    ttl = read_csv('ttl')
    ret = [0 for x in range(0, 32)]
    index = []

    for i in range(0, 32):
        str1 = ""
        if i == 31:
            str1 = ">" + str(i)
        else:
            str1 = str(i) + "~" + str(i + 1)
        index.append(str1)

    for item in ttl:
        for i in range(0, 32):
            if i == 31:
                if item[0] >= 86400 * i:
                    ret[i] += item[1]
            elif item[0] >= 86400 * i and item[0] < 86400 * (i + 1):
                ret[i] += item[1]
    print "data categorized."
    ret = np.dstack((index, ret))[0]

    write_csv(ret, "../data/categorized_Day.csv")


def small_dgaMatch():
    data = read_csv('domain')
    countDga = 0
    countSmall = 0
    countBoth = 0

    for item in data:
        if item[1] == 1:
            countDga += 1
        if item[2] <= 1800:
            countSmall += 1
        if item[1] == 1 and item[2] <= 1800:
            countBoth += 1

    print countDga
    print countSmall
    print countBoth
    print countBoth / float(countDga)
    print countBoth / float(countSmall)




if __name__ == '__main__':
    # index = findPeak()
    # peakAnalyse(index)
    # find_2Big2Small(
    # categorizeByDay()
    small_dgaMatch()