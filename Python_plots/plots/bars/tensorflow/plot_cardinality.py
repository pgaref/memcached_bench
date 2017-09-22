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

files = ["no_load.csv", "load_70.csv"]
labels = ["Tensorflow (isolated)", "Tensorflow (with background)"]
labels_map={"Tensorflow (isolated)": "no_load.csv", "Tensorflow (with background)": "load_70.csv"}

hatch_patterns = ["", "/", "\\", "x", ".", "o", "O"]

# Global style configuration
# utils.set_rcs()


def get_colors():
    return np.array([
        [0.1, 0.1, 0.1],          # black
        [0.4, 0.4, 0.4],          # very dark gray
        [0.7, 0.7, 0.7],          # dark gray
        [0.9, 0.9, 0.9],          # light gray
        [0.984375, 0.7265625, 0], # dark yellow
        [1, 1, 0.9]               # light yellow
    ])


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


def optimal_line_graph(formula, x_range):
    x = np.array(x_range)
    y = eval(formula)
    utils.plt.plot(x, y, linestyle='--', linewidth=1.5, color='red')
    utils.plt.show()


def grouped_bar(df):
    global labels
    fig = utils.plt.figure()
    ax = fig.add_subplot(111)

    space = 0.25
    # print df.keys()

    # n = len(conditions)
    n = len(labels)
    width = (1 - space) / n
    i = 0
    for cond in labels:
        x_vals = df[df['run'] == cond]['Cardinality'].values
        y_vals = df[df['run'] == cond][' Time(sec)'].values.astype(np.float)
        if labels_map.has_key(str(cond).strip()):
            ax.plot(x_vals, y_vals, label=cond, marker=utils.marker_list[i], color=utils.micro_color_list[i])
            i += 1

    indexes = np.arange(1, len(labels)+1, 1)
    print "Indexes: ", indexes
    print "Categories: ", labels
    # ax.set_xticks(indexes)
    # ax.set_xticklabels(x_vals)
    # utils.plt.setp(utils.plt.xticks()[1], rotation=00)
    ax.set_ylim(0)
    ax.set_xlim(0)

    # Make Y axis logscale
    # utils.plt.yscale('log', nonposy='clip')

    # Add the axis labels
    ax.set_ylabel("Tensorflow Runtime (sec)")
    ax.set_xlabel("Worker Cardinality")
    ax.grid(linestyle='--', axis='both')


    # optimal_line_graph('100*( x*8 ) + '+str(cluster_size) + '+ 100', range(0, len(categories) + 1))

    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    utils.plt.tight_layout()

    return fig, ax


def file_parser(fnames):
    file_data = (pd.read_csv(f) for f in fnames)
    all_data = pd.concat(file_data, keys=labels, names=['run','Cardinality' ' Time(sec)'])
    print all_data.columns.values
    all_data = all_data.reset_index()
    return all_data


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
        print "Usage: plot_cardinality.py <input PATH>"
        sys.exit(-1)

    outname = "tf_cardinalities"

    fpaths = []
    for file in files:
      fpaths.append(sys.argv[1]+"/"+file)
      # labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))
    # print 'Labels given: {}'.format(" | ".join(label for label in labels))

    data = file_parser(fpaths)
    fig, axes = grouped_bar(data)
    # utils.set_rcs()
    utils.prepare_legend(legend_loc="upper left", alpha_num=1.0, frameOn=True)
    utils.writeout("%s"%outname)