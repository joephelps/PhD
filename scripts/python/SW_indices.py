# %% IMPORTS

import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# %% LOAD DATA

swvl1 = xr.open_dataset("/Users/phelps/PhD/DATA/ERA5-Land/swvl1_1980-2024.nc").squeeze(drop=True)
swvl1_df = swvl1.to_dataframe()
# %% INDICES/STATISTICS FUNCTIONS

def SWI(sw,window=365, baseline_start='1980-01-01', baseline_end='2009-12-31'):
    # 1. compute N-month rolling sum
    SW_N_mo = sw.rolling(window=window, min_periods=window).sum()

    # 2. select baseline period
    baseline_mask = (sw.index >= baseline_start) & (sw.index <= baseline_end)
    baseline_12mo = SW_N_mo[baseline_mask].dropna()

    # 3. compute percentile rank for each date
    def percentile_rank(value):
        return 100 * (baseline_12mo <= value).sum() / len(baseline_12mo)

    swi = SW_N_mo.apply(percentile_rank)

    return swi

def SW_climatology(sw, baseline_start='1980-01-01', baseline_end='2009-12-31'):
    baseline_mask = (sw.index >= baseline_start) & (sw.index <= baseline_end)
    baseline_sw = sw[baseline_mask]
    climatology = baseline_sw.groupby(baseline_sw.index.dayofyear).mean()
    return climatology

def SW_anomaly(sw, climatology):
    day_of_year = sw.index.dayofyear
    climatology_aligned = climatology.reindex(day_of_year).values
    anom = sw.values - climatology_aligned
    return pd.Series(anom, index=sw.index)

# %% MAIN

sw_D = swvl1_df['swvl1']
sw_M = swvl1_df['swvl1'].resample('MS').mean()

SWI_1_180 = SWI(swvl1_df['swvl1'], window=180)
SWI_1_365 = SWI(swvl1_df['swvl1'], window=365)

SWI_1_6 = SWI(swvl1_df['swvl1'].resample('MS').sum(), window=6)
SWI_1_12 = SWI(swvl1_df['swvl1'].resample('MS').sum(), window=12)

SW_climatology = SW_climatology(swvl1_df['swvl1'])
SW_anom = SW_anomaly(swvl1_df['swvl1'], SW_climatology)

SW_anom_M = SW_anom.resample('MS').mean()


indices_monthly_df = pd.DataFrame({
    'date':SWI_1_6.index,
    'swvl1': sw_M.values,
    'SWI_1_6': SWI_1_6.values,
    'SWI_1_12': SWI_1_12.values,
    'SW_anom_M': SW_anom_M.values
})

indices_daily_df = pd.DataFrame({
    'date':SWI_1_180.index,
    'swvl1': sw_D.values,
    'SWI_1_180': SWI_1_180.values,
    'SWI_1_365': SWI_1_365.values,
    'SW_anom': SW_anom.values
})


# %% SAVE OUPUTS
indices_monthly_df.to_csv('/Users/phelps/PhD/DATA/climate/Indices/monthly/SW_indices_M.csv')
indices_daily_df.to_csv('/Users/phelps/PhD/DATA/climate/Indices/daily/SW_indices_D.csv')
# %%
