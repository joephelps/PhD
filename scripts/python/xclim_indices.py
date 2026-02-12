# %% IMPORTS ###

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from xclim.indices import standardized_precipitation_index,standardized_precipitation_evapotranspiration_index, antecedent_precipitation_index
from xclim.indices.stats import standardized_index_fit_params
import xarray as xr

# %% LOAD CLIMATE DATA ###

def load_data(site):
    clim_data =pd.read_csv(f'/Users/phelps/PhD/DATA/climate/SILO/processed/point/{site}_SILO_1980-2026.csv')
    clim_data.set_index('YYYY-MM-DD', inplace=True)
    clim_data.index = pd.to_datetime(clim_data.index)

    PET_data = pd.read_csv('/Users/phelps/PhD/DATA/climate/PET/wom_SILO_1980-2026_PET.csv')
    PET_data.set_index('YYYY-MM-DD', inplace=True)
    PET_data.index = pd.to_datetime(PET_data.index)

    return clim_data, PET_data


# %% climate indices ###

def spi(pr, window):
    spi = standardized_precipitation_index(
        pr=pr,
        freq="MS",
        window=window,
        dist="gamma",
        method="ML",
        fitkwargs = {"floc": 0},
        cal_start="1980-01-01",
        cal_end="2009-12-31"
    )
    return spi

def spei(wb, window):
    spei = standardized_precipitation_evapotranspiration_index(
        wb=wb,
        freq="MS",
        window=window,
        dist="fisk",
        method="ML",
        cal_start="1980-01-01",
        cal_end="2009-12-31"
    )
    return spei

def api(pr, window, p_exp=0.935):
    api = antecedent_precipitation_index(
        pr=pr,
        window=window,
        p_exp=p_exp
    )
    return api

# %% MAIN ###

sites = ['cpr','whr','wom','tum','wac']

for site in sites:
    clim_data, PET_data = load_data(site)

    pr = xr.DataArray(
        clim_data['daily_rain'],
        coords=[clim_data.index],
        dims=['time'],
        attrs={'units': 'mm/day'}
    )
    wb = xr.DataArray(
        clim_data['daily_rain'] - PET_data['Penman'],
        coords=[clim_data.index],
        dims=['time'],
        attrs={'units': 'mm/day'}
    )

    spi_6 = spi(pr, window=6)
    spi_12 = spi(pr, window=12)
    spei_12 = spei(wb, window=12)
   

    indices_df = pd.DataFrame({
        'date':spi_6.time.values,
        'SPI_6': spi_6.values,
        'SPI_12': spi_12.values,
        'SPEI_12': spei_12.values
    })

    indices_df.to_csv(f'/Users/phelps/PhD/DATA/climate/Indices/monthly/{site}_climate_indices.csv')

# %%
