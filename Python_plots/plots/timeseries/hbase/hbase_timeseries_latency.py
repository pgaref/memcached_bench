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
from matplotlib import dates


plt.style.use('seaborn-white')
plt.style.use('seaborn-white')
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'],
                  'serif': ['Helvetica'], 'size': 14})
rc('text', usetex=True)
rc('legend', fontsize=12)
rc('axes', linewidth=0.5)
rc('lines', linewidth=0.5)


# paper_colors = ['#496ee2', '#8e053b', 'g', '#ef9708', '0', '#ff3399', '0.5', 'c', '0.7']
colors = ['b', 'r', 'g', 'c', 'm']


# ALL DATA
latency_data = {}

# ALL workloads
systems_compared = ['YARN', 'YARN-Cgroups', 'MEDEA']
workloads = ["A", "B", "C", "D", "E", "F"]
# systems_compared = ['YARN']
# workloads = ["A"]


def plot_ts(outname):

    for name in workloads:
        fig = plt.figure()
        # fig, axes = plt.subplots(ncols=len(workloads), sharey=True)
        # fig.subplots_adjust(wspace=0)
        ax1 = fig.add_subplot(121)
        ax1.set_xlabel("Time (minutes)")
        ax1.set_ylabel("Request Latency [ms]")

        i = 0
        handles = []
        for item in systems_compared:
            #Timestamps
            start_ts.replace(minute=0, second=0, microsecond=0)
            x = np.array([start_ts + datetime.timedelta(seconds=j) for j in range(len(latency_data[name][item]))])
            y = latency_data[name][item]
            plt.plot(x, y, color=colors[i], label=item)
            i += 1
        ax1.grid(True)
        ax1.legend(loc='upper right')
        hfmt = dates.DateFormatter('%M:%S')
        ax1.xaxis.set_major_locator(dates.MinuteLocator())
        ax1.xaxis.set_major_formatter(hfmt)
        ax1.set_ylim(bottom=0)
        # fig.autofmt_xdate()
        ax1.set_xticklabels(ax1.xaxis.get_majorticklabels(), rotation=90)
        print "Done with plots"
        plt.savefig("%s.pdf"%(outname+"_w"+name), format="pdf", bbox_inches="tight")
        print "Done with Writing to file"
        # plt.show()
        plt.clf()


def add_values(latency_values, workload, label):
    latency_data[workload][label] = latency_values


#############################################
# Message Format:
# {READ | INSERT | UPDATE},TIMESTAMP,LATENCY (us)
#############################################
start_ts = 0
end_ts = 0
def file_parser(fnames, workload):
    i = 0
    for f in fnames:
        print "Analyzing %s:" % (f)

        # parsing
        j = 0
        minrto_outliers = 0

        req_count = 0
        current_ts = 0
        all_values = []
        latency_sum = []
        latency_perc_values = []
        throughput_values = []
        for line in open(f).readlines():
            fields = [x.strip() for x in line.split(",")]
            if fields[0] not in ["READ", "INSERT", "UPDATE", "SCAN", "READ-MODIFY-WRITE"]:
                if (fields[0] not in ["CLEANUP"]) and (fields[1] not in ["latency"]):
                    print 'TYPE: %s -> NOT KNOWN '% fields[0]
                continue
            req_type = fields[0]
            req_ts = datetime.datetime.fromtimestamp( float(fields[1]) / 1000.0)
            req_latency = int(fields[2]) # Latency in micros
            req_latency = int(req_latency/1000) # Convert to millis
            if req_latency > 200:
                minrto_outliers += 1
            else:
                all_values.append(req_latency)
                if current_ts == 0:
                    current_ts = req_ts
                    latency_sum.append(req_latency)
                    req_count = 1
                elif (req_ts - current_ts).total_seconds() >= 1:
                    latency_perc_values.append(np.percentile(latency_sum, 99))
                    throughput_values.append(req_count)

                    req_count = 1
                    current_ts = req_ts
                    latency_sum = []
                    latency_sum.append(req_latency)
                else:
                    req_count += 1
                    latency_sum.append(req_latency)


            #print "request: %s ts %s latency %d" % (req_type, str( req_ts), req_latency)

            # Start and End timestamps
            if j == 0:
                global start_ts
                start_ts = req_ts
            elif j != 0:
                global end_ts
                end_ts = req_ts
            j += 1
        print "--------------------------------------"
        print "%s (%s)" % (labels[i], f)
        print "--------------------------------------"
        print "%d total samples" % (j)
        print "Runtime: %d seconds"% (end_ts-start_ts).total_seconds()
        print "%d outliers due to MinRTO" % (minrto_outliers)
        print "--------------------------------------"

        # for type in ['READ', 'INSERT']:
        if len(all_values) == 0:
            continue
        # print "===== TYPE: %s ====="% (type)
        print "Throughput: %d req/sec" % (j / (end_ts - start_ts).total_seconds())
        avg = np.mean(all_values)
        print "AVG: %f" % (avg)
        median = np.median(all_values)
        print "MEDIAN: %f" % (median)
        min_val = np.min(all_values)
        print "MIN: %ld" % (min_val)
        max_val = np.max(all_values)
        print "MAX: %ld" % (max_val)
        stddev = np.std(all_values)
        print " STDEV: %f" % (stddev)
        print " PERCENTILES:"
        perc10 = np.percentile(all_values, 10)
        print " 10th: %f" % (np.percentile(all_values, 10))
        perc25 = np.percentile(all_values, 25)
        print " 25th: %f" % (np.percentile(all_values, 25))
        perc50 = np.percentile(all_values, 50)
        print " 50th: %f" % (np.percentile(all_values, 50))
        perc75 = np.percentile(all_values, 75)
        print " 75th: %f" % (np.percentile(all_values, 75))
        perc90 = np.percentile(all_values, 90)
        print " 90th: %f" % (np.percentile(all_values, 90))
        perc99 = np.percentile(all_values, 99)
        print " 99th: %f" % (np.percentile(all_values, 99))

        add_values(latency_perc_values, workload, labels[i])

        i += 1


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: hbase_timeseries_throughput.py <input PATH> <label 1> ... " \
          "<input PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "hbase_latency_ts"

    fpaths = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fpaths.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'Paths given: {}'.format("".join(fname for fname in fpaths))
    print 'Labels given: {}'.format("".join(label for label in labels))

    for workload in workloads:
        fnames = []
        for path in  fpaths:
            fnames.append(path + "write-w"+workload+"-10R.dat")
        print "Processing.. "+ str(fnames)
        latency_data[workload] = {}
        file_parser(fnames, workload)

    plot_ts(outname)