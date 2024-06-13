"""
Plots a scalar horizontal transport test for multiple fields
"""

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
from tomplot import (set_tomplot_style, tomplot_contours, tomplot_cmap,
                     plot_contoured_field, add_colorbar_ax,
                     tomplot_field_title, extract_lfric_coords,
                     extract_lfric_field)

# ---------------------------------------------------------------------------- #
# Things that can be altered and parameters for the test case
# ---------------------------------------------------------------------------- #
# Options for different configurations to loop through
plot_stem = 'constant_xy'
title = r'Transport-Only X-Y'

# Options relating to the different fields to be plotted
field_names = ['rho', 'constant', 'tracer_adv', 'm_v']
cbar_labels = [r"$\rho \ / $ kg$\cdot$m$^{-3}$",
               r"$C \ / $ kg$\cdot$kg$^{-1}$",
               r"$q_{adv} \ / $ kg$\cdot$kg$^{-1}$",
               r"$m_v \ / $ kg$\cdot$kg$^{-1}$"]
colour_schemes = ['YlOrBr', 'bwr', 'YlGnBu', 'YlGnBu']
remove_contours = [1.0, None, 0.0, 0.0]
all_contours = [np.linspace(0.5, 1.5, 11),
                np.linspace(0.5, 1.5, 11),
                np.linspace(-1, 11, 13),
                np.linspace(-1, 11, 13)]
extra_cbarlabelpad = 0

# Options shared for all plots and subplots
xlabel = r'$x \ /$ m'
ylabel = r'$y \ /$ m'
contour_method = 'tricontour'
all_times = True  # If False, plots the last time step only
level = 0

xlims = [-1,1]
ylims = [-1,1]

# Directories that need specifying for results
test_name = 'constant_xy'
results_dirname_stem = '/home/h01/tbendall/lfric/swift_loc/miniapps/transport/debug_example'
plotdir = results_dirname_stem

# This is declared BEFORE figure and ax are initialised
set_tomplot_style(16)

results_dirname = f'{results_dirname_stem}'
# Determine number of time points
main_filename = f'{results_dirname}/lfric_diag.nc'
data_file = Dataset(main_filename, 'r')
num_time_idxs = len(data_file['time_instant'][:])
time_idxs = range(num_time_idxs)

dt = 0.1
diag_freq = 10

if not all_times:
    time_idxs = [-1]

# ---------------------------------------------------------------------------- #
# Loop through the different time-points
# ---------------------------------------------------------------------------- #

for time_idx in time_idxs:

    # Make figure
    fig = plt.figure(figsize=(12, 12))

    if time_idx == -1:
        time = dt*num_time_idxs*diag_freq
    else:
        time = dt*(time_idx+1)*diag_freq

    for i, (field_name, cbar_label, colour_scheme, remove_contour, contours) in \
        enumerate(zip(field_names, cbar_labels, colour_schemes, remove_contours, all_contours)):

        ax = fig.add_subplot(len(field_names), 2, 1+i)

        # ---------------------------------------------------------------- #
        # Data extraction
        # ---------------------------------------------------------------- #

        # Extract data
        coords_X, coords_Y = extract_lfric_coords(data_file, field_name)
        coords_X *= 100.
        coords_Y *= 100.
        field_data = extract_lfric_field(data_file, field_name, time_idx, level=level)

        print(field_name, np.min(field_data), np.max(field_data))

        # ---------------------------------------------------------------- #
        # Plot data
        # ---------------------------------------------------------------- #

        # Contours based on magnitude of vectors
        cmap, lines = tomplot_cmap(contours, colour_scheme, remove_contour=remove_contour)
        cf, _ = plot_contoured_field(ax, coords_X, coords_Y, field_data,
                                    contour_method, contours, line_contours=lines,
                                    cmap=cmap, plot_contour_lines=True)

        # ---------------------------------------------------------------- #
        # Add labels
        # ---------------------------------------------------------------- #

        # Label both y-axes
        ax.set_ylabel(ylabel, labelpad=-15)
        ax.set_yticks(ylims)
        ax.set_yticklabels(ylims)
        ax.set_ylim(ylims)

        ax.set_xlabel(xlabel, labelpad=-15)
        ax.set_xticks(xlims)
        ax.set_xticklabels(xlims)
        ax.set_xlim(xlims)

        tomplot_field_title(ax, None, minmax=True, minmax_format=".4f",
                            field_data=field_data)

        add_colorbar_ax(ax, cf, cbar_label, extra_labelpad=extra_cbarlabelpad,
                        location='right', cbar_format='.1f')

    # -------------------------------------------------------------------- #
    # Save figure
    # -------------------------------------------------------------------- #

    fig.subplots_adjust(wspace=0.25, hspace=0.3)

    plt.suptitle(f'{title}, time: {time:1.1f} s')

    plotname = f'{plotdir}/{plot_stem}_time_{time_idx:02d}.png'
    print(f'Saving figure to {plotname}')
    fig.savefig(plotname, bbox_inches='tight')
    plt.close()