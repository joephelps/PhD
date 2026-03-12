#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%%

def load_flux(site):
    df = pd.read_csv(f'/Users/phelps/PhD/daily_data/flux/{site}_D_summary.csv')
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index)
    df['gpp_rolling']= df['GPP_SOLO'].rolling(window=30).mean()
    df["growing_year"] = df.index.year + (df.index.month >= 7).astype(int)
    df['gy_doy'] =df.index.map(get_dayof_gy)

    return df

def get_dayof_gy(date):
    if date.year % 4 ==0:
        if date>= pd.to_datetime(f'{date.year}-02-29'):

            day = ((date.dayofyear - 183) % 366) + 1

        else:
             day = ((date.dayofyear - 182) % 366) + 1
    else:
        day = ((date.dayofyear - 182) % 365) + 1
    return day

def site_dates(site):
    mask = pd.read_csv('/Users/phelps/PhD/DATA/ozflux/flux_date_mask.csv')
    mask['time'] = pd.to_datetime(mask['time'])
    mask.index=mask['time']
    site_mask = mask[[site]]
    date_list = site_mask[site_mask[site]==True].index
    return date_list


#%%

sites = ['cpr','whr','wom','wac','tum']
fig, axes = plt.subplots(2,5,figsize=(32,12),dpi=200,sharex=True)
for i,site in enumerate(sites):

    df = load_flux(site)
    df['cum_gpp'] = df.groupby('growing_year')['GPP_SOLO'].cumsum()

    df_obs = df[df.index.isin(site_dates(site))]
    df_obs_mean = df_obs.groupby('gy_doy')['gpp_rolling'].mean()

    counts = df_obs.groupby('growing_year')['GPP_SOLO'].count()
    valid_years = counts[counts >= 360].index
    df_complete = df_obs[df_obs['growing_year'].isin(valid_years)]

    years = sorted(df_obs['growing_year'].unique())
    cmap = plt.cm.tab20

    dry_years =[2019]


    axes[0,i].plot(df_obs_mean,color='black')
    for j, (gy, d) in enumerate(df_obs.groupby('growing_year')):
        color = cmap(j / len(years))

        if gy in dry_years:

            axes[0,i].plot(d['gy_doy'], d['gpp_rolling'],color=color, label=gy)
            if gy in valid_years:
                axes[1,i].plot(d['gy_doy'], d['cum_gpp'],color=color,label=gy)
        else:
            axes[0,i].plot(d['gy_doy'], d['gpp_rolling'], color='gray',alpha=0.4)
            if gy in valid_years:
                axes[1,i].plot(d['gy_doy'], d['cum_gpp'], color='gray',alpha=0.4)

        if gy in valid_years:
            axes[1,i].plot(d['gy_doy'], d['cum_gpp'],color='gray',alpha=0.4)

    
    axes[0,i].legend(loc='center left', bbox_to_anchor=(1, 0.5))






    
    axes[0,i].set_title(site)
    
#df[df['growing_year']==2012]['cum_gpp'].plot()
# %%

