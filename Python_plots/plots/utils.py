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

from matplotlib import use, rc, rcParams
use('Agg')
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import brewer2mpl

# brewer2mpl.get_map args: set name  set type  number of colors
bmap = brewer2mpl.get_map('Paired', 'Qualitative', 4)
colorMap = bmap.hex_colors


paperMode = True


# Reject values based on the variance of the mean
def reject_double_outliers(latency_data, throughput_data, m=3):
    throughput_data = throughput_data[abs(latency_data - np.mean(latency_data)) < m * np.std(latency_data)]
    latency_data  = latency_data[abs(latency_data - np.mean(latency_data)) < m * np.std(latency_data)]
    return latency_data, throughput_data

# Reject values based on the variance of the mean
def reject_outliers(data, m=3):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


# plot saving utility function
def writeout(filename_base, tight=True):
  for fmt in ['pdf']:
    if tight:
        plt.savefig("%s.%s" % (filename_base, fmt), format=fmt, bbox_inches='tight', pad_inches=0.01)
    else:
        plt.savefig("%s.%s" % (filename_base, fmt), format=fmt)


def set_leg_fontsize(size):
    rc('legend', fontsize=size)


def prepare_legend(legend_loc=1, legend_ncol=1, alpha_num=0.8, bbox_to_anchor=None, frameOn=True):
    rc('legend', frameon=frameOn)
    # legfont = fnt.FontProperties()
    # legfont.set_size(legend_font)
    # leg = plt.legend(loc=legend_loc, ncol=legend_ncol, fancybox=True, prop=legfont)
    if bbox_to_anchor is not None:
        leg = plt.legend(loc=legend_loc, ncol=legend_ncol, fancybox=True, bbox_to_anchor=bbox_to_anchor)
    else:
        leg = plt.legend(loc=legend_loc, ncol=legend_ncol, fancybox=True)
    leg.get_frame().set_alpha(alpha_num)
    # leg.get_frame().set_linewidth(0.1)
    return


paper_figsize_small = (1.1, 1.1)
paper_figsize_small_square = (1.5, 1.5)
paper_figsize_medium = (2, 1.33)
paper_figsize_medium_square = (2, 2)
#paper_figsize_medium = (1.66, 1.1)
paper_figsize_large = (3, 2)
paper_figsize_storm_cdf = (2.2, 1.22) # font=6, 5
paper_figsize_latency_boxplot = (3.33, 2.22)  # 12, 6
paper_figsize_logscale = (3.33, 2)  # 8, 6
paper_figsize_microexp_bars = (3.33, 2)  # 8, 6
paper_figsize_throughput_bars = (3.33, 2.22)  # 11, 6
paper_figsize_default = (3.33, 2.22)  # 11, 6

def set_paper_rcs():
  rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
  rc('font', size=12)
  rc('text', usetex=True)
  # rc('text.latex', preamble=['\usepackage{mathptmx,sans-serif}'])
  rc('legend', fontsize=6)
  rc('figure', figsize=paper_figsize_default)
#  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  #   rc('axes', linewidth=0.2)
  rc('lines', linewidth=0.5)


def set_rcs( ):
    if paperMode:
        set_paper_rcs()
    return


