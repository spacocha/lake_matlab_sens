#!/usr/bin/env python

'''
Use the rates_...csv files produced from the matlab runs to find
the sensitivity of different positions for each rate curve to each
of the modified parameters
'''

import numpy as np
import scipy.interpolate, scipy.stats

vals = [0, 1, 2, 3, 4]
rate_i = 0

positions = []
for val in vals:
    fn = 'data/rates_0_{0}.csv'.format(val)
    dat = np.genfromtxt(fn, delimiter=',')
    x = range(dat.shape[0])
    y = dat[:, rate_i]

    f = scipy.interpolate.interp1d(x, y, kind='cubic')

    new_x = np.linspace(min(x), max(x), 1000)
    new_y = f(new_x)
    print new_y
    new_dat = np.vstack((new_x, new_y)).T

    # find the value and position of the maximum
    max_pos = np.argmax(new_y)
    max_x = new_x[max_pos]
    max_y = np.max(new_y)

    # find the upper and lower half-max
    above_hm = new_x[new_y > np.max(new_y) / 2]
    uhm = np.max(above_hm)
    lhm = np.min(above_hm)

    positions.append([val, lhm, max_x, uhm])

    np.savetxt('out_{0}'.format(val), new_dat)

positions = np.array(positions)

# do the linear regressions for each column
for i in [1, 2, 3]:
    x = positions[:, 0]
    y = positions[:, i]
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    print i, slope

#np.savetxt('out', out)
