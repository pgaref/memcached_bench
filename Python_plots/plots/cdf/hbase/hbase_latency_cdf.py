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
        op_values = {"READ": [], "INSERT": [], "UPDATE": [], "CLEANUP": [],
                     "SCAN": [], "READ-MODIFY-WRITE": []}
        for line in open(f).readlines():
            # Skip information  Line
            if "latency" in line:
                print '-> Skipping info Line: %s' % line
                continue
            else:
                fields = [x.strip() for x in line.split(",")]
                if fields[0] not in op_values.keys():
                    print 'TYPE: %s -> NOT KNOWN ' % (fields[0])
                else:
                    req_type = fields[0]
                    req_ts = datetime.datetime.fromtimestamp( float(fields[1]) / 1000.0) # Timestamp in ms
                    req_latency = int(fields[2]) # Latency in micros
                    op_values[req_type].append(req_latency/1000.0) # Convert to ms
                    # if (req_latency > 200) or (req_latency <=0.0):
                    #     minrto_outliers += 1
                    # else:
                    #     values.append(req_latency)
                    #print "request: %s ts %s latency %d" % (req_type, str( req_ts), req_latency)
                    # Start and End timestamps
                    if j == 0:
                        start_ts = req_ts
                    elif j != 0:
                        end_ts = req_ts
                    j += 1

        # values = utils.reject_outliers(np.array(values))

        for op in op_values.keys():
            # Skipping empty operations
            if len(op_values[op]) == 0:
                continue
            print "--------------------------------------"
            print "%s (%s)" % (labels[i], f)
            print "--------------------------------------"
            print "%d total samples - %d after filtering " % (j, len(op_values[op]))
            print "Runtime: %d seconds"% (end_ts-start_ts).total_seconds()
            print "%d outliers due to MinRTO" % (minrto_outliers)
            print "--------------------------------------"

            print "===== TYPE: %s ====="% (op)
            print "Throughput: %d req/sec" % (j / (end_ts - start_ts).total_seconds())
            avg = np.mean(op_values[op])
            print "AVG: %f" % (avg)
            median = np.median(op_values[op])
            print "MEDIAN: %f" % (median)
            min_val = np.min(op_values[op])
            print "MIN: %f" % (min_val)
            max_val = np.max(op_values[op])
            print "MAX: %ld" % (max_val)
            stddev = np.std(op_values[op])
            print " STDEV: %f" % (stddev)
            print " PERCENTILES:"
            perc1 = np.percentile(op_values[op], 1)
            print " 1st: %f" % perc1
            perc10 = np.percentile(op_values[op], 10)
            print " 10th: %f" % perc10
            perc25 = np.percentile(op_values[op], 25)
            print " 25th: %f" % perc25
            perc50 = np.percentile(op_values[op], 50)
            print " 50th: %f" % perc50
            perc75 = np.percentile(op_values[op], 75)
            print " 75th: %f" % perc75
            perc90 = np.percentile(op_values[op], 90)
            print " 90th: %f" % perc90
            perc99 = np.percentile(op_values[op], 99)
            print " 99th: %f" % perc99

        all_values = []
        for op in op_values.keys():
            all_values += op_values[op]
        values = utils.reject_outliers(np.asarray(all_values))
        cdf(values, labels[i], i)
        i += 1


if __name__ == '__main__':

    print "System Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: hbase_latency_cdf.py <input PATH 1> <label 1> ... " \
          "<input  PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "hbase_latency_cdf_"

    fpaths = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fpaths.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'PATH given: {}'.format("".join(fname for fname in fpaths))
    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))

    for workload in workloads:
        fnames = []
        for path in  fpaths:
            fnames.append(path + "write-w"+workload+"-10R.dat")
        print "Processing.. " + str(fnames)
        file_parser(fnames)
        utils.plot_cdf(outname+"w"+workload, ylabel="Request latency [ms]")