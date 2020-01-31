import pickle as pk
import numpy as np
import time
import boid
import matplotlib.pyplot as plt

mac = 0     # If running on mac, mac = 1

def load_seed():
    try:
        seeds = pk.load(open('seed.pickle', 'rb'))
        s = seeds[0]
    except:
        np.random.seed(round(time.time()))
        make_seeds()
        seeds = pk.load(open('seed.pickle', 'rb'))
        s = seeds[0]

    seeds = np.delete(seeds, 0)
    pk.dump(seeds, open('seed.pickle', 'wb'))
    return s


def make_seeds():
    seeds = np.random.randint(0, 2 ** 20, 10000)
    pk.dump(seeds, open('seed.pickle', 'wb'))

def wd():
    if mac:
        return "/Users/samknox/Dropbox (The University of Manchester)/D2020/PhD/Experiments/FlockingPython/Logs/"
    else:
        return "/home/samknox/Dropbox (The University of Manchester)/D2020/PhD/Experiments/FlockingPython/Logs/"


def separation_plot(vars):
    b = boid.boid(vars)
    xs = np.linspace(-250,250,1000) / vars["S2r"]
    ys = np.zeros(1000)

    mf = b.max_force

    for x, i in zip(xs, range(1000)):
        ys[i] = b.separation_profile(x)/mf

    xs = xs * vars["S2r"] / vars["s"]

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(xs,ys)

    for y, i in zip(ys, range(1000)):
        if y > 1:
            width = i
            break

    size = -xs[i]*2 * vars["s"]
    plt.annotate(s='', xy=(xs[width], 1), xytext=(xs[500-(width-500)], 1), arrowprops=dict(arrowstyle='<->'))
    plt.text(xs[500-(width-500)]+0.01, 0.92,
             f'$Width = {size:.1f}\; [m]$',
             fontsize=14)

    y2 = [1] * 1000
    ax.plot(xs, y2, 'r--')
    ax.set_xlabel('$\hat{x}$')
    ax.set_ylabel('$\hat{F}$')
    ax.grid()
    ax.set_xlim((-0.5, 0.5))
    plt.tight_layout()

    plt.show()
    quit()

def print_dict(x):
    vars = pk.load(open(wd() + x + "_vars.pickle", 'rb'))

    for x in vars:
        print(x, ':', vars[x])