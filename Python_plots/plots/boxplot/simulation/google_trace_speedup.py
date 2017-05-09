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
import sys
import os
import random
import plots.utils as utils
import csv


# Global style configuration
utils.set_rcs()



#############################################
# Message Format:
#############################################
def get_scheduling_delays(fpath):
    trace_path = fpath + "/task_latency.csv"
    print "Analyzing %s:" % (trace_path)
    is_med = False
    if 'MEDEA' in  trace_path:
        is_med = True

    csv_file = open(trace_path)
    csv_reader = csv.reader(csv_file)
    delays = []
    for row in csv_reader:
        # latency in ms
        runtime = long(row[0])
        if runtime/1000.0 > 0.01:
            delays.append(runtime/1000.0)
    csv_file.close()
    return delays


def plot_scheduling_delays(delays, labels, colors):
    utils.set_rcs()

    ax = utils.plt.gca()
    bp = utils.percentile_box_plot(ax, delays, color=colors)

    utils.plt.plot(-1, -1, label='MEDEA (short tasks)', color='b', lw=1.0)
    utils.plt.plot(-1, -1, label='YARN', color='r', lw=1.0)
#    plt.plot(-1, -1, label='Cost scaling', color='g', lw=1.0)

    for i in range(2, len(delays), 2):
        utils.plt.axvline(i + 0.5, ls='-', color='k')

    ax.legend(frameon=False, loc="upper center", ncol=6,
              bbox_to_anchor=(0.0, 1.02, 1.0, 0.1), handletextpad=0.2,
              columnspacing=0.2)

    #plt.errorbar(range(1, len(setups) + 1), [np.mean(x) for x in runtimes],
    #             yerr=[np.std(x) for x in runtimes], marker="x")
    utils.plt.xlim(0.5, len(delays) + 0.5)
    utils.plt.ylim(ymin=0, ymax=5.2)
    utils.plt.xticks([x * 2 + 1.5 for x in range(0, len(labels))], "")
    # utils.plt.yticks(range(0, 20000001, 3000000), range(0, 21, 3))
    utils.plt.ylabel("Scheduling latency  (sec)")
    utils.plt.xlabel("Google trace 200x speedup")
    str_ylabels = []
    for y_tick in ax.get_yticks():
        str_ylabels.append(str(int(y_tick)))
    ax.set_yticklabels(str_ylabels)
    utils.set_rcs()
    utils.prepare_legend(legend_loc="upper left", legend_ncol=2, bbox_to_anchor=(0.015, 1.19), frameOn=False)
    utils.plt.savefig("google_speedup_scheduling.pdf",
                format="pdf", bbox_inches="tight")


def main(argv):
    trace_paths = ['/home/pg1712/Development/memcached_bench/Python_plots/data/google_speedup/200x/YARN',
                   '/home/pg1712/Development/memcached_bench/Python_plots/data/google_speedup/200x/MEDEA'
                   ]
    speedups = ['200']
    delays = {}
    for trace_path in trace_paths:
        trace_delays = get_scheduling_delays(trace_path)
        if 'YARN' in trace_path:
            if 'YARN' in delays:
                delays['YARN'].append(trace_delays)
            else:
                delays['YARN'] = [trace_delays]
        elif 'MEDEA' in trace_path:
            if 'MEDEA' in delays:
                delays['MEDEA'].append(trace_delays)
            else:
                delays['MEDEA'] = [trace_delays]
        # elif 'relax' in trace_path:
        #     if 'relax' in delays:
        #         delays['relax'].append(trace_delays)
        #     else:
        #         delays['relax'] = [trace_delays]
        else:
            print 'Error: Unexpected algorithm'
            exit(1)


    # utils.plt.figure(figsize=(3.33, 2.22))
    utils.set_paper_rcs()


    delay_list = []
    labels = []
    colors = ['k']
    for speedup_index in range(0, len(speedups)):
        labels.append(str(speedups[speedup_index]) + 'x')
        for algo, speedup_delays in delays.items():
            delay_list.append(speedup_delays[speedup_index])
            if algo == 'YARN':
                colors.append('r')
            elif algo == 'MEDEA':
                colors.append('b')
            # elif algo == 'relax':
            #     colors.append('g')
            else:
                print 'Error: unknown algorithm ', algo
    print len(delay_list)
    print labels
    print colors
    # plt.legend(loc='lower right', frameon=False, handlelength=1.5,
    #            handletextpad=0.1, numpoints=1)
    plot_scheduling_delays(delay_list, labels, colors)


if __name__ == '__main__':
  main(sys.argv)