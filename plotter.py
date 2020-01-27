from matplotlib import pyplot as plt
import pickle as pk
import numpy as np
import misc
from matplotlib.lines import Line2D

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'Serif','Serif':['Palatino']})
rc('text', usetex=True)


def import_data(files):
    data = []
    for file in files:
        ds = pk.load(open(misc.wd() + file + "_data.pickle",'rb'))
        for d in ds:
            data.append(d)

    return data


def plot_mean(data):

    x = np.mean(np.array(data), axis=0)
    plt.plot(x)
    plt.xlabel("Timestep")
    plt.ylabel("Mean")
    plt.show()


def plot_multi_mean_nums(vars, data):

    ls = [None] * len(data)
    fig, ax = plt.subplots()
    for i in range(len(data)):
        d = data[i][0]
        y = np.mean(np.array(d), axis=0)
        x = np.linspace(0, vars["run_time"], int(vars["run_time"]/vars["timestep"]))
        st = str(vars["variables"][i])
        ls[i], = ax.plot(x, y, label = st)
        ax.set_xlabel("$t \; [s]$", fontsize=16)
        ax.set_ylabel("$\sigma_x \; [m]$", fontsize=16)

    plt.grid()
    if len(vars["variables"]) > 4:
        leg = ax.legend(title='\# of Boids', ncol=2)
    else:
        leg = ax.legend(title='\# of Boids', ncol=1)
    plt.xlim(0, int(vars["run_time"]))
    plt.ylim(bottom=0)
    plt.tight_layout()

    plt.show()

def plot_multi_mean_time(vars, data):

    ls = [None] * len(data)
    fig, ax = plt.subplots()

    for i in range(len(data)):
        d = data[i][0]          # The 0 index is for STD in x
        y = np.mean(np.array(d), axis=0)
        x = np.linspace(0, vars["run_time"], len(y))
        st = str(vars["variables"][i])
        ls[i], = ax.plot(x, y, label = st)
        ax.set_xlabel("$t \; [s]$", fontsize=16)
        ax.set_ylabel("$\sigma_x \; [m]$", fontsize=16)

    plt.grid()
    if len(vars["variables"]) > 4:
        leg = ax.legend(title='Timestep', ncol=2)
    else:
        leg = ax.legend(title='Timestep', ncol=1)
    plt.xlim(0,int(vars["run_time"]))
    plt.tight_layout()

    plt.show()

def plot_multi_velocity(vars, data):

    ls = [None] * len(data)
    fig, ax = plt.subplots()

    for i in range(len(data)):
        d = data[i][1]  # The 0 index is for STD in x
        y = np.mean(np.array(d), axis=0)
        x = np.linspace(0, vars["run_time"], len(y))
        st = str(vars["variables"][i])
        ls[i], = ax.plot(x, y, label=st)
        ax.set_xlabel("$t \; [s]$", fontsize=16)
        ax.set_ylabel("$\sigma_x \; [m]$", fontsize=16)

    plt.grid()
    if len(vars["variables"]) > 4:
        leg = ax.legend(title='Timestep', ncol=2)
    else:
        leg = ax.legend(title='Timestep', ncol=1)
    plt.xlim(0, int(vars["run_time"]))
    plt.tight_layout()

    plt.show()
