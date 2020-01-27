import pickle as pk
import numpy as np
import time


def load_seed():
    seeds = pk.load(open('seed.pickle', 'rb'))

    if len(seeds) < 100:
        try:
            np.random.seed(seeds[0])
        except:
            print("Ran out of seed, might be a bug")
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
    return "/home/samknox/Dropbox (The University of Manchester)/D2020/PhD/Experiments/FlockingPython/Logs/"