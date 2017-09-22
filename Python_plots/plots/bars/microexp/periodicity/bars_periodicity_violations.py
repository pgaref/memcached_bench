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

files = ["ILP-on_stats.csv", "GR-NODE_CAND_CACHED_stats.csv", "GR-NODE_CAND_CACHED_LB_stats.csv", "GR-SERIAL_stats.csv", "GR-APP_C_TAG_L_stats.csv", "KUBE_stats.csv"]
labels = ["ILP", "Node Candidates", "Node Candidates LB", "Serial", "Popular Tags", "Kubernetes"]
labels_map={"ILP-on": "ILP", "GR-NODE_CAND_CACHED": "Node Candidates", "GR-NODE_CAND_CACHED_LB": "Node Candidates LB",
            "GR-SERIAL": "Serial",  "GR-APP_C_TAG_L": "Popular Tags","KUBE": "Kubernetes"}

# Global style configuration
# utils.set_rcs()



def color_bars(axes, colors):
    i = 0
    # These are the patches (matplotlib's terminology
    # for the rectangles corresponding to the bars)
    for p in axes.patches:
        # Pull out the dark and light colors for
        # the current subplot
        dark_color = colors[i % len(files)]
        light_color = colors[(i + 1) % len(files)]
        # The first bar gets the dark color
        # p1.set_color(dark_color)

        # The second bar gets the light color, plus
        # hatch marks int he dark color
        p.set_color(light_color)
        p.set_edgecolor(dark_color)
        p.set_hatch(utils.hatch_patterns[i % len(files)])
        i += 1

def optimal_line_graph(formula, x_range):
    x = np.array(x_range)
    y = eval(formula)
    utils.plt.plot(x, y, linestyle='--', linewidth=1.5, color='red')
    utils.plt.show()


def grouped_bar(data):
    # ax = sns.barplot(
    #     x='  totJobs', y='  ObjectiveValue ', hue='  Plan technique',
    #     #order=["fixed", "reactive", "predictive"],
    #     # hue_order=["oracle", "bayesian"],
    #     data=data)
    fig = utils.plt.figure()
    ax = fig.add_subplot(111)

    space = 0.2

    condition_indexes = np.unique(data[:, 0], return_index=True)[1]
    conditions = [data[:, 0][index] for index in sorted(condition_indexes)]
    categories = np.unique(data[:, 14])


    print conditions
    print categories

    # n = len(conditions)
    n = len(labels_map)

    width = (1 - space) / n
    print "width:", width

    i = 0
    for cond in conditions:
        print cond
        y_vals = data[data[:, 0] == cond][:, 16].astype(np.float) / data[data[:, 0] == cond][:, 3].astype(np.float) *100
        print y_vals
        pos = [j - (1 - space) / 2. + i * width for j in range(1, len(categories) + 1)]
        if labels_map.has_key(str(cond).strip()):
            ax.bar(pos, y_vals, width=width, label=labels_map[str(cond).strip()], color=utils.get_bw_colors()[i],
                   hatch=utils.hatch_patterns[i], edgecolor='black', linewidth=0.05)
            ax.plot(pos, y_vals, color='black', marker=utils.marker_list[i], linestyle='--', linewidth=0.6)
            i +=1

    indexes = np.arange(1, len(categories)+1, 1)
    print "Indexes: ", indexes
    print "Categories: ", categories
    # ax.set_xticks(indexes)
    # ax.set_xticklabels(["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])
    utils.plt.setp(utils.plt.xticks()[1], rotation=00)
    ax.set_ylim(0,50)
    # ax.set_xlim(0.3,9.5)

    # Add the axis labels
    ax.set_ylabel("Constraint violations (%) \n Soft:{} Period:{} Complexity:{}".format(np.unique(data[:, 13])[0].strip(),
                                                                                      np.unique(data[:, 14])[0],
                                                                                      np.unique(data[:, 15])[0]), labelpad=2)
    ax.set_xlabel("Periodicity \n Nodes: {} Racks: {}".format(np.unique(data[:, 8])[0], np.unique(data[:, 7])[0]), labelpad=2)

    str_ylabels = []
    for y_tick in ax.get_yticks():
        str_ylabels.append(str(int(y_tick)))
    ax.set_yticklabels(str_ylabels)



    # optimal_line_graph('100*( x*8 ) + '+str(cluster_size) + '+ 100', range(0, len(categories) + 1))

    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    utils.plt.tight_layout()

    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(0.1)

    return fig, ax


def file_parser(fnames):
    file_data = (pd.read_csv(f) for f in fnames)
    all_data = pd.concat(file_data, ignore_index=True)
    # grouped_data = all_data.groupby(['  Plan technique', '  totJobs'])['  ObjectiveValue '].mean()
    print all_data.columns.values
    # print grouped_data
    numpyMatrix = all_data[['    PlannerAlgorithm', '  Runtime(ms)', '  LRAs', '  LraRRs',
                            '  TagsAvg', '  AcceptedLRAs', '  AcceptedRRs', '  Racks', '  Nodes',
                            '  NodesMem(GB)', '  AllocatedMem(GB)', '  NodesMemUtil(%)',
                            '  LraSuccess(%)', '  Soft', '  Period', '  Complexity', '  Violations',
                            '  FragmentedNodes(%)', '  LeastLoadedNode(%)', '  LoadImbalance(stdev)',
                            '  CWeight', '  RWeight', '  LWeight', '  ObjectiveValue ']].values
    return numpyMatrix


if __name__ == '__main__':

    print "System Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
        print "Usage: bars_complexity_violations.py <input PATH>"
        sys.exit(-1)

    outname = "periodicity_violations"

    fpaths = []
    for file in files:
      fpaths.append(sys.argv[1]+"/"+file)
      # labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))
    # print 'Labels given: {}'.format(" | ".join(label for label in labels))

    data = file_parser(fpaths)
    fig, axes = grouped_bar(data)
    # utils.set_rcs()
    utils.prepare_legend(legend_loc="upper right", legend_ncol=2,  frameOn=False)
    utils.writeout("%s"%outname)