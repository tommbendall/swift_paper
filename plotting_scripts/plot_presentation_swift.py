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
                     regrid_horizontal_slice)

# ---------------------------------------------------------------------------- #
# Things that can be altered and parameters for the test case
# ---------------------------------------------------------------------------- #
# Directories for results and to plot to
branch = 'r48987_swift_paper-transport-meto-spice-presentation'
results_dirname_stem = f'/data/users/tbendall/cylc-run/{branch}/share/output/intel_64-bit_fast-debug/transport'
plotdir = f'/data/users/tbendall/results/swift_paper'
mesh_dt = 'BiP128x128-1000x1000_dt-2p0'

# To alter test-by-test
plot_stem = 'deformational'
test_number = 4
title = r'$c_{max}=5.12$'

# Options relating to the different fields to be plotted
field_names = ['rho', 'tracer_adv']
cbar_labels = [r"$\rho \ / $ kg m$^{-3}$",
               r"$m \ / $ kg kg$^{-1}$"]
colour_schemes = ['YlGn', 'BuPu']
remove_contours = [0.8, None]
extend_cmaps = [False, True]

# Options for different configurations
test_configs = ['cosmic', 'swift']
config_titles = ['COSMIC', 'SWIFT']

# Options shared for all plots and subplots
time_factor = 20.0  # For some reason LFRic outputs the wrong time
xlabel = r'$x \ /$ km'
ylabel = r'$y \ /$ km'
contour_method = 'tricontour'
time_idxs = [0,5,10,15,20,25,30,35,40,45,50]
level = 0
xlims = [-0.5, 0.5]
ylims = [-0.5, 0.5]
vector_magnitude_cutoff = 0.01
spatial_filter_step = 5
contour_dict = {'rho': np.linspace(0.5, 1.1, 13),
                'tracer_adv': np.linspace(0.0, 1.0, 11),
                'tracer_con': np.linspace(0.0, 1.0, 11)}

# This is declared BEFORE figure and ax are initialised
set_tomplot_style(16)

# ---------------------------------------------------------------------------- #
# Loop through the different time-points
# ---------------------------------------------------------------------------- #

for l, raw_time_idx in enumerate(time_idxs):

    # Make figure
    fig, axarray = plt.subplots(len(config_titles), len(field_names),
                                figsize=(8, 8), sharex='col', sharey='row')

    all_cf = []

    for i, (field_name, colour_scheme, remove_contour, extend_cmap) in \
        enumerate(zip(field_names, colour_schemes, remove_contours, extend_cmaps)):

        # -------------------------------------------------------------------- #
        # Loop through subplots
        # -------------------------------------------------------------------- #

        for j, (results_opt, config_title) in \
            enumerate(zip(test_configs, config_titles)):

            ax = axarray.flatten()[j*len(field_names)+i]

            results_dirname = f'{results_dirname_stem}/{results_opt}_test_{test_number}/{mesh_dt}/results'

            main_filename = f'{results_dirname}/lfric_diag.nc'
            init_filename = f'{results_dirname}/lfric_initial.nc'

            if raw_time_idx == 0:
                time_idx = None
                data_file = Dataset(init_filename, 'r')
                # Extract coords
                time = 0.0
                coords_X, coords_Y = extract_lfric_coords(data_file, field_name)
                field_data = extract_lfric_field(data_file, field_name, level=level)

            else:
                data_file = Dataset(main_filename, 'r')
                time_idx = raw_time_idx - 1
                # Extract coords
                time = time_factor*data_file['time_instant'][time_idx]
                coords_X, coords_Y = extract_lfric_coords(data_file, field_name)
                field_data = extract_lfric_field(data_file, field_name, time_idx, level=level)

            # Scale coordinates
            coords_X *= 10.
            coords_Y *= 10.

            # Handle tiny new extrema
            if field_name == 'tracer_adv':
                field_data = np.where(np.abs(field_data + 1.0e-12) < 2.0e-12, 0.0, field_data)
                field_data = np.where(np.abs(field_data - 1.0 + 1.0e-12) < 2.0e-12, 1.0 - 1.0e-12, field_data)

            # ---------------------------------------------------------------- #
            # Plot data
            # ---------------------------------------------------------------- #

            # Contours based on data for whole row
            contours = contour_dict[field_name]
            cmap, lines = tomplot_cmap(contours, colour_scheme,
                                       remove_contour=remove_contour,
                                       extend_cmap=extend_cmap)
            cf, _ = plot_contoured_field(ax, coords_X, coords_Y, field_data,
                                        contour_method, contours, line_contours=lines,
                                        cmap=cmap, plot_contour_lines=True)

            # Save cf for later
            all_cf.append(cf)

            # ---------------------------------------------------------------- #
            # Add wind vectors
            # ---------------------------------------------------------------- #

            if field_name == 'rho':
                coords_X_raw, coords_Y_raw = extract_lfric_coords(data_file, 'u_in_w2h')

                # Scale coordinates
                coords_X_raw *= 10.
                coords_Y_raw *= 10.

                field_data_X_raw = extract_lfric_field(data_file, 'u_in_w2h', time_idx, level)
                field_data_Y_raw = extract_lfric_field(data_file, 'v_in_w2h', time_idx, level)

                # To be able to filter plotted vectors nicely, regrid to 2d-array
                new_coords_X, new_coords_Y = \
                    np.meshgrid(np.linspace(xlims[0], xlims[1], 50),
                                np.linspace(ylims[0], ylims[1], 50), indexing='ij')

                field_data_X = regrid_horizontal_slice(new_coords_X, new_coords_Y,
                                                       coords_X_raw, coords_Y_raw,
                                                       field_data_X_raw)
                field_data_Y = regrid_horizontal_slice(new_coords_X, new_coords_Y,
                                                       coords_X_raw, coords_Y_raw,
                                                       field_data_Y_raw)
                field_data_mag = np.sqrt(field_data_X**2 + field_data_Y**2)

                # Quivers
                _ = plot_field_quivers(ax, new_coords_X, new_coords_Y, field_data_X, field_data_Y,
                                       scale=250, minlength=vector_magnitude_cutoff,
                                       magnitude_filter=vector_magnitude_cutoff,
                                       spatial_filter_step=spatial_filter_step)

            data_file.close()

            # ---------------------------------------------------------------- #
            # Add labels
            # ---------------------------------------------------------------- #

            if i == 0:
                ax.set_ylabel(ylabel, labelpad=-20)
                ax.set_yticks(ylims)
                ax.set_yticklabels(ylims)
            ax.set_ylim(ylims)

            if j == len(config_titles) - 1:
                ax.set_xlabel(xlabel, labelpad=-12)
                ax.set_xticks(xlims)
                ax.set_xticklabels(xlims)
            ax.set_xlim(xlims)

            tomplot_field_title(ax, None, minmax=True, field_data=field_data,
                                minmax_format='.4f')

            if i == len(field_names)-1:
                ax2 = ax.twinx()
                ax2.set_yticks([])
                text = f'{config_title}'
                ax2.set_ylabel(text, labelpad=10)

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

    plt.suptitle(f'{title}, '+r'$t=$'+f' {time:0.0f} s')

    plotname = f'{plotdir}/presentation_swift_{l:02d}.jpg'
    print(f'Saving figure to {plotname}')
    fig.savefig(plotname, bbox_inches='tight')
    plt.close()