def plot_cdf(outname, ylabel):
    plt.ylim((0,1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlim((-1))
    plt.xlabel(ylabel, labelpad=2)
    plt.ylabel("CDF", labelpad=2)
    # plt.grid(True, which='both', alpha=0.3)
    prepare_legend(legend_loc=4, alpha_num=0.5)

    writeout("%s"%outname)
    # plt.show()
    plt.clf()


def plot_scatter(outname, workloads, latency_data, throughput_data, systems_compared):
    scatter_colors = ['r', 'g', 'b', 'c', 'm']
    scatter_markets = ['v', 'x', 'o', '*']

    # Global style configuration
    set_rcs()

    for name in workloads:

        plt.xlabel("Latency 99th percentile [ms]", fontsize=matplotlib.rcParams['font.size'])
        plt.ylabel("Throughput [Kops/s]", fontsize=matplotlib.rcParams['font.size'])
        props = dict(alpha=0.5, edgecolors='none')

        # print "Latency Len: " + str(len(latency_data[name]['YARN']))
        # print "Throughput len: "+ str(len(throughput_data[name]['YARN']))

        i = 0
        handles = []
        for item in systems_compared:
            # s = np.random.randint(50,200)
            plt.scatter(latency_data[name][item], throughput_data[name][item], marker=scatter_markets[i],
                                       color=scatter_colors[i], s=50, label=item, **props)
            # ax1.scatter(latency_data["A"][item],throughput_data["A"][item], color=colors[i], s=5,edgecolor='none')
            # ax1.set_aspect(1./ax1.get_data_ratio()) # make axes square
            i += 1
        # axes
        axes = plt.gca()
        ymin, ymax = axes.get_ylim()
        xmin, xman = axes.get_xlim()
        plt.ylim(0,ymax)
        plt.xlim(0,xman)
        #Convert y Values using K instead
        locs, labels = plt.yticks()
        tick_labels = []
        for tick in locs:
            if (int(tick)/1000) > 0 or (float(tick)/1000) == 0:
                tick_labels.append(str(int(tick)/1000)) # + "K")
            else:
                tick_labels.append(str(float(tick) / 1000))  # + "K")
        plt.yticks(locs, tick_labels)

        # Global style configuration
        set_rcs()
        prepare_legend(legend_loc=1)

        writeout("%s"%(outname+"_w"+name))
        print "Done with Writing to file"
        plt.clf()


def color_box(bp):
    color_list = [colorMap[3], colorMap[2], colorMap[1], colorMap[0]]
    double_color_list = [colorMap[3], colorMap[3], colorMap[2], colorMap[2], colorMap[1],  colorMap[1], colorMap[0], colorMap[0],]
    # Define the elements to color. You can also add medians, fliers and means
    elements = ['boxes','caps','whiskers']
    # Iterate over each of the elements changing the color
    for elem in elements:
        i = 0
        for idx in xrange(len(bp[elem])):
            if elem == 'boxes':
                plt.setp(bp[elem][idx], color=color_list[i])
            else:
                plt.setp(bp[elem][idx], color=double_color_list[i])
            i += 1
    return


def plot_multiboxplot(data, outname, workloads, systems_compared, systems_labels):
    fig, axes = plt.subplots(ncols=len(workloads)+1, sharey=True)
    fig.subplots_adjust(wspace=0)
    # fig.text(0.5, 0.04, "YCSB Workloads", ha='center')
    fig.text(-0.02, 0.5, "Request latency [ms]", va='center', rotation='vertical')
    for ax, name in zip(axes, workloads):
        # whis from 5th to 99th precentile
        bp = ax.boxplot(x=[data[name][item] for item in systems_compared], whis=[5, 99], sym=" ")
        # ax.set_yscale('log')
        plt.setp(bp['boxes'], linewidth=0.6)
        plt.setp(bp['medians'], linewidth=0.6)
        plt.setp(bp['whiskers'], linewidth=0.7)
        color_box(bp)
        xtickNames = ax.set(xticklabels='')
        # plt.setp(xtickNames, rotation=90, fontsize=textsize/2)
        workloadXtick = ax.set(xlabel=name)
        plt.setp(workloadXtick)
        # # Add a horizontal grid to the plot, but make it very light in color
        # # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
        # Hide these grid behind plot objects
        ax.set_axisbelow(True)
        ax.margins(0.05) # Optional
        # ax.set_ylim(0, 250)
    i = 0
    for ax in axes:
        xaxis = ax.xaxis
        xaxis.set_ticks_position('none')
        yaxis = ax.yaxis
        yaxis.set_ticks_position('none')
        ax.set(xticklabels='')
        str_ylabels = []
        for y_tick in ax.get_yticks():
            str_ylabels.append(str(int(y_tick)))
        ax.set_yticklabels(str_ylabels)
        # if i == len(workloads):
        #     # ax.yaxis.set_tick_params(direction='in')
        #     ax.get_yaxis().set_tick_params(direction='out', color='white')
        i += 1
    # WorkloadE on a separate plot ?
    # now, the second axes that shares the x-axis with the ax1
    ax2 = fig.add_subplot(1, 8, 8)
    bp = ax2.boxplot(x=[data["E"][item] for item in systems_compared], whis=[5, 99], sym=" ")
    # ax2.set_yscale('log')
    plt.setp(bp['boxes'], linewidth=0.6)
    plt.setp(bp['medians'], linewidth=0.6)
    plt.setp(bp['whiskers'], linewidth=0.7)
    color_box(bp)
    ax2.set(xticklabels='')
    workloadXtick = ax2.set(xlabel='E')
    plt.setp(workloadXtick)
    ax2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    # Hide these grid behind plot objects
    ax2.set_axisbelow(True)
    ax2.margins(0.05)  # Optional
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    # ax2.set_ylim(0, 300)

    xaxis = ax2.xaxis
    xaxis.set_ticks_position('none')
    yaxis = ax2.yaxis
    yaxis.set_ticks_position('none')
    str_ylabels = []
    for y_tick in ax2.get_yticks():
        str_ylabels.append(str(int(y_tick)))
    ax2.set_yticklabels(str_ylabels)

    # plt.ylim((0,50))
    # plt.xlim((-1,100))
    # plt.legend(loc=4, frameon=True, handlelength=2.5, handletextpad=0.2)
    # axes
    # axes = plt.gca()
    # ymin, ymax = axes.get_ylim()
    # plt.ylim(0, ymax-100)
    # draw temporary red and blue lines and use them to create a legend
    rc('legend', frameon=True)
    # legfont = fnt.FontProperties()
    # legfont.set_size('xx-small')
    hA, = plt.plot([1, 1], colorMap[3], linewidth=0.8)
    hB, = plt.plot([1, 1], colorMap[2], linewidth=0.8)
    hC, = plt.plot([1, 1], colorMap[1], linewidth=0.8)
    hD, = plt.plot([1, 1], colorMap[0], linewidth=0.8)
    leg = plt.legend((hA, hB, hC, hD), (systems_compared),bbox_to_anchor=(2.0, 1.15), loc='upper right', ncol=4,
                     fancybox=True)
    leg.get_frame().set_alpha(0.0)
    hA.set_visible(False)
    hB.set_visible(False)
    hC.set_visible(False)
    hD.set_visible(False)

    # Global style configuration
    set_rcs()
    # plt.rcParams['axes.linewidth'] = 5  # set the value globally
    print "Done with plots"
    writeout("%s"%outname)
    print "Done with Writing to file"


def plot_boxplot(data, outname, systems_compared, systems_labels):
    fig, axes = plt.subplots(ncols=1, sharey=True)
    fig.subplots_adjust(wspace=0)
    fig.text(0.01, 0.5, "Request latency [ms]", va='center', rotation='vertical')
    # for ax, name in zip(axes, workloads):
    # whis from 5th to 99th precentile
    bt = axes.boxplot(x=[data[item] for item in systems_compared], whis=[5, 99], sym="+")
    # plt.setp(bt['fliers'], color='red', marker='+')
    xtickNames = axes.set(xticklabels=systems_labels)
    plt.setp(xtickNames, rotation=0, fontsize=matplotlib.rcParams['font.size'])

    # # Add a horizontal grid to the plot, but make it very light in color
    # # so we can use it for reading data values but not be distracting
    axes.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                    alpha=1)
    # Hide these grid behind plot objects
    axes.set_axisbelow(True)
    axes.margins(0.05)  # Optional
    # Global style configuration
    set_rcs()
    print "Done with plots"
    writeout("%s"%outname)
    print "Done with Writing to file"