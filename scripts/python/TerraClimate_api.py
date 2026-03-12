# %%
import pandas as pd
import requests
#%%

def download_terra(site, bbox, var):
    # Base URL
    base_url = f"http://thredds.northwestknowledge.net:8080/thredds/ncss/agg_terraclimate_{var}_1958_CurrentYear_GLOBE.nc"

    # Parameters (cleaner than hardcoding the whole URL)
    params = {
        "var": var,
        "north": bbox[0],
        "west": bbox[3],
        "east": bbox[2],
        "south": bbox[1],
        "disableProjSubset": "on",
        "horizStride": 1,
        "time_start": "1950-01-01T00:00:00Z",
        "time_end": "2025-12-01T00:00:00Z",
        "timeStride": 1,
        "accept": "netcdf"
    }

    # Output file name
    output_file = f"TerraClim/{site}_terraclimate_{var}_1950_2025.nc"

    # Make request
    response = requests.get(base_url, params=params, stream=True)

    # Check request
    response.raise_for_status()

    # Save to file
    with open(output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Saved to {output_file}")

def get_bbox(lat, lon):
    bbox = []
    bbox.append(lat+0.001)
    bbox.append(lat-0.001)
    bbox.append(lon+0.001)
    bbox.append(lon-0.001)
    return bbox


# %%


site_meta = pd.read_csv('/Users/phelps/PhD/DATA/ozflux/flux_sites.csv')

vars = ['ppt']

for var in vars:

    for index,row in site_meta.iterrows():
        bbox = get_bbox(row['latitude'], row['longitude'])
        site = row['site_name']
        download_terra(site, bbox, var)


# %%
