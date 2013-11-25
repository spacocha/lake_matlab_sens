#!/usr/bin/env python

import numpy as np, re

base_fn = 'run.m'
template_ext = '.template'

script_fn_base = 'run_'
script_ext = '.m'

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

out_fn_mask = '__OUT__'
out_fn_base = 'rates_'
out_fn_ext = '.csv'

multipliers = np.linspace(0.99, 1.01, 3)

# read in the template file
with open(base_fn + template_ext, 'r') as f:
    base_script = f.read()

# set up indexing
i = 0

# modulate each of the parameters in turn
for param, base_val in params.items():
    # when modulating this parameter, multiply by some multiplier
    for multiplier in multipliers:
        params[param] = base_val * multiplier

        # go through each pair of params and values, replacing the param placeholder
        # with the value for this loop
        script = base_script
        for p, v in params.items():
            script = re.sub(p, str(v), script)

        # replace the output file direction
        script = re.sub(out_fn_mask, out_fn_base + str(i) + out_fn_ext, script)

        # write this new script to a file
        with open(script_fn_base + str(i) + script_ext, 'w') as f:
            f.write(script)

        # write the parameters to a separate file
        with open(param_fn_base + str(i) + param_ext, 'w') as f:
            f.write("\n".join(["{0}\t{1}".format(k, v) for k, v in params.items()]))

        i += 1

    # reset the parameter to its base value
    params[param] = base_val
