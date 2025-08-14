# import Python packages
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cmocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from tropycal import tracks, utils
import datetime as dt

#---do not modify---
def detrend(da, dim, deg=1):
    # detrend along a single dimension
    p = da.polyfit(dim=dim, deg=deg)
    fit = xr.polyval(da[dim], p.polyfit_coefficients)
    return da - fit

# open dataset using xarray (msl.nc) Mean Sea Level Pressure
filePath = 'ERA5_monthly_msl_regrid.nc'
slp = xr.open_dataset(filePath)

# display dataset
msl=slp['msl']/100

msl

SLP_Detrend =detrend(msl, 'time', deg=1)

SLP_Filt = SLP_Detrend

# climatology (average seasonal cycle) of the filtered data (do not modify)
clim_SLP = SLP_Filt.groupby(SLP_Filt['time'].dt.month).mean()

Monthly_SLP = SLP_Filt.groupby(SLP_Filt['time'].dt.month)

# monthly anomalies
anom_SLP = Monthly_SLP-clim_SLP

# display the output DataArray
anom_SLP

# open dataset using xarray (sst.nc) Sea Surface Temperatures
filePath = 'oiv2.nc'
sst = xr.open_dataset(filePath)

# display dataset
sst=sst['sst']

sst

#detrends SST so 

SST_Detrend =detrend(sst, 'time', deg=1)

SST_Filt = SST_Detrend

# climatology (average seasonal cycle) of the filtered data
clim_SST = SST_Filt.groupby(SST_Filt['time'].dt.month).mean()

Monthly_SST = SST_Filt.groupby(SST_Filt['time'].dt.month)

# monthly anomalies
anom_SST = Monthly_SST-clim_SST

# display the output DataArray
anom_SST

#loop for analysis and generation of multiple years
#LA Nina
#years=[1985, 1999, 2008, 2022]
#El Nino
years=[1983, 1987, 1998, 2016]
#Neutral
#years=[1990, 1993, 2002, 2014]

basin = tracks.TrackDataset(basin='north_atlantic',include_btk=False)

for y in years:
    start_time = str(y)+'-06-01'
    end_time = str(y)+'-11-01'
    
    ENSO_SLPA = msl.sel(time=slice(start_time, end_time)).mean('time')
    ENSO_SSTA = anom_SST.sel(time=slice(start_time, end_time)).mean('time')
    
    season = basin.get_season(y)
    hurricanes = season.to_dataframe()
    name = hurricanes[hurricanes['name'] != 'UNNAMED']
    names = name['name']
    print(names)
    
    basin = tracks.TrackDataset(basin='north_atlantic',include_btk=False)
    
    # map projection, colormap using cmocean, and levels for the colorbar
    proj = ccrs.Robinson(central_longitude=0)
    cmap = cmocean.cm.balance
    lev = np.arange(-3, 3.5, 0.5)
    contour_lev = np.arange(976, 1026, 2)
    
    fig=plt.figure(figsize=(10,4.5), dpi=300)
    ax=plt.axes(projection = proj)
    
    ENSO_SSTA.plot.contourf(
        x='lon',
        y='lat',
        ax=ax,
        transform=ccrs.PlateCarree(),
        levels=lev,
        extend='both',
        colors=cmap,
        add_colorbar=False,)

    #adds isobars
    contour_lines = ax.contour(ENSO_SLPA['lon'], ENSO_SLPA['lat'], ENSO_SLPA, levels=contour_lev,
                                  colors='grey', linestyles= 'dashed',transform=ccrs.PlateCarree())
    ax.clabel(contour_lines, inline=True, fontsize=7)
    
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', edgecolor='k', facecolor='lightgray'))
    ax.coastlines(
        resolution='110m')
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(),
                      draw_labels=True,
                      linewidth=1,
                      color='gray',
                      alpha=0.5,
                      linestyle='--')
    
    ax.set_title(str(y))
    
    for i in names:  
    
        storm = basin.get_storm((i,y))
    
        # Append Tropycal functionality to this axes
        ax = utils.add_tropycal(ax)
    
        # Plot Hurricane Michael's track line
        ax.plot_storm(storm, color='k', linewidth=1)
    
        # Plot storm dots in blue
        ax.plot_storm(storm, 'o', ms=4, mfc='lime', mec='none')
    
    # Zoom in over the Atlantic Ocean and Gulf of Mexico
    ax.set_extent([-100,0,0,60])
    
    fig.savefig('ENSONeutral'+str(y)+'.png', facecolor='white', transparent=False, bbox_inches='tight')

    print(ENSO_SLPA.min().values)
    print(ENSO_SLPA.max().values)
