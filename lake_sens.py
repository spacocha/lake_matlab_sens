#!/usr/bin/env python

import numpy as np, re

base_fn = 'run.m'
template_ext = '.template'

script_fn_base = 'run_'
script_ext = '.m'

command_base = 'matlab -nojvm -r run_'

n_submits = 3
submit_fn_base = 'submit_'
submit_ext = '.sh'

param_fn_base = 'params_'
param_ext = '.txt'

params = {
    '__NITROGEN_RATIO__' : 0.30,
    '__CARBON_RATIO__' : 1.0,
    '__FIXED_OXYGEN_LEVEL__' : 75.0,
    '__FIXED_OXYGEN_DIFFUSION__' : 1e4,
    '__FIXED_CO2_LEVEL__' : 600.0,
    '__T_MAX__' : 25.0,
    '__FE_PRECIPITATION__' : 0.1,
}

func_mask = '__FUNCTION_NAME__'
func_base = 'run_'

out_fn_mask = '__OUT__'
out_fn_base = 'rates_'
out_fn_ext = '.csv'

multipliers = np.linspace(0.99, 1.01, 3)

def write_dict(fn, d):
    with open(fn ,'w') as f:
        f.write("\n".join(["{0}\t{1}".format(k, v) for k, v in d.items()]))

# save the base params
write_dict('base_params.txt', params)

# read in the template file
with open(base_fn + template_ext, 'r') as f:
    base_script = f.read()

# modulate each of the parameters in turn
param_map = {}
for param_i, (param, base_val) in enumerate(params.items()):
    param_map[param_i] = param
    val_i = 0

    # when modulating this parameter, multiply by some multiplier
    val_map = {}
    for val_i, multiplier in enumerate(multipliers):
        val = base_val * multiplier
        val_map[val_i] = val
        params[param] = val

        script_i = "{0}_{1}".format(param_i, val_i)

        # go through each pair of params and values, replacing the param placeholder
        # with the value for this loop
        script = base_script
        for p, v in params.items():
            script = re.sub(p, str(v), script)

        # replace the output file direction
        script = re.sub(out_fn_mask, out_fn_base + script_i + out_fn_ext, script)

        # replace the function name
        script = re.sub(func_mask, func_base + script_i, script)

        # write this new script to a file
        with open(script_fn_base + script_i + script_ext, 'w') as f:
            f.write(script)

    # write out the value map
    write_dict("valmap_{0}.txt".format(param_i), val_map)

    # reset the parameter to its base value
    params[param] = base_val

# write out the param map
write_dict("parammap.txt", param_map)
