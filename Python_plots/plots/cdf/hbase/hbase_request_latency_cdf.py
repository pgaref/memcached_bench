__author__ = 'pg1712'

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

import datetime
import logging
import os, sys, re
import numpy as np
import matplotlib
# import seaborn as sns
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
from Python_plots.plots.utils import *

logging.basicConfig(level=logging.INFO)

__author__ = "Panagiotis Garefalakis"
__copyright__ = "MSR"

paper_mode = True

if paper_mode:
    colors = paper_colors
#    fig = plt.figure(figsize=(2.33, 1.55))
    fig = plt.figure(figsize=(4.44, 3.33))
    set_paper_rcs()
else:
    colors = ['b', 'r', 'g', 'c', 'm', 'k', 'y', '0.5']
    fig = plt.figure()
    set_rcs()


def plot_cdf(outname):

    plt.xticks()
    #  plt.xscale("log")
    plt.xlim(0, 60)
    plt.xticks(range(0, 61, 10), [str(x) for x in range(0, 61, 10)])
    plt.ylim(0, 1.0)
    plt.yticks(np.arange(0.0, 1.01, 0.1), [str(x) for x in np.arange(0.0, 1.01, 0.1)])
    plt.xlabel("Request latency [$m$s]")
    plt.ylabel("CDF")
    # print n
    # print bins
    # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    #           ncol=3, mode="expand", frameon=True, borderaxespad=0.)
    plt.legend(loc=4, frameon=False, handlelength=2.5, handletextpad=0.2)
    plt.savefig("%s.pdf" % outname, format="pdf", bbox_inches="tight")
    # plt.ylim(0.9, 1.0)
    #plt.axhline(0.999, ls='--', color='k')
    # plt.savefig("%s-90th.pdf" % outname, format="pdf", bbox_inches="tight")


def add_plt_values(values, min_val, max_val, label, label_count, req_type):
    # figure out number of bins based on range
    bin_width = 0.01  # 7.5ns measurement accuracy
    bin_range = max_val - min_val
    num_bins = min(600000, bin_range / bin_width)
    print "Binning into %d bins and plotting..." % (num_bins)

    # plotting
    if paper_mode:
        #    plt.rc("font", size=8.0)
        label_str = label
        if label_count % 3 == 0:
            style = 'solid'
        elif label_count % 3 == 1:
            style = 'dashed'
        else:
            style = 'dotted'
        (n, bins, patches) = plt.hist(values, bins=num_bins, log=False, normed=1,
                                      cumulative=True, histtype="step",
                                      ls=style, color=colors[label_count])
        # hack to add line to legend
        plt.plot([-100], [-100], label=label_str, color=colors[label_count],
                 linestyle=style, lw=1.0)
        # hack to remove vertical bar
        patches[0].set_xy(patches[0].get_xy()[:-1])
    else:
        label_str = "%s (%s)" % (label, req_type)
        (n, bins, patches) = plt.hist(values, bins=num_bins, log=False, normed=1,
                                      cumulative=True, histtype="step",
                                      label=label_str)
        # hack to remove vertical bar
        patches[0].set_xy(patches[0].get_xy()[:-1])


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
        values = {'READ': [], 'INSERT': [], 'TOTAL': []}
        for line in open(f).readlines():
            fields = [x.strip() for x in line.split(",")]
            if fields[0] == "CLEANUP " or\
                fields[0] not in ["READ", "INSERT"] or\
                fields[1] == "latency":
#                print "Skipping line '%s'" % (line)
                continue
            req_type = fields[0]
            req_ts = datetime.datetime.fromtimestamp( float(fields[1]) / 1000.0)
            req_latency = int(fields[2]) # Latency in micros
            req_latency = int(req_latency/1000) # Convert to millis
            if req_latency > 200:
                minrto_outliers += 1
            values[req_type].append(req_latency)

            #print "request: %s ts %s latency %d" % (req_type, str( req_ts), req_latency)

            # Start and End timestamps
            if j == 0:
                start_ts = req_ts
            elif j != 0:
                end_ts = req_ts
            j += 1
        print "--------------------------------------"
        print "%s (%s)" % (labels[i], f)
        print "--------------------------------------"
        print "%d total samples" % (j)
        print "Runtime: %d seconds"% (end_ts-start_ts).total_seconds()
        print "%d outliers due to MinRTO" % (minrto_outliers)
        print "--------------------------------------"
        for type in ['READ', 'INSERT']:
            if len(values[type])==0:
                continue
            print "===== TYPE: %s ====="% (type)
            print "Throughput: %d req/sec"% (j/(end_ts-start_ts).total_seconds())
            avg = np.mean(values[type])
            print "%s - AVG: %f" % (type, avg)
            median = np.median(values[type])
            print "%s - MEDIAN: %f" % (type, median)
            min_val = np.min(values[type])
            print "%s - MIN: %ld" % (type, min_val)
            max_val = np.max(values[type])
            print "%s - MAX: %ld" % (type, max_val)
            stddev = np.std(values[type])
            print "%s - STDEV: %f" % (type, stddev)
            print "%s - PERCENTILES:" % (type)
            perc1 = np.percentile(values[type], 1)
            print " 1st: %f" % (perc1)
            perc10 = np.percentile(values[type], 10)
            print " 10th: %f" % (np.percentile(values[type], 10))
            perc25 = np.percentile(values[type], 25)
            print " 25th: %f" % (np.percentile(values[type], 25))
            perc50 = np.percentile(values[type], 50)
            print " 50th: %f" % (np.percentile(values[type], 50))
            perc75 = np.percentile(values[type], 75)
            print " 75th: %f" % (np.percentile(values[type], 75))
            perc90 = np.percentile(values[type], 90)
            print " 90th: %f" % (np.percentile(values[type], 90))
            perc99 = np.percentile(values[type], 99)
            print " 99th: %f" % (np.percentile(values[type], 99))

            add_plt_values(values[type], min_val, max_val, labels[i], i, type)

        i += 1


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: memcached_latency_cdf.py <input file 1> <label 1> ... " \
          "<input  file n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "hbase_req_latency_cdf"

    fnames = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fnames.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format("".join(fname for fname in fnames))
    print 'Labels given: {}'.format("".join(label for label in labels))

    file_parser(fnames)
    plot_cdf(outname)
# ../../../data/results/yarn/write-wB-1R.dat WorkloadB ../../../data/results/yarn/write-wC-1R.dat WorkloadC ../../../data/results/yarn/write-wD-1R.dat WorkloadD ../../../data/results/yarn/write-wE-1R.dat WorkloadE ../../../data/results/yarn/write-wF-1R.dat WorkloadF