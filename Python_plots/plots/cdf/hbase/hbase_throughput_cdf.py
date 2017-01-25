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
# SOFTWARE
import numpy as np
import datetime
import sys
import os
import plots.utils as utils


colors = ['r', 'g', 'b', 'm', 'c']
markers = ['o', '^', 'v', 'h']
linestyle_list = ['--', '-.', '-', ':']

# ALL workloads
workloads = ["A", "B", "C", "D", "E", "F"]
systems_compared = ['YARN', 'YARN-Cgroups', 'MEDEA', 'MEDEA-Cgroups']

# Global style configuration
utils.set_rcs(figureStyle=3)


def cdf(data, label, label_count):
    data_size = len(data)
    # Set bins edges
    data_set = sorted(set(data))
    bins = np.append(data_set, data_set[-1]+1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(data, bins=bins, density=False)
    counts = counts.astype(float)/data_size

    # Find the cdf
    cdf = np.cumsum(counts)

    # Starting point (0,0)
    bin_edges[0] = 0
    cdf[0] = 0

    # Plot the cdf
    # plt.plot(bin_edges[0:-1], cdf, linestyle='--', marker='o', label=label, color=colors[label_count])
    utils.plt.plot(bin_edges[0:-1], cdf, linestyle=linestyle_list[label_count], label=label, color=colors[label_count])


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
            all_values.append(req_latency/1000.0)
            if current_ts == 0:
                current_ts = req_ts
                latency_sum.append(req_latency)
                req_count = 1
            elif (req_ts - current_ts).total_seconds() >= 1:
                if "wE" in f and (req_count / 1000 > 5000) or (req_count / 1000 > 4000):
                    req_count = 1
                    current_ts = req_ts
                    latency_sum = []
                else:
                    latency_perc_values.append(np.percentile(latency_sum, 99))
                    if "wE" in f:
                        throughput_values.append(req_count)
                    else:
                        throughput_values.append(req_count / 1000)
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
        print "MIN: %f" % (min_val)
        max_val = np.max(all_values)
        print "MAX: %ld" % (max_val)
        stddev = np.std(all_values)
        print " STDEV: %f" % (stddev)
        print " PERCENTILES:"
        perc1 = np.percentile(all_values, 1)
        print " 1th: %f" % perc1
        perc10 = np.percentile(all_values, 10)
        print " 10th: %f" % perc10
        perc25 = np.percentile(all_values, 25)
        print " 25th: %f" % perc25
        perc50 = np.percentile(all_values, 50)
        print " 50th: %f" % perc50
        perc75 = np.percentile(all_values, 75)
        print " 75th: %f" % perc75
        perc90 = np.percentile(all_values, 90)
        print " 90th: %f" % perc90
        perc99 = np.percentile(all_values, 99)
        print " 99th: %f" % perc99

        throughput_values = utils.reject_outliers(np.array(throughput_values))
        cdf(throughput_values, labels[i], i)

        i += 1


if __name__ == '__main__':

    print "System Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: hbase_throughput_cdf.py <input PATH 1> <label 1> ... " \
          "<input  PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "hbase_throughput_cdf_"

    fpaths = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fpaths.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'Paths given: {}'.format(" | ".join(fname for fname in fpaths))
    print 'Labels given: {}'.format(" | ".join(label for label in labels))

    for workload in workloads:
        fnames = []
        for path in fpaths:
            fnames.append(path + "write-w"+workload+"-10R.dat")
        print "Processing.. "+ str(fnames)
        file_parser(fnames)
        if "E" in workload:
            utils.plot_cdf(outname+"w"+workload, ylabel="Throughput [ops/s]")
        else:
            utils.plot_cdf(outname + "w" + workload, ylabel="Throughput [Kops/s]")