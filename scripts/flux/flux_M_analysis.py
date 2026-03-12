#%% IMPORTS
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
# %% FUCNTIONS

def load_df(path):
    df = pd.read_csv(path)
    df['time'] =  pd.to_datetime(df['time'])
    df = df.set_index('time')
    
    return df

def season(date):
    if date.month in [12,1,2]:
        return 'DJF'
    elif date.month in [3,4,5]:
        return 'MAM'
    elif date.month in [6,7,8]:
        return 'JJA'
    else:
        return 'SON'

#%% LOAD DATA

site = 'cpr'

flux_data = load_df(f'/Users/phelps/PhD/monthly_data/{site}_month_summary.csv')
flux_anom = load_df(f'/Users/phelps/PhD/monthly_data/{site}_monthly_anoms.csv')
terra_data = load_df(f'/Users/phelps/PhD/monthly_data/{site}_terra.csv')
terra_anom = load_df(f'/Users/phelps/PhD/monthly_data/{site}_terra_anoms.csv')
# %%

anoms_df = pd.merge(flux_anom, terra_anom,on='time',how='inner')

df = pd.merge(flux_data,terra_data,on='time', how='inner')
df["NEE"] = df['GPP_SOLO'] - df['ER_SOLO']
df["season"] = df.index.map(season)
df['month'] = df.index.month

anoms_df["season"] = anoms_df.index.map(season)


df_long_month = df.melt(id_vars=['month'], 
                                             value_vars=["GPP_SOLO", 'ER_SOLO'],
                                             var_name="variable", value_name="value")

df_long_season = df.melt(id_vars=['season'], 
                                             value_vars=["GPP_SOLO", 'ER_SOLO', 'NEE'],
                                             var_name="variable", value_name="c-flux")

# %%


plt.figure(figsize=(10,6))

sns.boxplot(x="season", y="c-flux", hue="variable", 
            data=df_long_season, showfliers=False)
plt.title("Monthly C-fluxes")
plt.show()


# %%
fig, ax = plt.subplots(figsize=(10,6))

ax.bar(df.index,df.ppt)
ax2=ax.twinx()
ax2.plot(df.index,df.NEE)
# %%
