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

import numpy as np
import datetime
import sys
import os
import plots.utils as utils


# Global style configuration
utils.set_rcs()


# ALL DATA
data = {}

# ALL workloads
workloads = ["A", "B", "C", "D", "E", "F"]
systems_compared = ['YARN', 'YARN-Cgroups', 'MEDEA', 'MEDEA-Cgroups']



def add_values(values, workload, label):
    data[workload][label] = values


#############################################
# Message Format:
# {READ | INSERT | TOTAL},TIMESTAMP,LATENCY (us)
#############################################
def file_parser(fnames, workload):
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
            fields = [x.strip() for x in line.split(",")]
            if fields[0] not in ["READ", "INSERT", "UPDATE", "SCAN", "READ-MODIFY-WRITE"]:
                if (fields[0] not in ["CLEANUP"]) and (fields[1] not in ["latency"]):
                    print 'TYPE: %s -> NOT KNOWN '% fields[0]
                continue
            req_type = fields[0]
            req_ts = datetime.datetime.fromtimestamp( float(fields[1]) / 1000.0)
            req_latency = int(fields[2]) # Latency in micros
            req_latency = int(req_latency/1000.0) # Convert to millis
            if req_latency > 0.0:
                values.append(req_latency)
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
        if len(values) == 0:
            continue
        # print "===== TYPE: %s ====="% (type)
        print "Throughput: %d req/sec" % (j / (end_ts - start_ts).total_seconds())
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

        values = utils.reject_outliers(np.array(values))

        print " ===> 99th: %f" % (np.percentile(values, 99))
        add_values(values, workload, labels[i])

        i += 1


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: hbase_boxplot_latency_percentiles.py <input PATH> <label 1> ... " \
          "<input PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "hbase_latency_boxes"

    fpaths = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fpaths.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'Paths given: {}'.format(" | ".join(fname for fname in fpaths))
    print 'Labels given: {}'.format(" | ".join(label for label in labels))

    for workload in workloads:
        fnames = []
        for path in  fpaths:
            fnames.append(path + "write-w"+workload+"-10R.dat")
        print "Processing.. "+ str(fnames)
        data[workload] = {}
        file_parser(fnames, workload)

    utils.plot_multiboxplot(data, outname, ["A", "B", "C", "D", "F"], systems_compared, labels)
    # /media/mydatadrive/Medea/results-test/yarn/test/ YARN /media/mydatadrive/Medea/results-test/yarn-cgroups/test/ YARN-Cgroups /media/mydatadrive/Medea/results-test/medea/test/ MEDEA /media/mydatadrive/Medea/results-test/medea-cgroups/test/ MEDEA-Cgroups