#%% IMPORTS
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
# %% FUCNTIONS

def load_flux_data(site,window):
    path = '/Users/phelps/PhD/DATA/ozflux/L6'
    ds = xr.open_dataset(f'{path}/{site}_summary_L6_2.nc', group=window)
    #ds = all_ds.window
    return ds.squeeze(drop=True)


def make_df(ds, vars):
    df = ds[vars].to_dataframe()
    df['time'] = ds.time
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df.index = df.index.normalize()

    return df
# %%
sites = ['cpr','whr','wom','wac','tum']

vars = ['Sws','Ta','GPP_SOLO','ER_SOLO','ET', 'Precip', 'Fsd']

for site in sites:

    flux_df = make_df(load_flux_data(site,'Daily'),vars)
    flux_df = flux_df.replace(-9999, np.nan)

    flux_df.to_csv(f'/Users/phelps/PhD/daily_data/flux/{site}_D_summary.csv')

# %%
flux_df = make_df(load_flux_data('wom','Daily'),vars)
flux_df = flux_df.replace(-9999, np.nan)

flux_df.to_csv(f'/Users/phelps/PhD/daily_data/flux/wom2_D_summary.csv')
# %%
