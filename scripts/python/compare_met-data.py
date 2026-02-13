# %% IMPORTS

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %% LOAD DATA FUNCTIONS

def load_ERA5(path, site, variable):
    ds = xr.open_dataset(f"{path}/ERA5-Land/{site}_{variable}_*.nc")
    return ds

def load_SILO(site,path='/Users/phelps/PhD/DATA/climate/SILO/processed/point'):
    df = pd.read_csv(f"{path}/{site}_SILO_1980-2026.csv")
    return df

def load_ozflux(site,path='/Users/phelps/PhD/DATA/ozflux/L6'):
    ds = xr.open_dataset(f"{path}/{site}_L6.nc")
    return ds

# %% DATA PREPROCESSING FUNCTIONS

def get_daily(ds, variable, method):

    if method == 'mean':
        daily_ds = ds[variable].resample(time='1D').mean()
    elif method == 'sum':
        daily_ds = ds[variable].resample(time='1D').sum()
    elif method == 'max':
        daily_ds = ds[variable].resample(time='1D').max()
    elif method == 'min':
        daily_ds = ds[variable].resample(time='1D').min()
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', 'max', or 'min'.")
        
    return daily_ds




def ozflux_to_daily(ds):

    daily_rain = get_daily(ds, 'Precip', 'sum').squeeze()
    max_temp = get_daily(ds, 'Ta', 'max').squeeze()
    rh_tmax = get_daily(ds, 'RH', 'max').squeeze()
    min_temp = get_daily(ds, 'Ta', 'min').squeeze()
    rh_tmin = get_daily(ds, 'RH', 'min').squeeze()
    radiation = get_daily(ds, 'Fsd', 'sum').squeeze()
    Sws = get_daily(ds, 'Sws', 'mean').squeeze()


    df = pd.DataFrame({
        'date': daily_rain.time.values,
        'daily_rain': daily_rain.values,
        'max_temp': max_temp.values,
        'rh_tmax': rh_tmax.values,
        'min_temp': min_temp.values,
        'rh_tmin': rh_tmin.values,
        'radiation': radiation.values,
        'Sws': Sws.values
    })

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

def ozflux_SW_data(ds, variable="Sws"):

    Sws = ds[variable]
    Sws_daily = get_daily(Sws, variable, 'mean')
    return Sws_daily
    
# %%
