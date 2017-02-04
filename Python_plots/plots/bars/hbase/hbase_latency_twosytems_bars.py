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
import plots.utils as utils
import brewer2mpl

# brewer2mpl.get_map args: set name  set type  number of colors
# bmap = brewer2mpl.get_map('RdBu', 'Diverging', 5)
bmap = brewer2mpl.get_map('Paired', 'Qualitative', 5)
colors = bmap.hex_colors
colors[4] = colors[3]
colors[3] = colors[1]

# ALL workloads
workloads = ["A", "B", "C", "D", "E", "F"]
systems_compared = ["YARN", "MEDEA"]

# Global style configuration
hatch_patterns = ["", "\\"]
utils.set_rcs()



def get_colors():
    return colors


def color_bars(axes, colors):
    i = 0
    # These are the patches (matplotlib's terminology
    # for the rectangles corresponding to the bars)
    for p in axes.patches:
        # Pull out the dark and light colors for
        # the current subplot
        dark_color = colors[i % len(labels)]
        light_color = colors[(i + 1) % len(labels)]
        # The first bar gets the dark color
        # p1.set_color(dark_color)

        # The second bar gets the light color, plus
        # hatch marks int he dark color
        p.set_color(light_color)
        p.set_edgecolor(dark_color)
        p.set_hatch(hatch_patterns[i % len(labels)])
        i += 1


def percentage(part, whole):
  return 100 * float(part)/float(whole)


# def optimal_line_graph(formula, x_range):
#     x = np.array(x_range)
#     y = eval(formula)
#     utils.plt.plot(x, y, linestyle='--', linewidth=1.5, color='red')
#     utils.plt.show()

def grouped_bar(data):
    # ax = sns.barplot(
    #     x='  totJobs', y='  ObjectiveValue ', hue='  Plan technique',
    #     #order=["fixed", "reactive", "predictive"],
    #     # hue_order=["oracle", "bayesian"],
    #     data=data)
    fig = utils.plt.figure()
    ax = fig.add_subplot(111)

    space = 0.2

    conditions = np.unique(systems_compared)
    categories = np.unique(workloads)
    # n = len(conditions)
    n = len(systems_compared)

    width = (1 - space) / n
    print "width:", width

    i = 0
    for cond in systems_compared:
        y_vals = data_map[cond]
        pos = [j - (1 - space) / 2. + i * width for j in range(1, len(categories) + 1)]
        ax.bar(pos, y_vals, width=width, label=cond, color=get_colors()[len(colors)-i-1], hatch=hatch_patterns[i])
        i += 1

    indexes = np.arange(1, len(categories) + 1, 1)
    print "Indexes: ", indexes
    print "Categories: ", categories
    ax.set_xticks(indexes)
    ax.set_xticklabels(workloads)
    utils.plt.setp(utils.plt.xticks()[1], rotation=00)
    ax.set_xlim(0, len(indexes)+1)

    # Add the axis labels
    ax.set_ylabel("Latench [ms]")
    ax.set_xlabel("YCSB Workload")

    # optimal_line_graph('100*( x*8 ) + '+str(cluster_size) + '+ 100', range(0, len(categories) + 1))

    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    utils.plt.tight_layout()

    return fig, ax


data_map = {}
def file_parser(fnames, label):
    for f, l  in zip(fnames, labels):
        # print "Analyzing %s:" % (f)
        for line in open(f).readlines():
            fields = [x.strip() for x in line.split(",")]
            if len(fields) > 2 and fields[1] == 'Average' and fields[0] == '[READ]':
                print 'Label:', l, 'Latency: ', int(float(fields[2])/1000)
                if l not in data_map:
                    data_map[l] = []
                data_map[l].append(int(float(fields[2])/1000))
                break
            elif len(fields) > 2 and fields[1] == 'Average' and fields[0] == '[SCAN]':
                print 'Label:', l, 'Latency: ', int(float(fields[2])/1000)
                if l not in data_map:
                    data_map[l] = []
                data_map[l].append(int(float(fields[2])/1000))
                break

if __name__ == '__main__':

    print "System Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
      print "Usage: hbase_latency_twosystems_bars.py <input PATH 1> <label 1> ... " \
          "<input  PATH n> <label n> [output file]"

    if (len(sys.argv) - 1) % 2 != 0:
      outname = sys.argv[-1]
    else:
      outname = "hbase_latency_bars"

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
            fnames.append(path + "write-w"+workload+"-10R-sum.dat")
        print "Processing.. "+ str(fnames)
        file_parser(fnames, labels)
    grouped_bar(data_map)

    utils.set_rcs()
    utils.prepare_legend(legend_loc="upper right", alpha_num=0.8, legend_ncol=2,  bbox_to_anchor=(0.80, 1.16), frameOn=False)
    utils.writeout("%s" % outname)