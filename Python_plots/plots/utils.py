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
import matplotlib.font_manager as fnt
import numpy as np
import brewer2mpl

# brewer2mpl.get_map args: set name  set type  number of colors
bmapSpectral = brewer2mpl.get_map('RdYlBu', 'Diverging', 4)
colorMap = bmapSpectral.hex_colors


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
paper_figsize_bigsim3 = (2.4, 1.7)
paper_figsize_default = (3.33,2.22)

def set_paper_rcs():
  rc('font', family='serif', size=9)
  rc('text.latex', preamble=['\usepackage{times,mathptmx}'])
  rc('text', usetex=True)
  rc('legend', fontsize=8)
  rc('figure', paper_figsize_default)
#  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  #   rc('axes', linewidth=0.2)
  rc('lines', linewidth=0.5)


def set_rcs( ):
    if paperMode:
        set_paper_rcs()

    # if paperMode:
    #     # rcParams dict
    #     rcParams['font.size'] = paper_textsize
    #     rcParams['axes.labelsize']  = paper_textsize
    #     rcParams['xtick.labelsize'] = paper_textsize
    #     rcParams['ytick.labelsize'] = paper_textsize
    #     rcParams['legend.fontsize'] = paper_textsize
    #     rcParams['font.family'] = 'serif'
    #     rcParams['font.serif'] = ['Computer Modern Roman']
    #     rcParams['text.usetex'] = True
    #
    #     # Single plot
    #     if figureStyle == 1:
    #         rcParams['figure.figsize'] = 4, 2
    #     # Multi boxplot
    #     elif figureStyle == 2:
    #         rcParams['figure.figsize'] = 6, 4
    #         rcParams['axes.labelsize']  = paper_textsize+5
    #         rcParams['xtick.labelsize'] = paper_textsize
    #         rcParams['ytick.labelsize'] = paper_textsize+5
    #         rcParams['legend.fontsize'] = paper_textsize
    #     # CDFs
    #     elif figureStyle == 3:
    #         rcParams['figure.figsize'] = 5,  3
    #         rcParams['font.size'] = paper_textsize+15
    #         rcParams['axes.labelsize']  = paper_textsize+15
    #         rcParams['xtick.labelsize'] = paper_textsize+10
    #         rcParams['ytick.labelsize'] = paper_textsize+10
    #         rcParams['legend.fontsize'] = paper_textsize+5
    #
    #     if not isboxPlot:
    #         plt.grid(True, which='both', alpha=0.3)
    # # else:
    # #     textsize = 34
    # #     rc('axes', linewidth=0.5)
    # #     rc('lines', linewidth=1)
    # #
    # #     if not isboxPlot:
    # #         plt.rcParams['font.size'] = textsize
    # #         plt.rcParams['xtick.labelsize'] = textsize - 4
    # #         plt.rcParams['ytick.labelsize'] = textsize - 4
    # #         plt.gca().yaxis.grid(True, alpha=0.85)
    # #         plt.grid(True)
    # #     else:
    # #         plt.rcParams['font.size'] = textsize - 10
    # #         plt.rcParams['xtick.labelsize'] = textsize/2 -12
    # #         plt.rcParams['ytick.labelsize'] = textsize/2
    # #         plt.rc('axes',   labelsize=(textsize/2 -2))  # fontsize of the x any y labels
    # #         # plt.rc('font', size=SIZE)  # controls default text sizes
    # #         # plt.rc('axes', titlesize=SIZE)  # fontsize of the axes title
    # #         # plt.rc('axes', labelsize=SIZE)  # fontsize of the x any y labels
    # #         # plt.rc('xtick', labelsize=SIZE)  # fontsize of the tick labels
    # #         # plt.rc('ytick', labelsize=SIZE)  # fontsize of the tick labels
    # #         # plt.rc('legend', fontsize=SIZE)  # legend fontsize
    # #         # plt.rc('figure', titlesize=SIZE)  # # size of the figure title

    return


def plot_cdf(outname, ylabel):
    plt.ylim((0,1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlim((-1))
    plt.xlabel(ylabel)
    plt.ylabel("CDF")

    plt.grid(True, which='both', alpha=0.3)
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
    color_list = [colorMap[0], colorMap[1], colorMap[3], colorMap[2]]
    double_color_list = [colorMap[0], colorMap[0], colorMap[1], colorMap[1], colorMap[3],  colorMap[3], colorMap[2], colorMap[2]]
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
    fig.text(0.02, 0.5, "Request latency [ms]", va='center', rotation='vertical')
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
    i = 0
    for ax in axes:
        xaxis = ax.xaxis
        xaxis.set_ticks_position('none')
        yaxis = ax.yaxis
        yaxis.set_ticks_position('none')
        ax.set(xticklabels='')
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

    xaxis = ax2.xaxis
    xaxis.set_ticks_position('none')
    yaxis = ax2.yaxis
    yaxis.set_ticks_position('none')

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
    hA, = plt.plot([1, 1], colorMap[0], linewidth=0.8)
    hB, = plt.plot([1, 1], colorMap[1], linewidth=0.8)
    hC, = plt.plot([1, 1], colorMap[3], linewidth=0.8)
    hD, = plt.plot([1, 1], colorMap[2], linewidth=0.8)
    leg = plt.legend((hA, hB, hC, hD), (systems_compared),bbox_to_anchor=(1.2, 1.25), loc='upper right', ncol=2,
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