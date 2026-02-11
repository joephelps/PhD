
#%%
import pyet
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt



#%%

site = 'tum'
site_list = pd.read_csv('/Users/phelps/PhD/DATA/ozflux/flux_sites.csv')

site_df = site_list[site_list['site'] == f'au-{site}']
site_lat = site_df['latitude'].values[0]
site_elev = site_df['elevation'].values[0]


data =pd.read_csv(f'/Users/phelps/PhD/DATA/climate/SILO/processed/point/{site}_SILO_1980-2026.csv')
data.set_index('YYYY-MM-DD', inplace=True)
data.index = pd.to_datetime(data.index)

#time = pd.to_datetime(data['YYYY-MM-DD'])
tmax = data['max_temp']
tmin = data['min_temp']
tmean = (tmax + tmin) / 2
rh_max = data['rh_tmax']
rh_min = data['rh_tmin']
rh = (rh_max + rh_min) / 2
rs = data['radiation']
wind = pd.Series(np.full_like(tmax, 2.0))  # Assuming a constant wind speed of 2 m/s
wind.index = tmax.index
elevation = site_elev
lat = site_lat * np.pi / 180 



# %% 

pet_df = pyet.calculate_all(tmean, wind, rs, elevation, lat, tmax=tmax, tmin=tmin, rh=rh)
# %%

pet_df.to_csv(f'/Users/phelps/PhD/{site}_SILO_1980-2026_PET.csv')

# %%
