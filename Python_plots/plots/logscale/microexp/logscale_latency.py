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


files = ["CPLEX-off_stats.csv", "CPLEX-on_stats.csv", "GR-NODE_CAND_stats.csv", "GR-SERIAL_stats.csv", "GR-RANDOM_stats.csv"]
labels = ["ILP-offline", "ILP-online", "Node Candidates", "Random"]
labels_map={"CPLEX-on": "ILP-online", "CPLEX-off": "ILP-offline",
            "GR-NODE_CAND": "Node Candidates", "GR-RANDOM": "Greedy", "GR-SERIAL": "Aurora"}


# colors = ['r', 'g', 'b', 'black', 'c', 'm']
markers = ['o', '^', 'v', 'h', 'x']
linestyle_list = ['--', '-', ':', '-', '-.']

# Global style configuration
utils.set_rcs()


def latency_logscale(data):
    fig = utils.plt.figure()
    fig.set_size_inches(4, 2.8)
    ax = fig.add_subplot(111)

    space = 0.25

    conditions = np.unique(data[:, 0])
    categories = np.unique(data[:, 1])
    # n = len(conditions)
    n = len(labels_map)

    width = (1 - space) / n
    print "width:", width

    i = 0
    for cond in conditions:
        print "cond:", cond
        y_vals = data[data[:, 0] == cond][:, 2].astype(np.float)
        x_vals = data[data[:, 0] == cond][:, 1].astype(np.int)
        pos = [j - (1 - space) / 2. + i * width for j in range(1, len(categories) + 1)]
        if labels_map.has_key(str(cond).strip()):
            ax.plot(x_vals, y_vals, label=labels_map[str(cond).strip()], color=colors[i], linestyle=linestyle_list[i],
                    marker=markers[i], linewidth=1.5,)
            # ,   edgecolor=get_colors()[i+1],hatch=hatch_patterns[i])
            i +=1

    indexes = range(1, len(categories) + 1)
    print "Indexes: ", indexes
    print "Categories: ", categories

    # Add the axis labels
    ax.set_ylabel("Latency (ms)", fontsize=12)
    ax.set_xlabel("Number of Nodes", fontsize=12)

    # Make Y axis logscale
    utils.plt.yscale('log', nonposy='clip')
    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    utils.plt.tight_layout()
    # Create some space for the last marker
    utils.plt.xlim((0, x_vals[len(x_vals)-1]+10))

    return fig, ax


def file_parser(fnames):
    file_data = (pd.read_csv(f) for f in fnames)
    all_data = pd.concat(file_data, ignore_index=True)
    # grouped_data = all_data.groupby(['  Plan technique', '  totJobs'])['  ObjectiveValue '].mean()
    print all_data.columns.values
    # print grouped_data
    numpyMatrix = all_data[['  Plan technique', '  clusterSize', '  runTime(ms)']].values
    # print numpyMatrix
    return numpyMatrix


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
        print "Usage: bars_efficiency.py.py <input PATH>"
        sys.exit(-1)
    outname = "placement_latency_log"

    fpaths = []
    for file in files:
      fpaths.append(sys.argv[1]+"/"+file)
      # labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))
    # print 'Labels given: {}'.format(" | ".join(label for label in labels))
    # print brewer2mpl.print_maps()

    data = file_parser(fpaths)
    fig, axes = latency_logscale(data)
    utils.set_rcs(isboxPlot=True)
    utils.plt.grid(True, which='major', alpha=0.3)
    utils.prepare_legend(legend_loc="upper left")
    utils.writeout("%s"%outname)