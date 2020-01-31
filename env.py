from boid import boid
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
from matplotlib.collections import PatchCollection
import time
import concurrent.futures
from tqdm import tqdm
import misc


def run_sim_serial(vars):
    start = time.time()
    print(f'Starting {vars["working_var"]} value: {vars[vars["working_var"]]}')

    result = []

    for i in range(vars["runs"]):
        vars["seed"] = misc.load_seed()
        result.append(sim(vars))

    v = vars[vars["working_var"]]
    print(f"Completed {v}, in time {time.time() - start}")
    return result


def run_sim_parallel(vars):
    print(f'Starting {vars["working_var"]} value: {vars[vars["working_var"]]}')
    start = time.time()
    args = []
    for i in range(vars['runs']):
        vars["seed"] = misc.load_seed()
        args.append(vars.copy())
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(sim, args), total=vars['runs']))

    v = vars[vars["working_var"]]
    print(f"Completed {v}, in time {time.time() - start}")
    return list(results)


def sim(vars):
    # Generate a new flock and migration point
    flock = [boid(vars) for _ in range(vars["num"])]

    n_std = []
    v_std = []
    x_av = []

    point = np.random.rand() * 2 * np.pi

    if vars["vis"]: vis_init()

    rule_rate = round(vars["rule_time"]/vars["phys_time"])

    for b in flock:
        b.reset(point)

    for j in range(int(vars["run_time"] / vars["phys_time"])):

        for b in flock:
            if j % rule_rate == 0:
                b.apply_behaviour(flock)

            b.update()

        # Check for point update
        for b in flock:
            if b.point_reached(point, vars["threshold"]):
                point = np.random.rand() * 2 * np.pi
                for bb in flock:
                    bb.set_point(point)

        if vars["vis"]: vis_frame(vars, point, flock, j)

        # Statistics
        xmin = np.zeros((vars["num"],))
        xav = np.zeros((vars["num"],))
        v = np.zeros((vars["num"],))
        for n, b in zip(range(vars["num"]), flock):
            xmin[n], xav[n] = b.nearest_neighbour(flock)
            v[n] = b.vel

        v_std.append(np.std(v))
        n_std.append(np.std(xmin))
        x_av.append(np.mean(xav))

    if vars["vis"]:
        plt.show(block=False)
        plt.pause(0.001)
        plt.close('all')
        plt.pause(0.001)

    return [n_std, v_std, x_av]


def vis_init():
    global fig, ax
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')


def vis_frame(vars, point, flock, iter):
    global fig, ax

    plt.cla()
    patches = []
    patches.append(Wedge((vars["s"] / 2, vars["s"] / 2), vars["s"] * 0.9 / 2, 0, 360, width=25))

    [x, y] = make_vector(point, vars)
    patches.append(Circle((x, y), vars["s"] * 0.04 / 2))
    for b in flock:
        [x, y] = make_vector(b.pos, vars)
        patches.append(Circle((x, y), vars["s"] * 0.04 / 2))
        [x, y] = make_text_vector(b.pos, vars)
        plt.text(x, y,
                 f"$F={b.acc:.1f}$\n$[{b.F_alignment:.1f},{b.F_cohesion:.1f},{b.F_separation:.1f},{b.F_migration:.1f}]$",
                 fontsize=10)

    p = PatchCollection(patches, alpha=0.6)
    colours = [0, 10]
    colours += list(range(80, 80 + vars["num"] * 5, 5))
    p.set_array(np.array(colours))
    ax.add_collection(p)
    ax.set_xlim(vars["s"])
    ax.set_ylim(vars["s"])
    plt.text(vars["s"] - 10, vars["s"] - 10, "$Time (sec) = {:.3f}$".format(iter * vars["phys_time"]), fontsize=12)
    plt.pause(0.001)
    fig.canvas.draw()


def make_vector(pos, vars):
    return [vars["s"] / 2 + np.cos(pos) * vars["s"] * 0.425, vars["s"] / 2 + np.sin(pos) * vars["s"] * 0.425]


def make_text_vector(pos, vars):
    return [vars["s"] / 2 + 0.05 * vars["s"] + np.cos(pos) * vars["s"] * 0.35,
            vars["s"] / 2 + np.sin(pos) * vars["s"] * 0.35]
