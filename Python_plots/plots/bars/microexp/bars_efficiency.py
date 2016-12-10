from matplotlib import use, rc
use('Agg')
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import pandas as pd
import plots.utils as utils

files = ["CPLEX-off_stats.csv", "CPLEX-on_stats.csv", "GR-NODE_CAND_stats.csv", "GR-SERIAL_stats.csv", "GR-RANDOM_stats.csv"]
labels = ["ILP-offline", "ILP-online", "Node Candidates", "Random"]
labels_map={"CPLEX-on": "ILP-online", "CPLEX-off": "ILP-offline",
            "GR-NODE_CAND": "Node Candidates", "GR-RANDOM": "Greedy"}

hatch_patterns = ["", "/", "\\", "x", ".", "o", "O"]
cluster_size = 100

# Global style configuration
utils.set_rcs()


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
    plt.plot(x, y, linestyle='--', linewidth=1.5, color='red')
    plt.show()


def grouped_bar(data):
    # ax = sns.barplot(
    #     x='  totJobs', y='  ObjectiveValue ', hue='  Plan technique',
    #     #order=["fixed", "reactive", "predictive"],
    #     # hue_order=["oracle", "bayesian"],
    #     data=data)
    fig = plt.figure()
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
        pos = [j - (1 - space) / 2. + i * width for j in range(1, len(categories) + 1)]
        if labels_map.has_key(str(cond).strip()):
            ax.bar(pos, y_vals, width=width, label=labels_map[str(cond).strip()], color=get_colors()[i],
                   edgecolor=get_colors()[i+1],hatch=hatch_patterns[i])
            i +=1

    indexes = range(1, len(categories) + 1)
    print "Indexes: ", indexes
    print "Categories: ", categories
    ax.set_xticks(indexes)
    ax.set_xticklabels(["10\%", "20\%", "30\%", "40\%", "50\%", "60\%", "70\%", "80\%", "90\%", "100\%"])
    plt.setp(plt.xticks()[1], rotation=90)

    # Add the axis labels
    ax.set_ylabel("Placement Efficiency")
    ax.set_xlabel("Services Percentage")

    # Show the 50% mark, which would indicate an equal
    # ax.hlines(19.5, -0.5, 5.5, linestyle='--', linewidth=1)
    optimal_line_graph('100*( x*8 ) + '+str(cluster_size) + '+ 100', range(0, len(categories) + 1))

    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    plt.tight_layout()

    return fig, ax


def file_parser(fnames):
    file_data = (pd.read_csv(f) for f in fnames)
    all_data = pd.concat(file_data, ignore_index=True)
    # grouped_data = all_data.groupby(['  Plan technique', '  totJobs'])['  ObjectiveValue '].mean()
    # # print all_data.columns.values
    # print grouped_data
    numpyMatrix = all_data[['  Plan technique', '  totJobs','  ObjectiveValue ']].values
    # print numpyMatrix
    return numpyMatrix


if __name__ == '__main__':

    print "Sytem Path {}".format(os.environ['PATH'])

    if len(sys.argv) < 2:
        print "Usage: bars_efficiency.py.py <input PATH>"
        sys.exit(-1)

    outname = "placement_efficiency_bars"

    fpaths = []
    for file in files:
      fpaths.append(sys.argv[1]+"/"+file)
      # labels.append(sys.argv[2 + i])

    print 'Files given: {}'.format(" | ".join(fname for fname in fpaths))
    # print 'Labels given: {}'.format(" | ".join(label for label in labels))

    data = file_parser(fpaths)
    fig, axes = grouped_bar(data)
    utils.set_rcs()
    utils.prepare_legend(legend_loc="upper left", legend_font=16)
    utils.writeout("%s"%outname)