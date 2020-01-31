import env
import pickle as pk
import plotter
import numpy as np
import os
import concurrent.futures
import time
import misc

t = True
f = False

seed = misc.load_seed()

vars = {
    # Statistics for Runs
    "seed":         seed,
    "runs":         2,
    "run_time":     40,                # Seconds
    "file":         'R4',

    # Sim Properties
    "num":          5,
    "s":            500,
    "boid_size":    0.3,
    "threshold":    0.01 * 2 * np.pi,
    "S2r":          500/(2*np.pi),
    "gains":        [0, 1, 0, 0],
    "rule_time":    0.1,               # Seconds
    "phys_time":    0.1,
    "max_force":    5 * 9.81,
    "max_speed":    20,
    "sep_a":        100,            # Gaussian function: a is the height of the curve
    "sep_c":        1,              # Gaussian function: c is the std of the curve

    # Sim Bools
    "vis":          False,
    "plot":         False,
    "safety":       True,
    "serial":       True,
    "inner_serial": t,
    "help":         False,

    # Exp variables
    "working_var":  "num",
    "variables":    [5, 6, 7, 8],

    # Plotting variables
    "y":            2                   # 0 for x_std, 1 for v_std, 2 for x_av
}
# Help functions
if vars["help"]:
    x = input("Available functions:\n1: Separation Plot\n2: Dictionary Print\n ")
    if x == '1':
        misc.separation_plot(vars)
    if x == '2':
        x = input("Which vars file? ")
        try:
            misc.print_dict(x)
        except:
            x = input('That file doesn\'t exist, try again: ')
            misc.print_dict(x)




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
results = plotter.import_data([vars["file"]])

plotter.plot_multi(vars, results)

# Printing the final dictionary
for x in vars:
    print(x, ':', vars[x])


