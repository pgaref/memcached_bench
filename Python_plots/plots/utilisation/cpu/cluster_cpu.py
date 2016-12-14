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
import datetime
import plots.utils as utils
from matplotlib import dates

linestyle_list = ['--', '-.', ':', '-']
markers = ['o', '^', 'v', 'h', 'x']



fig = utils.plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_xlabel("Time")

nodeIndex=0


def plot_timeseries(data, nodeName):
    global nodeIndex
    # Timestamps
    start_ts = datetime.datetime.now()
    x = np.array([start_ts + datetime.timedelta(seconds=j) for j in range(len(data))])
    y = np.asarray(data).squeeze()
    utils.plt.plot(x, y, linewidth=0.5, label=nodeName, linestyle=linestyle_list[nodeIndex%len(linestyle_list)])
    nodeIndex += 1


def prepare_my_legend(legend_loc=1, legend_ncol=1, legend_font='small'):
    utils.rc('legend', frameon=True)
    legfont = utils.fnt.FontProperties()
    legfont.set_size(legend_font)
    leg = utils.plt.legend(loc=legend_loc, ncol=legend_ncol, fancybox=True, prop=legfont, bbox_to_anchor=(0.5, 1.15))
    leg.get_frame().set_alpha(0.7)

    hfmt = dates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_locator(dates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(hfmt)
    ax1.set_ylim(bottom=0)
    # fig.autofmt_xdate()
    utils.plt.xticks(rotation=15)
    return


def file_parser(fnames, nodes):
    i = 0
    for f in fnames:
        file_data = pd.read_csv(f)
        # grouped_data = all_data.groupby(['  Plan technique', '  totJobs'])['  ObjectiveValue '].mean()
        # print file_data.columns.values
        # print file_data
        numpyMatrix = file_data[['Avg_CPU_usage']].values
        # numpyMatrix = file_data[['Total_CPU_usage_percent']].values
        # numpyMatrix = average(numpyMatrix, 10)
        # print numpyMatrix
        plot_timeseries(numpyMatrix, nodes[i])
        i += 1
    file_data = (pd.read_csv(f) for f in fnames)
    all_data = pd.concat(file_data, ignore_index=True)
    numpyMatrix = all_data[['Avg_CPU_usage']].values
    # numpyMatrix = np.asarray(numpyMatrix).squeeze()
    # print "=> Average CPU Utilisation is: %.2f " % (np.mean(numpyMatrix.astype(np.float)))
    ax1.set_ylabel("CPU Utilization Perc. - Avg ( %.2f )"% (np.mean(numpyMatrix.astype(np.float))))
    ax1.set_ylim(0, 100)


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
        print "Usage: cluster_cpu.py <input PATH>"
        sys.exit(-1)

    outname = "cluster_cpu"

    fpaths = []
    nodes = []
    for i in range(30, 46):
        file = 'wombat'+str(i)+'_stats.csv'
        nodes.append('wombat'+str(i))
        fpaths.append(sys.argv[1]+"/"+file)
        # labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))
    # print 'Labels given: {}'.format(" | ".join(label for label in labels))
    file_parser(fpaths, nodes)
    prepare_my_legend(legend_loc="upper center", legend_ncol=5, legend_font=8)
    utils.writeout("%s"%outname)
