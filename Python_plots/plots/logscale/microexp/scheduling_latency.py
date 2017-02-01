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
import sys
import os
import numpy as np
import pandas as pd
import plots.utils as utils
import brewer2mpl

# brewer2mpl.get_map args: set name  set type  number of colors
# bmap = brewer2mpl.get_map('RdBu', 'Diverging', 5)
bmap = brewer2mpl.get_map('Set1', 'Qualitative', 5)
colors = bmap.mpl_colors


files = ["ILP-on_stats.csv", "ILP-2lvl_stats.csv"]
labels_map={"ILP-on": "ILP-ALL", "ILP-2lvl": "MEDEA",
            "GR-NODE_CAND": "Node Candidates", "GR-RANDOM": "Greedy", "GR-SERIAL": "Aurora"}


# colors = ['r', 'g', 'b', 'black', 'c', 'm']
markers = ['o', '^', 'v', 'h', 'x']
linestyle_list = ['--', '-', ':', '-', '-.']

# Global style configuration
utils.set_rcs()


def scheduling_latency(data):
    fig = utils.plt.figure()
    ax = fig.add_subplot(111)


    conditions = np.unique(data[:, 0])
    categories = np.unique(data[:, 1])
    # n = len(conditions)
    n = len(labels_map)


    i = 0
    for cond in conditions:
        print "cond:", cond
        y_vals = data[data[:, 0] == cond][:, 2].astype(np.float)/720
        x_vals = data[data[:, 0] == cond][:, 1].astype(np.int)

        if labels_map.has_key(str(cond).strip()):
            ax.plot(x_vals, y_vals, label=labels_map[str(cond).strip()], color=colors[i], linestyle=linestyle_list[i],
                    marker=markers[i], linewidth=1)
            i +=1

    indexes = []
    for c in  categories:
        indexes.append(c)
    # range(1, len(categories) + 1)
    print "Indexes: ", indexes
    print "Categories: ", categories
    ax.set_xticks(indexes)
    ax.set_xticklabels(["0", "5", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])
    utils.plt.setp(utils.plt.xticks()[1], rotation=00)
    ax.set_xlim(0, indexes[len(indexes)-1]+1)

    # Add the axis labels
    ax.set_ylabel("Task scheduling Latency (ms)")
    ax.set_xlabel("Percentage of Services")

    # Make Y axis logscale
    # utils.plt.yscale('log', nonposy='clip')
    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    utils.plt.tight_layout()
    # Create some space for the last marker
    # utils.plt.xlim((0, x_vals[len(x_vals)-1]+10))

    return fig, ax


def file_parser(fnames):
    file_data = (pd.read_csv(f) for f in fnames)
    all_data = pd.concat(file_data, ignore_index=True)
    # grouped_data = all_data.groupby(['  Plan technique', '  totJobs'])['  ObjectiveValue '].mean()
    print all_data.columns.values
    # print grouped_data
    numpyMatrix = all_data[['  Plan technique', '  numServiceJobs', '  runTime(ms)']].values
    # print numpyMatrix
    return numpyMatrix


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    # if len(sys.argv) < 2:
    #     print "Usage: scheduling_latency.py <input PATH>"
    #     sys.exit(-1)
    outname = "scheduling_latency"

    path = "/Users/pgaref/Development/memcached_bench/Python_plots/data/medea_scheduling2/"
    fpaths = []
    for file in files:
      fpaths.append(path+"/"+file)
      # labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))
    # print 'Labels given: {}'.format(" | ".join(label for label in labels))
    # print brewer2mpl.print_maps()

    data = file_parser(fpaths)
    fig, axes = scheduling_latency(data)
    utils.set_rcs()
    utils.plt.grid(True, which='major', alpha=0.3)
    utils.prepare_legend(legend_loc="upper left", alpha_num=1.0)
    utils.writeout("%s"%outname)