# %% IMPORTS

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import xclim.indices as xci
import xarray as xr
from xclim.core.calendar import percentile_doy


# %% LOAD DATA 

clim_ds = xr.open_dataset('/Users/phelps/PhD/DATA/climate/SILO/processed/point/site_SILO_1980-2026.nc')


# %% TXP90 Index

baseline_start = '1980-01-01'
baseline_end = '2010-12-31'

obs_start = '2011-01-01'
obs_end = '2024-12-31'

tas = clim_ds.max_temp

tasmax_90p = percentile_doy(tas.sel(time=slice(baseline_start, baseline_end)), per=90).sel(percentiles=90)

#hot_days =xci.tx90p(tas.sel(time=slice(obs_start, obs_end)), tasmax_per=tasmax_90p)

days_over_90p = tas > tasmax_90p

# %% Functions

def heat_days(site, tas=tas, tasmax_90p=tasmax_90p):
    site_tas = tas.sel(site=site)
    site_tasmax_90p = tasmax_90p.sel(site=site)



    df_heat = pd.DataFrame({
        'time': site_tas.time.values,
        'tas': site_tas.values,
        'doy': site_tas.time.dt.dayofyear.values
    })
    df_heat.set_index('time', inplace=True)

    df_heat['tasmax_90p'] = site_tasmax_90p.values[df_heat['doy']-1]

    df_heat['heat_day'] = df_heat['tas'] > df_heat['tasmax_90p']

    return df_heat

def monthly_stats(df_heat):

    base_start=1980
    base_end=2010

    df = df_heat.resample('ME').agg(
        mean_tmax=('tas', 'mean'),
        max_tmax=('tas', 'max'),
        heat_days=('heat_day', 'sum')
        )
    
    base_period = df[(df.index.year>=base_start)
                     & (df.index.year<=base_end)]

    clim = base_period.groupby(base_period.index.month).agg(
            clim_tmax=('mean_tmax', 'mean'),
            clim_heat_days=('heat_days', 'mean')
            )
            
    df = df.join(clim, on=df.index.month)
    df['tmax_anom'] = df['mean_tmax'] - df['clim_tmax']
    df['heat_days_anom'] = df['heat_days'] - df['clim_heat_days']

    df = df.drop('key_0', axis=1)
    df['year']=df.index.year
    df['month']=df.index.month
    

    return df



def seasonal_stats(df_monthly):

    df = df_monthly.copy()
    df['year'] = df.index.year
    df.loc[df.index.month == 12, 'year'] += 1
    df['season'] = np.where(df.index.month.isin([12, 1, 2]), 'DJF',
                   np.where(df.index.month.isin([3, 4, 5]), 'MAM',
                   np.where(df.index.month.isin([6, 7, 8]), 'JJA', 'SON')))
    
    seasonal_stats = df.groupby([df.index.year, 'season']).agg(
                     heat_days=('heat_days', 'sum'),
                     mean_tmax=('mean_tmax', 'mean'),
                     max_tmax=('max_tmax', 'max'),
                     clim_heat_days=('clim_heat_days', 'sum'),
                     heat_days_anom=('heat_days_anom', 'sum')
                     ).rename_axis(['year','season']).reset_index()
    
    return seasonal_stats



def find_heat_waves(df_heat):
    df = df_heat.copy()

    groups = (df['heat_day'] != df['heat_day'].shift()).cumsum()

    # Keep only True values
    true_runs = df[df['heat_day']]

    # Group consecutive True values
    result = (
        true_runs
        .groupby(groups[df['heat_day']])
        .agg(
            start_date=('heat_day', lambda x: x.index.min()),
            end_date=('heat_day', lambda x: x.index.max()),
            run_length=('heat_day', 'size'),
            max_temp=('tas','max'),
            mean_tmax=('tas','mean')
        )
        .reset_index(drop=True)
    )

    return result
    



# %% MAIN

sites = ['cpr', 'whr','wom','wac','tum']

for site in sites:

    df_heat = heat_days(site)

    month_stats = monthly_stats(df_heat)
 
    seas_stats = seasonal_stats(month_stats)

    heat_waves = find_heat_waves(df_heat)

    month_stats = month_stats.reset_index()
    cols = list(month_stats.columns)
    # Rearrange the 'Cost Price' column to the second position (index 1)
    cols.remove('year')
    cols.remove('month')
    cols.insert(1, 'year')
    cols.insert(2, 'month')
    month_stats = month_stats[cols]

    #df_heat.to_csv(f'{site}_daily_heat.csv')
    #month_stats.to_csv(f'{site}_monthly_heat_stats.csv')
    #seas_stats.to_csv(f'{site}_seas_heat_stats.csv')
    #heat_waves.to_csv(f'{site}_heat_waves.csv')


# %% SAVE TABLES
