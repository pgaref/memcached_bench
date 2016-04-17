__author__ = 'pg1712'

from matplotlib import use, rc

use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# plot saving utility function
def writeout(filename_base, tight=True):
    for fmt in ['pdf']:
        if tight:
            plt.savefig("%s.%s" % (filename_base, fmt), format=fmt, bbox_inches='tight')
        else:
            plt.savefig("%s.%s" % (filename_base, fmt), format=fmt)


def set_leg_fontsize(size):
    rc('legend', fontsize=size)


def set_paper_rcs():
    rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'],
                  'serif': ['Helvetica'], 'size': 9})
    rc('text', usetex=True)
    rc('legend', fontsize=8)
#    rc('figure', figsize=(3.33, 2.22))
    rc('figure', figsize=(5.55, 4.44))
    #  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
    rc('axes', linewidth=0.5)
    rc('lines', linewidth=0.5)


def set_rcs():
    rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'],
                  'serif': ['Times'], 'size': 12})
    rc('text', usetex=True)
    rc('legend', fontsize=7)
    rc('figure', figsize=(6, 4))
    rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
    rc('axes', linewidth=0.5)
    rc('lines', linewidth=0.5)


def append_or_create(d, i, e):
    if not i in d:
        d[i] = [e]
    else:
        d[i].append(e)


def add_or_create(d, i, e):
    if not i in d:
        d[i] = e
    else:
        d[i] = d[i] + e


# event log constants
RESOURCE_UTILIZATION_SAMPLE = 0
TX_SUCCEEDED = 1
TX_FAILED = 2
COLLECTION_ENDING = 3
VMS_CHANGED_STATE = 4
SCHEDULING_OUTCOME = 5
COLLECTION_SUBMITTED = 6
SCHEDULING_TIME = 7
ZOMBIE_COLLECTION_DROPPED = 8
OVERLAP_COLLECTION_DROPPED = 9
COLLECTION_TRUNCATED = 10
CELL_STATE_SETUP = 11
END_ONLY_ENDS = 12

ARRIVAL_SAMPLE = 100
LEAVING_SAMPLE = 101
RES_LIMIT_SAMPLE = 102
ACTIVE_SAMPLE = 103
COLLECTION_ARRIVING_EVENT = 104
COLLECTION_LEAVING_EVENT = 105

MAPREDUCE_PREDICTION = 200
MAPREDUCE_ORIGINAL_RUNTIME = 201
MAPREDUCE_RESOURCE_ADJUSTMENT = 202
MAPREDUCE_BASE_RUNTIME = 203

paper_figsize_small = (1.1, 1.1)
paper_figsize_small_square = (1.5, 1.5)
paper_figsize_medium = (2, 1.33)
paper_figsize_medium_square = (2, 2)
# paper_figsize_medium = (1.66, 1.1)
paper_figsize_large = (3.33, 2.22)
paper_figsize_bigsim3 = (2.4, 1.7)

# 8e053b red
# 496ee2 blue
# ef9708 orange
paper_colors = ['#496ee2', '#8e053b', 'g', '#ef9708', '0', '#eeefff', '0.5', 'c', '0.7']


# -----------------------------------

def think_time_fn(x, y, s):
    return x + y * s


# -----------------------------------

def get_mad(median, data):
    devs = [abs(x - median) for x in data]
    mad = np.median(devs)
    return mad


# -----------------------------------

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func

    return decorate
