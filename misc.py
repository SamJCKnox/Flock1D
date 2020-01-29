import pickle as pk
import numpy as np
import time

mac = 0     # If running on mac, mac = 1

def load_seed():
    try:
        seeds = pk.load(open('seed.pickle', 'rb'))
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