from matplotlib import pyplot as plt
import pickle as pk
import numpy as np
import misc
from matplotlib.lines import Line2D
#
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'Serif','Serif':['Palatino']})
rc('text', usetex=True)

legend_titles = {
    "max_force":    "Max Force",
    "phys_time":    "Timestep Physics",
    "num":          "\# of Boids",
    "rule_time":    "Timestep Rules"
}

y_labels = {
    0:  "$\sigma_{\hat{x}} \; \scriptstyle[m]$",
    1:  "$\sigma_{\hat{v}} \; \scriptstyle [ms^{-1}]$",
}

def import_data(files):
    data = []
    for file in files:
        ds = pk.load(open(misc.wd() + file + "_data.pickle", 'rb'))
        for d in ds:
            data.append(d)

    return data


def plot_mean(data):

    x = np.mean(np.array(data), axis=0)
    plt.plot(x)
    plt.xlabel("Timestep")
    plt.ylabel("Mean")
    plt.show()


def plot_multi(vars, data):

    ls = [None] * len(data)
    fig, ax = plt.subplots()

    for i in range(len(data)):
        d = np.array(data[i])
        d = d[:, vars["y"]]

        y = np.mean(d, axis=0) * vars["S2r"]    # Converting back to meters

        x, y, T0 = ND(vars, y, i)


        st = str(vars["variables"][i])
        ls[i], = ax.plot(x, y, label = st)
        ax.set_xlabel("$\hat{t}\;\scriptstyle[s]$", fontsize=20)
        ax.set_ylabel(y_labels[vars["y"]], fontsize=20)

    plt.grid()
    if len(vars["variables"]) > 4:
        leg = ax.legend(title=legend_titles[vars["working_var"]], ncol=2)
    else:
        leg = ax.legend(title=legend_titles[vars["working_var"]], ncol=1)
    plt.xlim(0, vars["run_time"]/T0)
    plt.ylim(bottom=0)
    plt.tight_layout()

    plt.show()



def ND(vars, y, i):
    # The several cases for ND will be handled individually here

    T0 = vars["s"] / vars["max_speed"]        # Time to do a full lap

    if vars["y"] == 0:  # x_std
        R0 = vars["s"] / vars["num"]          # Mean space between separated boids
    elif vars["y"] == 1:    # v_std
        R0 = vars["max_speed"]

    y = y / R0

    # Special handling for changing physics time
    if vars["working_var"] == 'phys_time':
        x = np.linspace(0, vars["run_time"], int(vars["run_time"] / vars["variables"][i])) / T0
    elif vars["working_var"] == 'max_speed':
        T0 = (vars["boid_size"] / vars["variables"][i])
        x = np.linspace(0, vars["run_time"],
                        int(vars["run_time"] / vars["variables"][i])) / T0
    else:
        x = np.linspace(0, vars["run_time"], int(vars["run_time"] / vars["phys_time"])) / T0

    return x, y, T0

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
    data = np.array(data)

    for i in range(data.shape[0]):
        d = data[i,:,1]
        y = np.mean(np.array(d), axis=0)
        x = np.linspace(0, vars["run_time"], len(y))
        st = str(vars["variables"][i])
        ls[i], = ax.plot(x, y, label=st)
        ax.set_xlabel("$t \; [s]$", fontsize=16)
        ax.set_ylabel("$\sigma_x \; [m]$", fontsize=16)

    plt.grid()
    if len(vars["variables"]) > 4:
        leg = ax.legend(title="Variable", ncol=2, fontsize=12)
    else:
        leg = ax.legend(title="Variable", ncol=1, fontsize=12)
    plt.xlim(0, int(vars["run_time"]))
    plt.tight_layout()

    plt.show()
