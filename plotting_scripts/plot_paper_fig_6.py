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
regime = 'const_dt'
titles = [r'Test 1: Constant $u$', r'Test 2: Deformational $u$', r'Test 3: Divergent $u$']

labels = [r'COSMIC $m$', r'SWIFT $m$']
variables = ['tracer_con', 'tracer_con']

schemes = ['cosmic', 'swift']
colours = ['red', 'blue']
markers = ['+', 'x']
legend = True

# ---------------------------------------------------------------------------- #
# Dictionary of resolutions for different tests
# ---------------------------------------------------------------------------- #

resolutions = {1: [256, 300, 400, 512, 600],
                2: [256, 300, 400, 512, 600, 700],
                3: [256, 300, 400, 512, 600, 700],
                4: [256, 300, 400, 512, 600, 700],
                5: [50, 64, 100, 128, 200],
                6: [50, 64, 100, 128, 200]}
dts = {1: ['0p05']*len(resolutions[1]),
        2: ['0p05']*len(resolutions[2]),
        3: ['0p05']*len(resolutions[3]),
        4: ['0p05']*len(resolutions[4]),
        5: ['0p025']*len(resolutions[5]),
        6: ['0p025']*len(resolutions[6])}

# ---------------------------------------------------------------------------- #
# Paths
# ---------------------------------------------------------------------------- #

results_stem = '/data/users/tbendall/results/swift_revision'
plot_stem = '/data/users/tbendall/results/swift_revision'
plot_name = f'{plot_stem}/fig_6_convergence.jpg'

set_tomplot_style(14)
fig, axarray = plt.subplots(1, len(test_cases), figsize=(12, 5))

# ---------------------------------------------------------------------------- #
# Details about data structure
# ---------------------------------------------------------------------------- #

column_indices = {'measure': 4, 'variable': 5, 'value': 7}


for i, (test_case, ax) in enumerate(zip(test_cases, axarray)):

    for j, variable in enumerate(variables):

        error_data = np.zeros(len(resolutions[test_case]))

        dxs = [1000. / res for res in resolutions[test_case]]

        for k, res in enumerate(resolutions[test_case]):

            dt = dts[test_case][k]
            data_file = f'{results_stem}/{schemes[j]}_test_{test_case}_conv_BiP{res}x{res}-1000x1000_{dt}.log'

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
                         marker=markers[j], log_base=10)

    # Adjust x limits to fit legend on nicely
    xlims = ax.get_xlim()
    ax.set_xlim([xlims[0], xlims[1] + 0.1*(xlims[1] - xlims[0])])
    ax.grid()

    only_minmax_ticklabels(ax)
    if legend:
        ax.legend(loc='lower right', fontsize=12)

    ax.set_title(titles[i])
    if i == 1:
        ax.set_xlabel(r'$\log_{10}(\Delta x)$', labelpad=0)
    if i == 0:
        ax.set_ylabel(r'$\log_{10}(||q-q_{true}||/||q_{true}||)$', labelpad=-25)

# ---------------------------------------------------------------------------- #
# Save figure
# ---------------------------------------------------------------------------- #
fig.subplots_adjust(wspace=0.25)
print(f'Saving figure to {plot_name}')
fig.savefig(plot_name, bbox_inches='tight', dpi=300)
plt.close()
