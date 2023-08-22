import os
import xarray as xr
import pandas as pd
import glob

base_dir = r"Z:\GLO\TC_related"
events = ['Left', 'MostLikely', 'Right']

for event in events:
    in_dir = os.path.join(base_dir, event)
    out_dir = os.path.join(base_dir, f'{event}_shifted')
    os.makedirs(out_dir, exist_ok=True)

    nc_files = glob.glob(os.path.join(in_dir, '*.nc'))

    for file in nc_files:
        ds = xr.open_dataset(file)

        # Generate new time dimension
        new_time = pd.date_range(start="1970-01-01 00:30", periods=len(ds['time']), freq='H')
        ds = ds.assign_coords(time=new_time)

        # Generate new output file path
        base = os.path.basename(file)
        new_file = os.path.join(out_dir, base.rsplit(".", 1)[0] + "_shift1970.nc")

        ds.to_netcdf(new_file)
