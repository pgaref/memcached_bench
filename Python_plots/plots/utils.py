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

from matplotlib import use, rc
use('Agg')
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fnt
import numpy as np


textsize = 34


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
            plt.savefig("%s.%s" % (filename_base, fmt), format=fmt, bbox_inches='tight')
        else:
            plt.savefig("%s.%s" % (filename_base, fmt), format=fmt)


def set_leg_fontsize(size):
    rc('legend', fontsize=size)


def prepare_legend(legend_loc=1, legend_ncol=1):
    rc('legend', frameon=True)
    legfont = fnt.FontProperties()
    legfont.set_size('small')
    leg = plt.legend(loc=legend_loc, ncol=legend_ncol, fancybox=True, prop=legfont)
    leg.get_frame().set_alpha(0.7)
    return


def set_rcs(use_seaborn=False, isboxPlot=False):
    if use_seaborn:
        plt.style.use('seaborn-white')
    rc('text', usetex=True)
    rc('font', **{'family': 'serif', 'serif': ['Helvetica'], 'size': textsize})

    # rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'], 'size': textsize})
    # rc('text.latex', preamble=r'\usepackage{cmbright}')

    rc('axes', linewidth=0.5)
    rc('lines', linewidth=1)

    if not isboxPlot:
        plt.rcParams['font.size'] = textsize
        plt.rcParams['xtick.labelsize'] = textsize - 4
        plt.rcParams['ytick.labelsize'] = textsize - 4
        plt.gca().yaxis.grid(True, alpha=0.85)
        plt.grid(True)
    else:
        plt.rcParams['font.size'] = textsize - 10
        plt.rcParams['xtick.labelsize'] = textsize/2 -12
        plt.rcParams['ytick.labelsize'] = textsize/2
        plt.rc('axes',   labelsize=(textsize/2 -2))  # fontsize of the x any y labels

        # plt.rc('font', size=SIZE)  # controls default text sizes
        # plt.rc('axes', titlesize=SIZE)  # fontsize of the axes title
        # plt.rc('axes', labelsize=SIZE)  # fontsize of the x any y labels
        # plt.rc('xtick', labelsize=SIZE)  # fontsize of the tick labels
        # plt.rc('ytick', labelsize=SIZE)  # fontsize of the tick labels
        # plt.rc('legend', fontsize=SIZE)  # legend fontsize
        # plt.rc('figure', titlesize=SIZE)  # # size of the figure title

    return


def plot_cdf(outname, ylabel):
    plt.ylim((0,1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlim((-1))
    plt.xlabel(ylabel, fontsize=matplotlib.rcParams['font.size'])
    plt.ylabel("CDF", fontsize=matplotlib.rcParams['font.size'])

    # Global style configuration
    set_rcs()
    prepare_legend(legend_loc=4)

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


def plot_multiboxplot(data, outname, workloads, systems_compared, systems_labels):
    fig, axes = plt.subplots(ncols=len(workloads), sharey=True)
    fig.subplots_adjust(wspace=0)
    # fig.text(0.5, 0.04, "YCSB Workloads", ha='center')
    fig.text(0.04, 0.5, "Request latency [ms]", va='center', rotation='vertical',
             fontsize=matplotlib.rcParams['font.size']-4)

    for ax, name in zip(axes, workloads):
        # whis from 5th to 99th precentile
        ax.boxplot(x=[data[name][item] for item in systems_compared], whis=[5, 99], sym=" ")
        xtickNames = ax.set(xticklabels=systems_labels)
        plt.setp(xtickNames, rotation=90, fontsize=textsize/2)

        workloadXtick = ax.set(xlabel='workload'+name)
        plt.setp(workloadXtick)
        # # Add a horizontal grid to the plot, but make it very light in color
        # # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
        # Hide these grid behind plot objects
        ax.set_axisbelow(True)
        ax.margins(0.05) # Optional
    # plt.ylim((0,50))
    # plt.xlim((-1,100))
    # plt.legend(loc=4, frameon=True, handlelength=2.5, handletextpad=0.2)
    # axes
    axes = plt.gca()
    ymin, ymax = axes.get_ylim()
    plt.ylim(0, ymax-100)
    # Global style configuration
    set_rcs(isboxPlot=True)
    print "Done with plots"
    writeout("%s"%outname)
    print "Done with Writing to file"


def plot_boxplot(data, outname, systems_compared, systems_labels):
    fig, axes = plt.subplots(ncols=1, sharey=True)
    fig.subplots_adjust(wspace=0)
    fig.text(0.04, 0.5, "Cache request latency [ms]", va='center', rotation='vertical',
             fontsize=matplotlib.rcParams['font.size']-4)
    # for ax, name in zip(axes, workloads):
    # whis from 5th to 99th precentile
    bt = axes.boxplot(x=[data[item] for item in systems_compared], whis=[5, 99], sym="+")
    # plt.setp(bt['fliers'], color='red', marker='+')
    xtickNames = axes.set(xticklabels=systems_labels)
    plt.setp(xtickNames, rotation=90, fontsize=textsize/2)

    # # Add a horizontal grid to the plot, but make it very light in color
    # # so we can use it for reading data values but not be distracting
    axes.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                    alpha=1)
    # Hide these grid behind plot objects
    axes.set_axisbelow(True)
    axes.margins(0.05)  # Optional
    print "Done with plots"
    writeout("%s"%outname)
    print "Done with Writing to file"