import seaborn as sns
import numpy as np
import datetime
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
markers = ['o', '^', 'v', 'h']
linestyle_list = ['-', '--', '-.']

# workloads = ["A", "B", "C", "D", "E", "F"]
systems_compared = ['No Constraints', 'Intra-Affinity', 'Inter-Affinity']


def plot_cdf(outname):
    plt.ylim((0,1))
    plt.xlim((-1))
    plt.xlabel("Operator latency [ms]")
    plt.ylabel("CDF")
    plt.grid(True)
    plt.legend(loc=4, frameon=True, handlelength=2.5, handletextpad=0.2)
    plt.savefig("%s.pdf"%outname, format="pdf", bbox_inches="tight")
    plt.show()


def cdf(data, label_count, label):

    data_size=len(data)

    # Set bins edges
    data_set=sorted(set(data))
    bins=np.append(data_set, data_set[-1]+1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(data, bins=bins, density=False)

    counts=counts.astype(float)/data_size

    # Find the cdf
    cdf = np.cumsum(counts)

    # Plot the cdf
    plt.plot(bin_edges[0:-1], cdf,linestyle='--', marker="o", label=label, color=colors[label_count])



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
        print "%d outliers due to MinRTO" % (minrto_outliers)
        print "--------------------------------------"

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
        perc1 = np.percentile(values, 1)
        print " 1st: %f" % (perc1)
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

        cdf(values, i, labels[i])

        i += 1


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: memcached_latency_cdf.py <input PATH 1> <label 1> ... " \
          "<input  PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "storm_placement_latency_cdf"

    fpaths = []
    labels = []
    for i in range(0, len(sys.argv) - 1, 2):
      fpaths.append(sys.argv[1 + i])
      labels.append(sys.argv[2 + i])

    print 'PATH given: {}'.format("".join(fname for fname in fpaths))
    print 'Labels given: {}'.format("".join(label for label in labels))

    fnames = []
    for path in fpaths:
        fnames.append(path + "trendingHashTags.log")
    print "Processing.. "+ str(fnames)
    file_parser(fnames)
    plot_cdf(outname)