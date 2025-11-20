import requests

download_location = 0 # 0: local, 1: mediaflux

output_path = '/Users/phelps/PhD_Project/data/climate/raw'

variable_names = ['min_temp', 'daily_rain', 'vp_deficit', 'rh_tmax', 'rh_tmin', 'radiation']
years = range(2000, 2025)

variable_name = 'daily_rain'
period = 'daily'

for variable_name in variable_names:
    for year in years:
    
        url = f'https://s3-ap-southeast-2.amazonaws.com/silo-open-data/Official/annual/{variable_name}/{year}.{variable_name}.nc'
        output_file = f"{output_path}/{variable_name}/{year}.{variable_name}.nc"

        response = requests.get(url)
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {output_file}")
    print(f"Completed downloads for {variable_name}")