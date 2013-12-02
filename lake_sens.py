#!/usr/bin/env python

import numpy as np, re, csv, itertools

command_mask = 'matlab -nojvm -r "run({}); exit;"'

n_submits = 1

submit_fn_mask = 'submit_{0}.sh'

param_fn_base = 'params_'
param_ext = '.txt'

# list of parameters in the same order as in the matlab definition
# the last matlab parameter must be the output file
base_params = [
    ['__NITROGEN_RATIO__', 0.30],
    ['__CARBON_RATIO__', 1.0],
    ['__FIXED_OXYGEN_LEVEL__', 75.0],
    ['__FIXED_OXYGEN_DIFFUSION__', 1e4],
    ['__FIXED_CO2_LEVEL__', 600.0],
    ['__T_MAX__', 25.0],
    ['__FE_PRECIPITATION__', 0.1],
]

out_fn_mask = '\'rates_{}.csv\''
out_fn_base = 'rates_'
out_fn_ext = '.csv'

multipliers = np.linspace(0.99, 1.01, 5)

# get a list of just the parameters
# add numbers to the base params
params = [x[1] for x in base_params]
base_params = [[i] + x for i, x in enumerate(base_params)]

# save the base params
def write_rows(fn, rows):
    with open(fn, 'w') as f:
        w = csv.writer(f)
        w.writerows(rows)

write_rows('base_params.txt', base_params)

# prepare the command list
commands = {}
command_cycler = itertools.cycle(range(n_submits))
for i in range(n_submits):
    commands[i] = []

# modulate each of the parameters in turn
for param_i, base_val in enumerate(params):

    # when modulating this parameter, multiply by some multiplier
    val_list = []
    for val_i, multiplier in enumerate(multipliers):
        these_params = list(params)
        this_val = params[param_i] * multiplier
        these_params[param_i] = this_val

        val_list.append([val_i, this_val])

        run_id = "{0}_{1}".format(param_i, val_i)

        # add the filename to the list of parameters
        out_fn = out_fn_mask.format(run_id)
        these_params.append(out_fn)

        # stringify the filename
        params_string = ','.join([str(x) for x in these_params])

        # make the command
        command = command_mask.format(params_string)
        commands[command_cycler.next()].append(command)

    # write out the value map
    write_rows('valmap_{0}.txt'.format(param_i), val_list)

# write out the command files
for submit_i, commands in commands.items():
    submit_fn = submit_fn_mask.format(submit_i)

    with open(submit_fn, 'w') as f:
        f.write("\n".join(commands))
