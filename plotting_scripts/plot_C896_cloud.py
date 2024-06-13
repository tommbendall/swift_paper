"""
Plots lon-lat slices of high resolution NWP data
"""
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from netCDF4 import Dataset
import numpy as np
import pandas as pd
from tomplot import plot_contoured_field, plot_cubed_sphere_panels, \
                    tomplot_field_title, set_tomplot_style, \
                    tomplot_cmap, extract_lfric_coords, extract_lfric_field

# ---------------------------------------------------------------------------- #
# Variables to alter based on the desired plot and test case
# ---------------------------------------------------------------------------- #

# Parameters for data extraction and figure creation that must be specified
results_filename = '/data/users/tbendall/c896_lfric_gal_diagnostics.nc'
plotdir = '/home/h01/tbendall/results'
plotstem = 'c896_cloud_portland'
figsize = (10,10)

# Things that will be the same for each field
time_idxs = range(24)
lon_centre = -122.6784
lat_centre = 45.5152
projection = ccrs.Orthographic(lon_centre, lat_centre)
field_filter = True

# Things that differ with each field
field_names = ['m_cl', 'sw_up_toa']
methods = ["scatter", "scatter"]
colour_schemes = ['Greys', 'Greys_r']
zorder = 2
all_contours = [np.linspace(5e-5, 5.5e-3, 101),
                np.linspace(0.0, 1050.0, 101)]
transparencies = [1.0, 0.01]


# ---------------------------------------------------------------------------- #
# Things that are likely the same for all scripts
# ---------------------------------------------------------------------------- #

# This is declared BEFORE figure and ax are initialised
set_tomplot_style(fontsize=16)

for time_idx in time_idxs:

    # ------------------------------------------------------------------------ #
    # Field plots
    # ------------------------------------------------------------------------ #

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1,1,1,projection=projection)
    ax.coastlines()
    ax.stock_img()

    # ------------------------------------------------------------------------ #
    # Plot fields
    # ------------------------------------------------------------------------ #

    for field_name, method, colour_scheme, contours, transparency in \
        zip(field_names, methods, colour_schemes, all_contours, transparencies):

        data_file = Dataset(results_filename, 'r')

        coords_X, coords_Y = extract_lfric_coords(data_file, field_name)

        if field_name == 'm_cl':
            # Sum column values
            field_data = np.sum(data_file[field_name][time_idx,:,:], axis=0)
        else:
            field_data = extract_lfric_field(data_file, field_name, time_idx=time_idx, level=None)

        data_file.close()

        # ------------------------------------------------------------------------ #
        # Filter data
        # ------------------------------------------------------------------------ #

        if field_filter is not None:
            df = pd.DataFrame({'coords_X': coords_X,
                               'coords_Y': coords_Y,
                               'field_data': field_data})
            if field_filter is not None:
                df = df[(df['field_data'] > contours[0])]

            coords_X = df['coords_X'].values
            coords_Y = df['coords_Y'].values
            field_data = df['field_data'].values

        # ------------------------------------------------------------------------ #
        # Plot data
        # ------------------------------------------------------------------------ #

        if field_name == 'm_v':
            cmap, _ = tomplot_cmap(contours, colour_scheme, cmap_rescale_type='bottom',
                                   cmap_rescaling=0.5)
        elif field_name == 'sw_up_toa':

            cm_dict = {'red': ((0.0, 0.0, 0.0),
                               (1.0, 0.0, 0.0)),
                       'green': ((0.0, 0.0, 0.0),
                                 (1.0, 0.0, 0.0)),
                       'blue': ((0.0, 0.0, 0.0),
                                (1.0, 0.0, 0.0)),
                       'alpha': ((0.0, 0.2, 0.2),
                                 (1.0, 0.0, 0.0))
                      }
            pure_cmap = LinearSegmentedColormap('day', cm_dict)
            colours = pure_cmap(contours)
            cmap = ListedColormap(colours)

        else:
            cmap, _ = tomplot_cmap(contours, colour_scheme)

        cf, _ = plot_contoured_field(ax, coords_X, coords_Y, field_data,
                                     method, contours=contours,
                                     cmap=cmap, plot_contour_lines=False,
                                     projection=projection, transparency=transparency,
                                     marker_scaling=0.2, zorder=zorder)

    plot_cubed_sphere_panels(ax, linewidth=0.5)

    plotname = f'{plotdir}/{plotstem}_t{time_idx:02d}.png'
    print(f'Plotting to {plotname}')
    fig.savefig(plotname, bbox_inches='tight')
    plt.close()

