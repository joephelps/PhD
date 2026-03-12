#%% Imports

import pandas as pd
import numpy as np

#%%
def create_date_list(ranges):
    date_list = []
    for range in ranges:
        start_date = range[0]
        end_date = range[1]
        date_list += pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y-%m-%d').tolist()
    
    return pd.to_datetime(date_list)


cpr_dates = create_date_list([['2010-07-30', '2014-01-14'],
                               ['2017-01-01', '2020-06-01']])

whr_dates = create_date_list([['2011-12-01', '2017-07-06'],
                              ['2019-06-13', '2022-01-01'],
                              ['2023-08-17', '2023-12-31']])

wom_dates = create_date_list([['2010-01-20', '2016-05-25'],

                              ['2017-01-18', '2021-05-29'],
                              ['2024-05-09', '2025-02-01']])

tum_dates = create_date_list([['2002-01-07', '2019-12-30']])

wac_dates = create_date_list([['2005-08-25', '2008-12-31']])

all_dates = create_date_list([['2000-01-01','2025-12-31']])

date_ranges = [cpr_dates, whr_dates, wom_dates, tum_dates, wac_dates]
# %%

date_mask = pd.DataFrame()
date_mask.index = all_dates
date_mask.index.name='time'
date_mask.index = pd.to_datetime(date_mask.index)

date_mask['cpr'] = date_mask.index.isin(cpr_dates)
date_mask['whr'] = date_mask.index.isin(whr_dates)
date_mask['wom'] = date_mask.index.isin(wom_dates)
date_mask['wac'] = date_mask.index.isin(wac_dates)
date_mask['tum'] = date_mask.index.isin(tum_dates)


date_mask.to_csv('flux_date_mask.csv')
# %%
