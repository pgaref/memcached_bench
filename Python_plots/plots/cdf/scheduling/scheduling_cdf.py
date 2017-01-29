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
from dateutil.parser import parse
import time
import sys
import os
import plots.utils as utils


colors = ['r', 'g', 'b', 'm', 'c']
markers = ['o', '^', 'v', 'h']
linestyle_list = ['--', '-.', '-', ':']

# ALL workloads
# workloads = ["A", "B", "C", "D", "E", "F"]
# systems_compared = ['YARN', 'YARN-Cgroups', 'MEDEA', 'MEDEA-Cgroups']

# Global style configuration
utils.set_rcs()


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


containers_start_map = {}
containers_finish_map = {}

data = {}
def file_parser(fnames, flabels):
    i = 0
    for f in fnames:
        print "Analyzing %s:" % (f)
        for line in open(f).readlines():
            # Skip information  Line
            if "Container Transitioned from ACQUIRED to RUNNING" in line:
                now =  parse(line.split(",")[0])
                fields = line.split(":")
                container = [x.strip() for x in fields[3].split(" ")][1]
                containers_start_map[container] = []
                containers_start_map[container].append(now)
            elif "Container Transitioned from RUNNING to COMPLETED" in line:
                then = parse(line.split(",")[0])
                fields = line.split(":")
                container = [x.strip() for x in fields[3].split(" ")][1]
                containers_finish_map[container] = []
                containers_finish_map[container].append(then)
                # fields = [x.strip() for x in line.split(",")]
                # if fields[0] not in op_values.keys():
                #     print 'TYPE: %s -> NOT KNOWN ' % (fields[0])
                # else:
                #     req_type = fields[0]
                #     req_ts = datetime.datetime.fromtimestamp( float(fields[1]) / 1000.0) # Timestamp in ms
                #     req_latency = int(fields[2]) # Latency in micros
                #     op_values[req_type].append(req_latency/1000.0) # Convert to ms
                #     # if (req_latency > 200) or (req_latency <=0.0):
                #     #     minrto_outliers += 1
                #     # else:
                #     #     values.append(req_latency)
                #     #print "request: %s ts %s latency %d" % (req_type, str( req_ts), req_latency)
                #     # Start and End timestamps
                #     if j == 0:
                #         start_ts = req_ts
                #     elif j != 0:
                #         end_ts = req_ts
                #     j += 1

        values = []
        for k in containers_finish_map.keys():
            if (containers_finish_map[k][0] - containers_start_map[k][0]).seconds < 250:
                values.append((containers_finish_map[k][0] - containers_start_map[k][0]).seconds)
        data[flabels[i]] =[]
        data[flabels[i]].append(values)

        cdf(values, labels[i], i)
        i += 1


if __name__ == '__main__':

    print "System Path {}".format(os.environ['PATH'])

    # if len(sys.argv) < 2:
    #   print "Usage: scheduling_cdf.py <input PATH 1> <label 1> ... " \
    #       "<input  PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "two_level_scheduling_cdf"

    fpaths = ['../../../data/two_level/hadoop-pg1712-resourcemanager-wombat30-batch.log',
              '../../../data/two_level/hadoop-pg1712-resourcemanager-wombat30-service.log',
              '../../../data/two_level/hadoop-pg1712-resourcemanager-wombat30-service2.log']
    labels = ['Batch Only',
              'Batch \& Service',
              'Batch \& Service2']
    for i in range(0, len(sys.argv) - 1, 2):
      fpaths.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'PATH given: {}'.format("".join(fname for fname in fpaths))
    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))


    print "Processing.. " + str(fpaths)
    file_parser(fpaths, labels)
    utils.plot_cdf(outname, ylabel="Task responce time [sec]")
    utils.plot_boxplot(data, "two_level_scheduling_boxplot", labels, labels)
