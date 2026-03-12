#%% IMPORTS
import pandas as pd
import numpy as np
import xarray as xr
from xclim.indices import standardized_precipitation_evapotranspiration_index as xc_spei
from xclim.indices import standardized_precipitation_index as xc_spi
import matplotlib.pyplot as plt
#%% FUNCTIONS

def load_terra(site):
    path = '/Users/phelps/PhD/TerraClim/all_data'
    filename = f'{path}/{site}.nc'
    ds = xr.open_dataset(filename).squeeze(drop=True)
    #days_in_month = ds["time"].dt.days_in_month
    #converts ppt and pet to mm/day for xclim inputs
    #ds['ppt'] = ds['ppt']/days_in_month
    #ds['pet'] = ds['pet']/days_in_month
    ds["aet"].attrs["units"] = "mm"
    ds["pet"].attrs["units"] = "mm/month"
    ds["ppt"].attrs["units"] = "mm/month"
    ds["soil"].attrs["units"] = "mm"
    ds["srad"].attrs["units"] = "W/m^2"
    ds["tmax"].attrs["units"] = "degC"
    ds["vpd"].attrs["units"] = "kPa"
    return ds

def make_df(ds):
    df = ds.to_dataframe()
    df.index = pd.to_datetime(df.index)
    return df

def monthly_climatology(df,var):  
    df = df[df.index.year.isin(base_period())]


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
    df = pd.DataFrame(df[df.index.year.isin(obs_period())][var])
    df['month']=df.index.month
    df = df.merge(clim_df, left_on="month", right_index=True)
    df['anom'] = df[var]-df['mean']
    df['z']=df['anom']/df['std']
    df['below_p10'] = df[var]<df['p10']
    df['above_p90'] = df[var]>df['p90']

    stats_df = df[[var,'anom','z','above_p90','below_p10']]
    return stats_df

def calc_spei(ds, window):
    ppt = ds.ppt
    pet = ds.pet
    wb = ppt-pet
    start_year = base_period()[0]
    end_year = base_period()[len(base_period())-1]
    cal_start=f'{start_year}-01-01'
    cal_end=f'{end_year}-12-31'

    wb.attrs['units']='mm/day'

    spei = xc_spei(wb,window=window,dist='gamma',method='ML',
                   cal_start=cal_start,cal_end=cal_end)
    return spei



def base_period(start_year=1958, end_year=2000):
    period = [year for year in range(start_year, end_year)]
    return period
def obs_period(start_year=2000, end_year=2026):
    period = [year for year in range(start_year, end_year)]
    return period


# %% MAIN - creating anomaly tables

sites = ['cpr','whr','wom','wac','tum']
for site in sites:
    ds = load_terra(site)
    df=make_df(ds)
    df['wb']=df['ppt']-df['pet']
    #df.to_csv(f'{site}_terra.csv')
    vars=['vpd','tmax','soil','ppt','pet','srad','wb']

    anom_df = pd.DataFrame()



    for var in vars:
        anom_df[f'{var}_anom'] = stats(df,var)['anom']
        anom_df[f'{var}_z'] = stats(df,var)['z']

    anom_df['wb_below_p10'] = stats(df,'wb')['below_p10']

    #merged_df = pd.merge(anom_df,spei_df,on='time',how='inner')


    anom_df.to_csv(f'{site}_terra_anoms.csv')

# %%
