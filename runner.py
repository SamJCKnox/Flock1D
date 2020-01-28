import env
import pickle as pk
import plotter
import numpy as np
import os
import concurrent.futures
import time
import misc


seed = misc.load_seed()

# Nondimensionalising Calcs

# TIME
# A boid should not be able to travel its length without
# doing a rule update, therefore the timestep is derived from the
# characterisitc speed and the boid size:
boid_size = 0.3         # meters
char_speed = 20         # meters / second
T0 = boid_size / char_speed

# SPACE

arena = 500             # meters
num = 5                 # ND
density = num / arena
R0 = arena / num


vars = {
    # Statistics for Runs
    "seed":         seed,
    "runs":         50,
    "run_time":     10,                # Seconds
    "file":         'Test',

    # Sim Properties
    "num":          num,
    "s":            arena,
    "threshold":    0.01 * 2 * np.pi,
    "R0":           arena/(2*np.pi),
    "T0":           T0,
    "gains":        [1, 0, 0, 0],
    "rule_time":    0.5,               # Seconds
    "phys_time":    0.1,
    "max_force":    5 * 9.81,
    "max_speed":    char_speed,

    # Sim Bools
    "vis":          False,
    "plot":         False,
    "safety":       False,
    "serial":       True,
    "inner_serial": False,

    # Exp variables
    "working_var":  "phys_time",
    "variables":    [0.5, 0.1, 0.05, 0.01]
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
results = plotter.import_data([vars["file"]])

if vars["working_var"] == "phys_time" or vars["working_var"] == "rule_rate":
    plotter.plot_multi(vars, results)
elif vars["working_var"] == "num":
    plotter.plot_multi_mean_nums(vars, results)
elif vars["working_var"] == "gains[0]":
    plotter.plot_multi_velocity(vars, results)
elif vars["working_var"] == "max_force":
    plotter.plot_multi_velocity(vars, results)
elif vars["working_var"] == "max_speed":
    plotter.plot_multi_velocity(vars, results)

# Printing the final dictionary
for x in vars:
    print(x, ':', vars[x])


