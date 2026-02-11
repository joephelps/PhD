import cdsapi

path = "/Users/phelps/PhD/DATA/ERA5"

years =['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
        '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
        '2020', '2021', '2022', '2023', '2024']

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

for year in years:


    dataset = "derived-era5-land-daily-statistics"
    request = {
        "variable": ["volumetric_soil_water_layer_1"],
        "year": year,
        "month": months,
        "day": days,
        "daily_statistic": "daily_mean",
        "time_zone": "utc+10:00",
        "frequency": "6_hourly",
        "area": [-37.4, 144.05, -37.45, 144.10]
    }

    client = cdsapi.Client()

    result = client.retrieve(dataset, request)
    result.download(f"{path}/soilwater_1_{year}.nc")
