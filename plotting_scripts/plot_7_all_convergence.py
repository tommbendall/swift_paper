"""
Plots convergence of specified tests
"""

import numpy as np
import matplotlib.pyplot as plt
from tomplot import (set_tomplot_style, plot_convergence,
                     only_minmax_ticklabels, tomplot_legend_ax,
                     tomplot_legend_fig)
import pandas as pd

# ---------------------------------------------------------------------------- #
# Options
# ---------------------------------------------------------------------------- #
test_cases = [2, 4, 6]
regime = 'big_cfl'
titles = [f'Test {test}' for test in test_cases]

version = 'limiter'  # 'limiter' or 'advective' or 'advective_limiter'

if version == 'limiter':
    equations = ['conservative', 'conservative', 'conservative', 'conservative', 'conservative', 'conservative', ]
    labels = [r'COSMIC $\rho$', r'SWIFT $\rho$', r'COSMIC $m_{cons}$', r'COSMIC $m_{cons}^L$', r'SWIFT $m_{cons}$', r'SWIFT $m_{cons}^L$']
    variables = ['rho', 'rho', 'tracer_con', 'tracer_adv', 'tracer_con', 'tracer_adv']

elif version == 'advective':
    equations = ['conservative', 'conservative', 'conservative', 'advective', 'conservative', 'advective', ]
    labels = [r'COSMIC $\rho$', r'SWIFT $\rho$', r'COSMIC $m_{cons}$', r'COSMIC $m_{adv}$', r'SWIFT $m_{cons}$', r'SWIFT $m_{adv}$']
    variables = ['rho', 'rho', 'tracer_con', 'tracer_con', 'tracer_con', 'tracer_con']

elif version == 'advective_limiter':
    equations = ['conservative', 'conservative', 'advective', 'advective', 'advective', 'advective', ]
    labels = [r'COSMIC $\rho$', r'SWIFT $\rho$', r'COSMIC $m_{adv}$', r'COSMIC $m_{adv}^L$', r'SWIFT $m_{adv}$', r'SWIFT $m_{adv}^L$']
    variables = ['rho', 'rho', 'tracer_con', 'tracer_adv', 'tracer_con', 'tracer_adv']


schemes = ['cosmic', 'swift', 'cosmic', 'cosmic', 'swift', 'swift']
colours = ['black', 'red', 'blue', 'cyan', 'purple', 'magenta']
markers = ['+', 'x', '^', 'v', 's', 'o']
legend = True

# ---------------------------------------------------------------------------- #
# Dictionary of resolutions for different tests
# ---------------------------------------------------------------------------- #

if regime == 'const_dt_paper':
    resolutions = {1: [256, 300, 400, 512, 600],
                   2: [256, 300, 400, 512, 600],
                   3: [256, 300, 400, 512, 600, 700],
                   4: [256, 300, 400, 512, 600, 700],
                   5: [50, 64, 100, 128, 200, 256],
                   6: [50, 64, 100, 128, 200, 256]}
    dts = {1: ['0p05']*len(resolutions[1]),
           2: ['0p05']*len(resolutions[2]),
           3: ['0p05']*len(resolutions[3]),
           4: ['0p05']*len(resolutions[4]),
           5: ['0p025']*len(resolutions[5]),
           6: ['0p025']*len(resolutions[6])}

elif regime == 'big_cfl':
    resolutions = {1: [64, 128, 256, 512],
                   2: [64, 128, 256, 512],
                   3: [64, 128, 256, 512],
                   4: [64, 128, 256, 512],
                   5: [64, 128, 256, 512],
                   6: [64, 128, 256, 512]}
    dts = {1: ['4p0', '2p0', '1p0', '0p5'],
           2: ['4p0', '2p0', '1p0', '0p5'],
           3: ['4p0', '2p0', '1p0', '0p5'],
           4: ['4p0', '2p0', '1p0', '0p5'],
           5: ['4p0', '2p0', '1p0', '0p5'],
           6: ['4p0', '2p0', '1p0', '0p5']}


elif regime == 'small_cfl':
    resolutions = {1: [64, 128, 256, 512],
                   2: [64, 128, 256, 512],
                   3: [64, 128, 256, 512],
                   4: [64, 128, 256, 512],
                   5: [64, 128, 256, 512],
                   6: [64, 128, 256, 512]}
    dts = {1: ['0p4', '0p2', '0p1', '0p05'],
           2: ['0p4', '0p2', '0p1', '0p05'],
           3: ['0p4', '0p2', '0p1', '0p05'],
           4: ['0p4', '0p2', '0p1', '0p05'],
           5: ['0p4', '0p2', '0p1', '0p05'],
           6: ['0p4', '0p2', '0p1', '0p05']}

# ---------------------------------------------------------------------------- #
# Paths
# ---------------------------------------------------------------------------- #

results_stem = '/data/users/tbendall/results/swift_paper'
plot_stem = '/data/users/tbendall/results/swift_paper'
plot_name = f'{plot_stem}/convergence_{regime}_{version}.png'

set_tomplot_style()
fig, axarray = plt.subplots(1, len(test_cases), figsize=(16.5, 6))

# ---------------------------------------------------------------------------- #
# Details about data structure
# ---------------------------------------------------------------------------- #

column_indices = {'measure': 4, 'variable': 5, 'value': 7}


for i, (main_test_case, ax) in enumerate(zip(test_cases, axarray)):

    for j, variable in enumerate(variables):

        if equations[j] == 'advective':
            test_case = main_test_case - 1
        else:
            test_case = main_test_case

        error_data = np.zeros(len(resolutions[test_case]))

        dxs = [1000. / res for res in resolutions[test_case]]

        for k, res in enumerate(resolutions[test_case]):

            dt = dts[test_case][k]
            data_file = f'{results_stem}/{schemes[j]}_test_{test_case}_conv_BiP{res}x{res}-1000x1000_dt-{dt}.log'

            # ---------------------------------------------------------------- #
            # Extract data
            # ---------------------------------------------------------------- #

            data = pd.read_csv(data_file, header=None, sep=' ', skipinitialspace=True, usecols=column_indices.values())

            # Name columns
            column_titles = {}
            for key, value in column_indices.items():
                column_titles[value] = key
            data =  data.rename(columns=column_titles)

            # Convert data to float
            data['value'] = data['value'].astype(float)

            # Extract error value for this data point
            error_data[k] = data[(data['measure'] == 'Rel-L2-error') & (data['variable'] == variable)]['value'].values[0]

        # -------------------------------------------------------------------- #
        # Plot
        # -------------------------------------------------------------------- #

        plot_convergence(ax, dxs, error_data, label=f'{labels[j]}:', color=colours[j],
                         marker=markers[j])

    # Adjust x limits to fit legend on nicely
    xlims = ax.get_xlim()
    ax.set_xlim([xlims[0], xlims[1] + 0.1*(xlims[1] - xlims[0])])
    ax.grid()

    only_minmax_ticklabels(ax)
    if legend:
        ax.legend(loc='lower right', fontsize=14)

    ax.set_title(titles[i])
    ax.set_xlabel(r'$\log(\Delta x)$', labelpad=-10)
    if i == 0:
        ax.set_ylabel(r'$\log(||q-q_{true}||_{L^2})$', labelpad=-10)

# ---------------------------------------------------------------------------- #
# Save figure
# ---------------------------------------------------------------------------- #
print(f'Saving figure to {plot_name}')
fig.savefig(plot_name, bbox_inches='tight')
plt.close()
