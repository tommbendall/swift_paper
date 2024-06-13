"""
A first attempt at quickly plotting fields for the SWIFT paper, test 1
"""

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
from tomplot import (set_tomplot_style, tomplot_contours, tomplot_cmap,
                     plot_contoured_field, add_colorbar_fig,
                     tomplot_field_title, extract_lfric_coords,
                     extract_lfric_field, plot_field_quivers,
                     regrid_horizontal_slice, extract_lfric_vertical_slice)

# ---------------------------------------------------------------------------- #
# Things that can be altered and parameters for the test case
# ---------------------------------------------------------------------------- #
# Directories for results and to plot to
branch = 'r48987_swift_paper-transport-meto-spice-three_d'
results_dirname_stem = f'/data/users/tbendall/cylc-run/{branch}/share/output/intel_64-bit_fast-debug/transport'
plotdir = f'/data/users/tbendall/results/swift_paper'
mesh_dt = 'BiP64x64-1000x1000_dt-2p5'  # dt is 0p5, 1p25 or 2p5

# To alter test-by-test
test_number = 7
plot_stem = f'swift_paper_{test_number}'
title = r'3D Test'

# Options relating to the different fields to be plotted
field_names = ['rho', 'tracer_con', 'tracer_adv']
cbar_labels = [r"$\rho \ / $ kg m$^{-3}$",
               r"$m \ / $ kg kg$^{-1}$",
               r"$m^L \ / $ kg kg$^{-1}$"]
colour_schemes = ['YlGn', 'BuPu', 'BuPu']
remove_contours = [None, 0.0, 0.0]

# Options for different configurations
test_configs = ['cosmic', 'swift']
config_titles = ['COSMIC', 'SWIFT']

slice_along = 'y'
slice_at = 0.00078125  # Nearest value to the center

# Options shared for all plots and subplots
time_factor = 250.0  # For some reason LFRic outputs the wrong time
xlabel = r'$x \ /$ cm'
ylabel = r'$z \ /$ cm'
contour_method = 'contour'
time_idxs = [0,1]
level = 0
xlims = [-5, 5]
ylims = [0, 5]
contour_dict = {'rho': np.linspace(0.5, 1.0, 11),
                'tracer_adv': np.linspace(-0.2, 1.2, 15),
                'tracer_con': np.linspace(-0.2, 1.2, 15)}

# This is declared BEFORE figure and ax are initialised
set_tomplot_style(16)

# ---------------------------------------------------------------------------- #
# Loop through the different time-points
# ---------------------------------------------------------------------------- #

for time_idx in time_idxs:

    # Make figure
    fig, axarray = plt.subplots(len(config_titles), len(field_names),
                                figsize=(12, 8), sharex='col', sharey='row')

    all_cf = []

    for i, (field_name, colour_scheme, remove_contour) in \
        enumerate(zip(field_names, colour_schemes, remove_contours)):

        # -------------------------------------------------------------------- #
        # Loop through subplots
        # -------------------------------------------------------------------- #

        for j, (results_opt, config_title) in \
            enumerate(zip(test_configs, config_titles)):

            ax = axarray.flatten()[j*len(field_names)+i]

            results_dirname = f'{results_dirname_stem}/{results_opt}_skam3d/{mesh_dt}/results'
            main_filename = f'{results_dirname}/lfric_diag.nc'

            data_file = Dataset(main_filename, 'r')

            full_field_data = extract_lfric_field(data_file, field_name, time_idx)

            # Extract coords
            time = time_factor*data_file['time_instant'][time_idx]
            field_data, coords_X, coords_Y, coords_Z = \
                extract_lfric_vertical_slice(data_file, field_name, time_idx,
                                             slice_along=slice_along, slice_at=slice_at)

            # Scale coordinates
            coords_X *= 100.
            coords_Z *= 5./64.

            # ---------------------------------------------------------------- #
            # Plot data
            # ---------------------------------------------------------------- #

            # Contours based on data for whole row
            contours = contour_dict[field_name]
            cmap, lines = tomplot_cmap(contours, colour_scheme,
                                       remove_contour=remove_contour,
                                       cmap_rescale_type='top', cmap_rescaling=0.7)
            cf, _ = plot_contoured_field(ax, coords_X, coords_Z, field_data,
                                        contour_method, contours, line_contours=lines,
                                        cmap=cmap, plot_contour_lines=True)

            # Save cf for later
            all_cf.append(cf)

            data_file.close()

            # ---------------------------------------------------------------- #
            # Add labels
            # ---------------------------------------------------------------- #

            if i == 0:
                ax.set_ylabel(ylabel, labelpad=-10)
                ax.set_yticks(ylims)
                ax.set_yticklabels(ylims)
            ax.set_ylim(ylims)

            if j == len(config_titles) - 1:
                ax.set_xlabel(xlabel, labelpad=-10)
                ax.set_xticks(xlims)
                ax.set_xticklabels(xlims)
            ax.set_xlim(xlims)

            if i == len(field_names)-1:
                ax.text(6.0,1.6, config_title, fontsize=20,
                        horizontalalignment='center', rotation='vertical')

            tomplot_field_title(ax, None, minmax=True, field_data=full_field_data,
                                minmax_format='.4f')

    # -------------------------------------------------------------------- #
    # Add colorbars and adjust figures
    # -------------------------------------------------------------------- #

    for i, cbar_label in enumerate(cbar_labels):
        ij = (len(config_titles)-1)*len(field_names) + i
        add_colorbar_fig(fig, all_cf[i*len(config_titles)+j], cbar_label,
                         ax_idxs=[ij], cbar_labelpad=-10,
                         location='bottom', cbar_thickness=0.025)

    fig.subplots_adjust(hspace=0.2)

    # -------------------------------------------------------------------- #
    # Save figure
    # -------------------------------------------------------------------- #

    plt.suptitle(f'{title}, time: {time:0.0f} s')

    plotname = f'{plotdir}/{plot_stem}_time_{time_idx:02d}.png'
    print(f'Saving figure to {plotname}')
    fig.savefig(plotname, bbox_inches='tight')
    plt.close()
