import env
import pickle as pk
import plotter
import numpy as np
import os
import concurrent.futures
import time
import misc


seed = misc.load_seed()

vars = {
    # Statistics for Runs
    "seed":         seed,
    "runs":         1000,
    "run_time":     30,                # Seconds
    "file":         'R3',

    # Sim Properties
    "num":          5,
    "s":            500,
    "boid_size":    0.3,
    "threshold":    0.01 * 2 * np.pi,
    "S2r":          500/(2*np.pi),
    "gains":        [0, 1, 0, 0],
    "rule_time":    2,               # Seconds
    "phys_time":    0.01,
    "max_force":    5 * 9.81,
    "max_speed":    20,

    # Sim Bools
    "vis":          False,
    "plot":         True,
    "safety":       True,
    "serial":       True,
    "inner_serial": False,

    # Exp variables
    "working_var":  "phys_time",
    "variables":    [2, 1, 0.5, 0.1, 0.05, 0.01],

    # Plotting variables
    "y":            0                   # 0 for x_std, 1 for v_std
}

# Saving Vars File

if not vars["plot"]:
    if vars["safety"]:
        if os.path.exists(misc.wd() + vars["file"] + "_vars.pickle"):
            x = input("Do you want to write over old file? (y/n) ")
            if x == 'y':
                pk.dump(vars, open(misc.wd() + vars["file"] + "_vars.pickle", 'wb'))
            else:
                quit()
        else:
            pk.dump(vars, open(misc.wd() + vars["file"] + "_vars.pickle", 'wb'))

    if vars["serial"]:
        start = time.time()
        steps = vars["variables"]
        results = []
        for step in steps:
            vars[vars["working_var"]] = step
            if vars["inner_serial"]:
                results.append(env.run_sim_serial(vars))
            else:
                results.append(env.run_sim_parallel(vars))
        pk.dump(results, open(misc.wd() + vars["file"] + "_data.pickle", 'wb'))
        print(f'Overall time: {time.time()-start}')
    else:
        start = time.time()
    # Starting Multiprocessing tool
        with concurrent.futures.ProcessPoolExecutor() as executor:
            steps = vars['variables']
            args = []

            # Creates a new dictionary for each working variable
            for step in steps:
                vars[vars["working_var"]] = step
                args.append(vars.copy())

            if vars["inner_serial"]:
                results = executor.map(env.run_sim_serial, args)
            else:
                results = executor.map(env.run_sim_parallel, args)

            pk.dump(list(results), open(misc.wd() + vars["file"] + "_data.pickle", 'wb'))
            print(f'Overall time: {time.time() - start}')

# Plotting results
results = plotter.import_data([vars["file"],"R2"])

plotter.plot_multi(vars, results)

# Printing the final dictionary
for x in vars:
    print(x, ':', vars[x])


