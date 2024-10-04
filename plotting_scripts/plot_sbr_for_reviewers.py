"""
Plots tracer transport on the sphere, at different time points.
"""
from os.path import abspath, dirname
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from tomplot import (
    set_tomplot_style, tomplot_cmap, plot_contoured_field,
    add_colorbar_fig, plot_field_quivers, tomplot_field_title,
    extract_lfric_coords, extract_lfric_field, regrid_horizontal_slice,
    plot_cubed_sphere_panels
)

full_test_name = 'transport_sbr_gaussian_corner_ffsl-C24_spice_intel_fast-debug-64bit'

# ---------------------------------------------------------------------------- #
# Directory for results and plots
# ---------------------------------------------------------------------------- #
results_file_path = f'/data/users/tbendall/cylc-run/r3751_swift_rev_plus/run4/share/output/transport/{full_test_name}/results'
plot_file_path = '/home/h01/tbendall/results'
plot_stem = 'swift_sbr'

# ---------------------------------------------------------------------------- #
# Plot details
# ---------------------------------------------------------------------------- #
field_name = 'm_v'
colour_scheme = 'Purples'
contours = np.linspace(0.5, 5, 10)
field_label = r'$m$ (kg kg$^{-1}$)'
remove_contour = 1.0

# ---------------------------------------------------------------------------- #
# General options
# ---------------------------------------------------------------------------- #
projection = ccrs.Robinson()
contour_method = 'contour'
xlims = [-180, 180]
ylims = [-90, 90]

time_idxs = [0, 1, 3, 5, 7, 8]

# We need to regrid onto lon-lat grid -- specify that here
lon_1d = np.linspace(-180.0, 180.0, 120)
lat_1d = np.linspace(-90, 90, 120)
lon_2d, lat_2d = np.meshgrid(lon_1d, lat_1d, indexing='ij')

# Things that are likely the same for all plots --------------------------------
set_tomplot_style()

# ---------------------------------------------------------------------------- #
# PLOTTING
# ---------------------------------------------------------------------------- #
fig = plt.figure(figsize=(12, 12))

for i, time_idx in enumerate(time_idxs):

    if time_idx == 0:
        data_file = Dataset(f'{results_file_path}/lfric_initial.nc')
        raw_time_idx = None
    else:
        data_file = Dataset(f'{results_file_path}/lfric_diag.nc')
        raw_time_idx = time_idx - 1

    # Make axes
    ax = fig.add_subplot(int(len(time_idxs)/2), 2, 1+i, projection=projection)

    # Data extraction ----------------------------------------------------------
    field_data = extract_lfric_field(data_file, field_name, time_idx=raw_time_idx, level=0)
    coords_X, coords_Y = extract_lfric_coords(data_file, field_name)

    if time_idx == 0:
        time = 0.0
    else:
        time = data_file['time_instant'][raw_time_idx] / (24.*60.*60.)

    # Regrid onto lon-lat grid
    field_data = regrid_horizontal_slice(
        lon_2d, lat_2d, coords_X, coords_Y, field_data, periodic_fix='sphere'
    )

    # Plot data ----------------------------------------------------------------
    cmap, lines = tomplot_cmap(contours, colour_scheme, remove_contour=remove_contour)
    cf, _ = plot_contoured_field(
        ax, lon_2d, lat_2d, field_data, contour_method, contours,
        cmap=cmap, line_contours=lines, projection=projection
    )

    tomplot_field_title(ax, r'$t = $'+f'{time:.1f} days', minmax=True, field_data=field_data)

    plot_cubed_sphere_panels(ax, projection=projection)

add_colorbar_fig(
    fig, cf, field_label, ax_idxs=range(len(time_idxs)), location='bottom', cbar_labelpad=-10,
    cbar_format='1.1f'
)

# Save figure ------------------------------------------------------------------
fig.subplots_adjust(wspace=0.2, hspace=0.2)
plot_name = f'{plot_file_path}/{plot_stem}.png'
print(f'Saving figure to {plot_name}')
fig.savefig(plot_name, bbox_inches='tight')
plt.close()