#%% IMPORTS
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
# %% FUCNTIONS

def load_flux_data(site,window):
    path = '/Users/phelps/PhD/DATA/ozflux/L6'
    ds = xr.open_dataset(f'{path}/{site}_summary_L6.nc', group=window)
    #ds = all_ds.window
    return ds.squeeze(drop=True)


def make_df(ds, vars):
    df = ds[vars].to_dataframe()
    df['time'] = ds.time
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df.index = df.index.normalize()

    return df

def monthly_climatology(df,var):  
    
    monthly_clim = df.groupby(df.index.month).agg(
        mean=(var, 'mean'),
        std=(var, 'std'),
        p10=(var, lambda x: x.quantile(0.10)),
        p90=(var, lambda x: x.quantile(0.90)),

    )
    monthly_clim.index.name='month'
    return monthly_clim

def stats(df,var):
    clim_df=monthly_climatology(df,var)
    df['month']=df.index.month
    df = df.merge(clim_df, left_on="month", right_index=True)
    df['anom'] = df[var]-df['mean']
    df['z']=df['anom']/df['std']
    df['below_p10'] = df[var]<df['p10']
    df['above_p90'] = df[var]>df['p90']

    stats_df = df[[var,'anom','z','above_p90','below_p10']]
    return stats_df

# %%
site='cpr'

vars = ['Sws','GPP_SOLO','ER_SOLO','ET', 'Precip', 'Fsd']

flux_df = make_df(load_flux_data(site,'Monthly'),vars)
flux_df = flux_df.replace(-9999, np.nan)

flux_df.to_csv(f'{site}_month_summary.csv')


anom_df = pd.DataFrame()

for var in vars:
    anom_df[f'{var}_anom'] = stats(flux_df,var)['anom']
    anom_df[f'{var}_z'] = stats(flux_df,var)['z']

anom_df.to_csv(f'{site}_monthly_anoms.csv')


# %%
