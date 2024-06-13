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
main_test_cases = [2, 4]
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

results_stem = '/data/users/tbendall/results/swift_paper'
plot_stem = '/data/users/tbendall/results/swift_paper'

set_tomplot_style()

# ---------------------------------------------------------------------------- #
# Details about data structure
# ---------------------------------------------------------------------------- #

column_indices = {'measure': 4, 'variable': 5, 'value': 7}

for main_test_case in main_test_cases:

    plot_name = f'{plot_stem}/tab_4_convergence_test_{main_test_case}.png'
    fig, axarray = plt.subplots(1, len(regimes), figsize=(12, 6))

    for i, (regime, ax) in enumerate(zip(regimes, axarray)):


        if regime == 'big_cfl':
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
