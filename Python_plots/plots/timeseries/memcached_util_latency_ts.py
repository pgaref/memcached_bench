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
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from plots.utils import *
from matplotlib.ticker import FuncFormatter as ff

logging.basicConfig(level=logging.INFO)

__author__ = "Panagiotis Garefalakis"
__copyright__ = "Imperial College London"

paper_mode = True


if paper_mode:
    colors = paper_colors
#    fig = plt.figure(figsize=(2.33, 1.55))
    fig = plt.figure(figsize=(4.44, 3.33))
    set_paper_rcs()
else:
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', '0.5']
    fig = plt.figure()
    set_rcs()



def m2hm(x, i):
    # h = int(x/60)
    # m = int(x%60)
    # return '%(h)02d:%(m)02d' % {'h':h,'m':m}
    return "{}".format(i)


def plot_ts(outname):
    plt.xlabel('Time in [s] ' )
    plt.ylabel("Request latency [$\mu$s]")
    plt.xticks(range(0, 25, 5), [str(x) for x in range(0, 25, 5)])
    plt.xlim(0, 25)
    plt.savefig("%s-90th.pdf" % outname, format="pdf", bbox_inches="tight")


def file_parser(fnames):

    for f in fnames:
        print "Analyzing %s:" % (f)

        # parsing
        j = 0
        minrto_outliers = 0
        values = {}
        ts_windows = []
        ts_window = 0
        curr_ts = 0
        for line in open(f).readlines():
            fields = [x.strip() for x in line.split()]
            if fields[0] not in ["GET", "SET", "TOTAL"]:
                print "Skipping line '%s'" % (line)
                continue
            req_type = fields[0]
            req_ts = datetime.datetime.utcfromtimestamp(float(fields[3])/1000000000.0)
            req_latency = int(fields[5])
            if req_latency > 200000:
                minrto_outliers += 1

            if (curr_ts == 0) or (req_ts > (curr_ts + datetime.timedelta(seconds=1))):
                curr_ts = req_ts
                ts_window += 1
                ts_windows.append(curr_ts)

            if ts_window in values:
                values[ts_window].append(req_latency)
            else:
                values[ts_window] = []
                values[ts_window].append(req_latency)

            j += 1

        i = 0
        print "--------------------------------------"
        print "%s (%s)" % (labels[i], f)
        print "--------------------------------------"
        print "%d total samples" % (j)
        print "%d outliers due to MinRTO" % (minrto_outliers)
        print "--------------------------------------"

        ts = 1
        perc_values = []
        while ts <= ts_window:
            print "-> Window(%d) - Samples: %d" % (ts, len(values[ts]))
            avg = np.mean(values[ts])
            print "%s - AVG: %f" % (ts, avg)
            median = np.median(values[ts])
            print "%s - MEDIAN: %f" % (ts, median)
            min_val = np.min(values[ts])
            print "%s - MIN: %ld" % (ts, min_val)
            max_val = np.max(values[ts])
            print "%s - MAX: %ld" % (ts, max_val)
            stddev = np.std(values[ts])
            print "%s - STDEV: %f" % (ts, stddev)
            print "%s - PERCENTILES:" % (ts)
            perc1 = np.percentile(values[ts], 1)
            print " 1st: %f" % (perc1)
            perc10 = np.percentile(values[ts], 10)
            print " 10th: %f" % (np.percentile(values[ts], 10))
            perc25 = np.percentile(values[ts], 25)
            print " 25th: %f" % (np.percentile(values[ts], 25))
            perc50 = np.percentile(values[ts], 50)
            print " 50th: %f" % (np.percentile(values[ts], 50))
            perc75 = np.percentile(values[ts], 75)
            print " 75th: %f" % (np.percentile(values[ts], 75))
            perc90 = np.percentile(values[ts], 90)
            print " 90th: %f" % (np.percentile(values[ts], 90))
            perc99 = np.percentile(values[ts], 99)
            print " 99th: %f" % (np.percentile(values[ts], 99))
            perc_values.append(perc99)
            ts += 1
        plt.plot(range(1, ts_window+1, 1), perc_values, 'ro')
        i += 1


if __name__ == '__main__':

    print "Ssytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: memcached_latency_cdf.py <input file 1> <label 1> ... " \
          "<input  file n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "memcached_latency_ts"

    fnames = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fnames.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format("".join(fname for fname in fnames))
    print 'Labels given: {}'.format("".join(label for label in labels))

    file_parser(fnames)
    plot_ts(outname)