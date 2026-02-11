import cdsapi
from urllib3 import request

#dataset = "derived-era5-single-levels-daily-statistics" # "derived-era5-single-levels-daily-statistics" or "derived-era5-land-daily-statistics" for daily ERA5/ERA5-Land data

#variable = 'volumetric_soil_water_layer_1'

#site = 'wom'
extent = [-37.4, 144.05, -37.45, 144.10]

years = ['2015', '2016', '2017', '2018', '2019',
         '2020', '2021', '2022', '2023', '2024']

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

path = "/Users/phelps/PhD/DATA" 

def get_extent(latitude,longitude):
    """
    Get the extent for a given latitude and longitude.
    
    Parameters
    ----------
    latitude : float
        Latitude of the point of interest.
    longitude : float
        Longitude of the point of interest.
    
    Returns
    -------
    list
        Extent in the format [lat_max, lon_min, lat_min, lon_max].
    """
    lat_max = latitude + 0.05
    lat_min = latitude - 0.05
    lon_max = longitude + 0.05
    lon_min = longitude - 0.05
    
    return [lat_max, lon_min, lat_min, lon_max]

def download_ERA5(dataset, variable, year, months, days, extent, path):

    if dataset == "derived-era5-land-daily-statistics":
        
        request = {
            "variable": [variable],
            "year": year,
            "month": months,
            "day": days,
            "daily_statistic": "daily_mean",
            "time_zone": "utc+10:00",
            "frequency": "6_hourly",
            "area": extent
        }

        client = cdsapi.Client()

        result = client.retrieve(dataset, request)
        result.download(f"{path}/ERA5-Land/{variable}_{year}.nc")
    
    elif dataset == "derived-era5-single-levels-daily-statistics":

        request = {
            "product_type": "reanalysis",
            "variable": variable,
            "year": year,
            "month": months,
            "day": days,
            "daily_statistic": "daily_sum",
            "time_zone": "utc+10:00",
            "frequency": "1_hourly",
            "area": extent
        }

        client = cdsapi.Client()
    
        result = client.retrieve(dataset, request)
        result.download(f"{path}/ERA5/{variable}_{year}.nc")


for year in years:

 

    dataset = "derived-era5-land-daily-statistics"
    variable = 'volumetric_soil_water_layer_1'
    download_ERA5(dataset, variable, year, months, days, extent, path)


