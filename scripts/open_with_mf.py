from mediaflux import mf_utils as mf
import xarray as xr
import tempfile


with tempfile.TemporaryDirectory() as tmpdir:
    # Download a NetCDF file from Mediaflux
    mf.download_from_mediaflux(
        src_path="/projects/proj-6600_phelps_data-1128.4.1369/Whroo_L6.nc",
        local_dir=tmpdir
    )
    
    # Load the NetCDF file using xarray
    local_file_path = f"{tmpdir}/Whroo_L6.nc"
    dataset = xr.open_dataset(local_file_path)
    print(dataset)
    






