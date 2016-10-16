__author__ = "Panagiotis Garefalakis"
__copyright__ = "Imperial College London"

# The MIT License (MIT)
#
# Copyright (c) 2016 Panagiotis Garefalakis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import seaborn as sns
import numpy as np
import datetime
import random
import sys
import os

import matplotlib.pyplot as plt
from matplotlib import rc

plt.style.use('seaborn-white')
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'],
                  'serif': ['Helvetica'], 'size': 14})
rc('text', usetex=True)
rc('legend', fontsize=12)
rc('axes', linewidth=1)
rc('lines', linewidth=1)


# paper_colors = ['#496ee2', '#8e053b', 'g', '#ef9708', '0', '#ff3399', '0.5', 'c', '0.7']
colors = ['b', 'r', 'g', 'c', 'm']


# ALL DATA
data = {}
# data['workloadA'] = {}

# ALL workloads
# workloads = ["A", "B", "C", "D", "E", "F"]
systems_compared = ['No Constraints', 'Intra-Affinity', 'Inter-Affinity']
# workloads = ["A", "B"]


def plot_boxes(outname):
    fig, axes = plt.subplots(ncols=1, sharey=True)
    fig.subplots_adjust(wspace=0)
    # fig.text(0.5, 0.04, "YCSB Workloads", ha='center')
    fig.text(0.04, 0.5, "Operator latency [ms]", va='center', rotation='vertical')

    # for ax, name in zip(axes, workloads):
    # whis from 5th to 99th precentile
    bt = axes.boxplot(x=[data[item] for item in systems_compared], whis=[5, 99], sym="+")
    plt.setp(bt['fliers'], color='red', marker='+')
    xtickNames = axes.set(xticklabels=systems_compared)
    plt.setp(xtickNames, rotation=90, fontsize=12)

    # workloadXtick = axes.set(xlabel='Placement Constraints')
    # plt.setp(workloadXtick, fontsize=14)

    # # Add a horizontal grid to the plot, but make it very light in color
    # # so we can use it for reading data values but not be distracting
    axes.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                    alpha=1)
    # Hide these grid behind plot objects
    axes.set_axisbelow(True)
    axes.margins(0.05)  # Optional
    # plt.ylim((0,50))
    # plt.xlim((-1,100))
    # plt.legend(loc=4, frameon=True, handlelength=2.5, handletextpad=0.2)
    print "Done with plots"
    plt.savefig("%s.pdf"%outname, format="pdf", bbox_inches="tight")
    print "Done with Writing to file"
    plt.show()


def add_values(values, label):
    data[label] = values


#############################################
# Message Format:
# {READ | INSERT | TOTAL},TIMESTAMP,LATENCY (us)
#############################################
def file_parser(fnames):
    i = 0
    for f in fnames:
        print "Analyzing %s:" % (f)

        # parsing
        j = 0
        minrto_outliers = 0
        start_ts = 0
        end_ts = 0
        values = []
        for line in open(f).readlines():
            if "STDIO [INFO] READ:" in line:
                fields = [x.strip() for x in line.split("READ:")]
                if j == 100:
                    print 'Sample Latency: %s -> '% int(fields[1])
                    print line
                    print f
                req_latency = int(fields[1]) # Latency in millis

                values.append(req_latency)
                #print "request: %s ts %s latency %d" % (req_type, str( req_ts), req_latency)
                j += 1
        print "--------------------------------------"
        print "%s (%s)" % (labels[i], f)
        print "--------------------------------------"
        print "%d total samples" % (j)
        # print "Runtime: %d seconds"% (end_ts-start_ts).total_seconds()
        # print "%d outliers due to MinRTO" % (minrto_outliers)
        print "--------------------------------------"

        # for type in ['READ', 'INSERT']:
        if len(values) == 0:
            continue
        # print "===== TYPE: %s ====="% (type)
        # print "Throughput: %d req/sec" % (j / (end_ts - start_ts).total_seconds())
        avg = np.mean(values)
        print "AVG: %f" % (avg)
        median = np.median(values)
        print "MEDIAN: %f" % (median)
        min_val = np.min(values)
        print "MIN: %ld" % (min_val)
        max_val = np.max(values)
        print "MAX: %ld" % (max_val)
        stddev = np.std(values)
        print " STDEV: %f" % (stddev)
        print " PERCENTILES:"
        perc10 = np.percentile(values, 10)
        print " 10th: %f" % (np.percentile(values, 10))
        perc25 = np.percentile(values, 25)
        print " 25th: %f" % (np.percentile(values, 25))
        perc50 = np.percentile(values, 50)
        print " 50th: %f" % (np.percentile(values, 50))
        perc75 = np.percentile(values, 75)
        print " 75th: %f" % (np.percentile(values, 75))
        perc90 = np.percentile(values, 90)
        print " 90th: %f" % (np.percentile(values, 90))
        perc99 = np.percentile(values, 99)
        print " 99th: %f" % (np.percentile(values, 99))

        add_values(values, labels[i])

        i += 1


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: stom_latency_boxplot.py <input PATH> <label 1> ... " \
          "<input PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "storm_placement_latency_boxplot"

    fpaths = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fpaths.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'Paths given: {}'.format("".join(fname for fname in fpaths))
    print 'Labels given: {}'.format("".join(label for label in labels))

    fnames = []
    for path in  fpaths:
        fnames.append(path + "trendingHashTags.log")
    print "Processing.. "+ str(fnames)
    file_parser(fnames)
    plot_boxes(outname)