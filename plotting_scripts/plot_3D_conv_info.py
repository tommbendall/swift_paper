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

test_case = 'skam3d'
regimes = ['small_cfl', 'big_cfl']
titles = [r'Small $c$', 'Big $c$']

equations = ['advective', 'advective', 'advective', 'advective',
             'conservative', 'conservative',
             'conservative', 'conservative', 'conservative', 'conservative', ]
labels = [r'COSMIC $m_{adv}$', r'SWIFT $m_{adv}$', r'COSMIC $m_{adv}^L$', r'SWIFT $m_{adv}^L$',
          r'COSMIC $\rho$', r'SWIFT $\rho$',
          r'COSMIC $m_{cons}$', r'SWIFT $m_{cons}$', r'COSMIC $m_{cons}^L$', r'SWIFT $m_{cons}^L$']
variables = ['tracer_con', 'tracer_con', 'tracer_adv', 'tracer_adv',
             'rho', 'rho',
             'tracer_con', 'tracer_con', 'tracer_adv', 'tracer_adv']

schemes = ['cosmic', 'swift', 'cosmic', 'swift', 'cosmic', 'swift', 'cosmic', 'swift', 'cosmic', 'swift']
colours = ['black', 'red', 'blue', 'cyan', 'purple', 'magenta', 'lime', 'brown', 'orange', 'pink']
markers = ['+', 'x', '^', 'v', 's', 'o', '+', 'x', '^', 'v']
legend = True

# ---------------------------------------------------------------------------- #
# Dictionary of resolutions for different tests
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Paths
# ---------------------------------------------------------------------------- #

results_stem = '/data/users/tbendall/results/swift_revision'
plot_stem = '/data/users/tbendall/results/swift_revision'

set_tomplot_style()

# ---------------------------------------------------------------------------- #
# Details about data structure
# ---------------------------------------------------------------------------- #

column_indices = {'measure': 4, 'variable': 5, 'value': 7}

plot_name = f'{plot_stem}/conv_3D_test_{test_case}.png'
fig, axarray = plt.subplots(1, len(regimes), figsize=(12, 6))

for i, (regime, ax) in enumerate(zip(regimes, axarray)):


    if regime == 'big_cfl':
        resolutions = [64, 80, 128]
        dts = ['2p5', '2p0', '1p25']


    elif regime == 'small_cfl':
        resolutions = [64, 80, 128]
        dts = ['0p25', '0p2', '0p125']


    for j, variable in enumerate(variables):

        error_data = np.zeros(len(resolutions))

        dxs = [1000. / res for res in resolutions]

        for k, res in enumerate(resolutions):

            dt = dts[k]
            data_file = f'{results_stem}/{schemes[j]}_{test_case}_conv_{res}_{dt}.log'

            # ------------------------------------------------------------ #
            # Extract data
            # ------------------------------------------------------------ #

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

        # ---------------------------------------------------------------- #
        # Plot
        # ---------------------------------------------------------------- #

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

# ------------------------------------------------------------------------ #
# Save figure
# ------------------------------------------------------------------------ #
print(f'Saving figure to {plot_name}')
fig.savefig(plot_name, bbox_inches='tight')
plt.close()
