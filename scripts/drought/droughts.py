# %% IMPORTS

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import xclim.indices as xci
import xarray as xr
from xclim.core.calendar import percentile_doy
import seaborn as sns

# %% LOAD DATA
clim_ds = xr.open_dataset('/Users/phelps/PhD/DATA/climate/SILO/processed/point/site_SILO_1980-2026.nc')
pr = clim_ds.pr
pr_monthly = pr.resample(time='1ME').sum()
# %% RAIN MONTH & SEASON TOTALS AND PERCENTILES

def month_stats(site,pr_monthly=pr_monthly):

    base_start=1980
    base_end=2010

    pr_monthly=pr_monthly.sel(site=site)
    df = pd.DataFrame({
        'time': pr_monthly.time.values,
        'pr': pr_monthly.values
    })
    df.set_index('time', inplace=True)

    base_period = df[(df.index.year>=base_start)
                                  & (df.index.year<=base_end)]

    clim = base_period.groupby(base_period.index.month).agg(
            pr_clim=('pr', 'mean'),
            pr_std=('pr', 'std'),
            pr_10p=('pr', lambda x: x.quantile(0.10))
            )
    
    df = df.join(clim, on=df.index.month)
    df['pr_anom'] = df['pr'] - df['pr_clim']
    df['z_pr'] = df['pr_anom'] / df['pr_std']
    df['pr_below_10p'] = df['pr'] < df['pr_10p']
    return df

def seasonal_stats(df_monthly):

    base_start=1980
    base_end=2010
             
    df=df_monthly.copy()
    df['year'] = df.index.year
    df.loc[df.index.month == 12, 'year'] += 1

    df['season'] = np.where(df.index.month.isin([12, 1, 2]), 'DJF',
                    np.where(df.index.month.isin([3, 4, 5]), 'MAM',
                    np.where(df.index.month.isin([6, 7, 8]), 'JJA', 'SON')))
    seasonal_totals = (
        df
        .groupby([df.index.year, 'season'])['pr']
        .sum()
        .unstack()   # seasons become columns
    )

    seasonal_totals.index.name = 'year'

    seasonal_totals = seasonal_totals.reset_index().melt(id_vars='year', var_name='season', value_name='pr')

    base_period = seasonal_totals[(seasonal_totals['year']>=base_start)
                                  & (seasonal_totals['year']<=base_end)]

    clim = base_period.groupby(base_period['season']).agg(
            pr_clim=('pr', 'mean'),
            pr_std =('pr', 'std'),
            pr_10p=('pr', lambda x: x.quantile(0.10))
            )
    
    seasonal_totals = seasonal_totals.join(clim, on=seasonal_totals['season'])
    seasonal_totals['pr_anom'] = seasonal_totals['pr'] - seasonal_totals['pr_clim']
    seasonal_totals['z_pr'] = (seasonal_totals['pr'] - seasonal_totals['pr_clim'])/seasonal_totals['pr_std']

    seasonal_totals['pr_below_10p'] = seasonal_totals['pr'] < seasonal_totals['pr_10p']

    seasonal_totals = seasonal_totals.drop('key_0', axis=1)
    seasonal_totals =seasonal_totals.set_index('year').sort_index()

    return seasonal_totals.reset_index()


# %% PLOT SEASONAL RAINFALL TOTALS
sites = ['cpr', 'whr', 'wom', 'wac', 'tum']

fig, axes = plt.subplots(1,5,figsize=(16, 4), sharey=True, layout='tight')

for i, site in enumerate(sites):
    seasonal_totals = seasonal_stats(month_stats(site))
    sns.boxplot(x='season', y='pr',
                 data=seasonal_totals, order=['DJF','MAM','JJA','SON'],
                   ax=axes[i], showfliers=False)
    axes[i].set_title(site)
        
sites = ['cpr', 'whr','wom','wac','tum']


# %%
for site in sites:
    monthly_stats = month_stats(site)
    seas_stats = seasonal_stats(monthly_stats)

    monthly_stats.to_csv(f'{site}_monthly_rain_stats.csv')
    seas_stats.to_csv(f'{site}_seas_rain_stats.csv')

# %%
